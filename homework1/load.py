#!/usr/bin/python2.7
import requests
import json
import sys
import re
from collections import defaultdict
from string import punctuation

url = 'https://inf551-hanz.firebaseio.com/'  # my database url.
print('my database url: ' + url)
load_loc = sys.argv[1]  # get data location.
complete_url = url + load_loc

with open(load_loc) as load_f:
    load_dict = json.load(load_f)
    response = requests.put(complete_url, json.dumps(load_dict))  # upload prize data.
    print("prize data uploaded, response status code: " + str(response.status_code))

stopwords_loc = 'stopwords.txt'
stopwords_list = []
with open(stopwords_loc, 'r') as load_f:
    stopwords_list = [line.strip('\n') for line in load_f.readlines()]  # load stopwords


index = defaultdict(list)

# index = {}  # create index dictionary.
prizes = load_dict['prizes']
for prize in prizes:
    for laureate in prize['laureates']:
        if 'motivation' in laureate.keys():
            motivation_words = json.dumps(laureate['motivation']).lower()
            motivation_words = re.sub(re.escape(punctuation), '', motivation_words).split()
            # re.split("[ ,.\?\!]", re.sub(s.lower())
            # s = re.sub(re.escape(punctuation), "", s)
            for word in motivation_words:
                word = ''.join(x for x in word if x.isalnum())
                if not (word in stopwords_list) and word is not '':
                    # if word in index.keys():
                    index[word].append(int(laureate['id']))
                    # else:
                    #     index[word] = [int(laureate['id'])]
response = requests.put(url + "prize/index.json", json.dumps(index))  # upload index data.
print("index data uploaded, response status code: " + str(response.status_code))
