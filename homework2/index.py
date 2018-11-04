#!/usr/bin/python2.7
from lxml import etree
import sys

load_loc = sys.argv[1]  # get data location.
save_loc = sys.argv[2]  # get save location.

stopwords_loc = 'stopwords.txt'
stopwords_list = []
with open(stopwords_loc, 'r') as load_f:
    stopwords_list = [line.strip('\n') for line in load_f.readlines()]  # load stopwords

f = open(load_loc)
prizes = etree.parse(f)

index = dict()  # create index dictionary.

for prize in prizes.iter():
    for laureate in prize.iter():
        laureate_id = laureate.get('id')
        motivation = laureate.findtext('motivation')
        motivation = motivation.lower().split() if motivation else ''
        for word in motivation:
            word = ''.join(x for x in word if x.isalnum())
            if not (word in stopwords_list) and word is not '':
                if word in index and int(laureate_id) not in index[word]:
                    index[word].append(int(laureate_id))
                else:
                    index[word] = [int(laureate_id)]

index_xml = etree.Element("index")
for keyword, ids in index.items():
    entry_xml = etree.SubElement(index_xml, 'entry')
    keyword_xml = etree.SubElement(entry_xml, "keyword")
    keyword_xml.text = keyword
    ids_xml = etree.SubElement(entry_xml, "ids")
    for id_num in ids:
        id_xml = etree.SubElement(ids_xml, "id")
        id_xml.text = str(id_num)

with open(save_loc, 'wb') as save_f:
    save_f.write(etree.tostring(index_xml, pretty_print=True))

