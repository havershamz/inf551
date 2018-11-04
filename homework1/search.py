#!/usr/bin/python2.7
import sys
import requests

url = 'https://inf551-hanz.firebaseio.com/'  # my database url.

inputs = sys.argv[1].lower().split()
laureate_ids = []  # create a list to store all related laureates' id
for keyword in inputs:
    response = requests.get(url+'prize/index.json?orderBy="$key"&equalTo="{}"'.format(keyword))
    tmp_laureate_ids = response.json().values()[0] if response.json().values() else []
    for laureate_id in tmp_laureate_ids:
        if laureate_id not in laureate_ids:
            laureate_ids.append(laureate_id)

prize_ids = []  # create a list to store all related prizes' id
response = requests.get(url+'prize/prizes.json')
for prize in response.json():
    for laureate in prize['laureates']:
        if int(laureate['id']) in laureate_ids and int(response.json().index(prize)) not in prize_ids:
            prize_ids.append(int(response.json().index(prize)))
            break

print(prize_ids)

