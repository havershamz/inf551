#!/usr/bin/python2.7
import sys
import mysql.connector

input = sys.argv[1].lower()

cnx = mysql.connector.connect(user='inf551', password='inf551',
                              host='127.0.0.1', database='world')

cursor = cnx.cursor()

query = 'select headofstate from country where name = "{}";'.format(input)

cursor.execute(query)

for headofstate in cursor:
    print headofstate[0]

cursor.close()
cnx.close()
