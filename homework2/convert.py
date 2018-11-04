#!/usr/bin/python2.7
import json
from lxml import etree
import sys

load_loc = sys.argv[1]  # get data location.
save_loc = sys.argv[2]  # get save location.

with open(load_loc) as load_f:
    load_dict = json.load(load_f)

prizes = load_dict['prizes']
prizes_xml = etree.Element("prizes")
for prize in prizes:
    prize_xml = etree.Element(prize['category'])
    for laureate in prize['laureates']:
        laureate_xml = etree.Element("laureate", id=laureate['id'], year=prize['year'])
        firstname = etree.SubElement(laureate_xml, "firstname")
        firstname.text = laureate['firstname']
        surname = etree.SubElement(laureate_xml, "surname")
        surname.text = laureate['surname']
        if 'motivation' in laureate.keys():
            motivation = etree.SubElement(laureate_xml, "motivation")
            motivation.text = laureate['motivation']
        share = etree.SubElement(laureate_xml, "share")
        share.text = laureate['share']
        prize_xml.append(laureate_xml)
    prizes_xml.append(prize_xml)

with open(save_loc, 'wb') as save_f:
    save_f.write(etree.tostring(prizes_xml, pretty_print=True))
