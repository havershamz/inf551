#!/usr/bin/python2.7
import json
from lxml import etree
import sys

load_loc = sys.argv[1]  # get data location.
inputs = sys.argv[2].lower().split()
laureate_ids = []

f = open(load_loc)
index = etree.parse(f)

for keyword in inputs:
    for element in index.xpath('//entry[keyword="'+keyword+'"]'):
        for laureate_id in element.iter('id'):
            if int(laureate_id.text) not in laureate_ids:
                laureate_ids.append(int(laureate_id.text))

print(laureate_ids)
