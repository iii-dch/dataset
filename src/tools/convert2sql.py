import sys
import csv
import urllib.request, json
import argparse
import yaml
import os

import requests
import pandas as pd
import json
import csv

file_path = "data/all.csv"

f = open("../settings.yml", "r+")
settings = yaml.load(f)
f.close()

f = open(file_path, 'r')

reader = csv.reader(f)

endpoint = settings["api_url"]

count = 0

omeka_id_col = -1

fields = {}

fo = open(file_path+".sql", 'w')

for row in reader:

    if count == 0:
        for i in range(len(row)):
            term = row[i]

            if term == "OmekaID":
                omeka_id_col = i

            url = endpoint + "/properties?term=" + term

            r = requests.get(url)
            data = json.loads(r.content)

            if len(data) == 1:
                print(term)
                fields[i] = data[0]["o:id"]
    else:
        for i in fields:
            field_id = str(fields[i])
            value = row[i]
            oid = str(row[omeka_id_col])

            if value != "":
                sql = "delete from `value` where `resource_id` = '"+oid+"' and `property_id` = '"+field_id+"';\n"
                fo.write(sql)
                if value.startswith("http"):
                    sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`, `is_public`) VALUES ('0', '"+oid+"', '"+field_id+"', NULL, 'uri', NULL, NULL, '"+str(value)+"', '1');\n"
                else:
                    sql = "INSERT INTO `value` (`id`, `resource_id`, `property_id`, `value_resource_id`, `type`, `lang`, `value`, `uri`, `is_public`) VALUES ('0', '"+oid+"', '"+field_id+"', NULL, 'literal', NULL, '"+str(value)+"', NULL, '1');\n"
                fo.write(sql)
    count += 1

fo.close()
