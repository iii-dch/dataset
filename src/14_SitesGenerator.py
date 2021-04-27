import sys
import urllib
import json
import argparse
import urllib.request
import os
import yaml
import shutil

dir = "../docs/api/sites"
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)

def properties_generator():

    
    f = open("settings.yml", "r+")
    data = yaml.load(f)

    api_url = data["api_url"]

    loop_flg = True
    page = 1

    query = ""
    if "key_identity" in data:
        query += "&key_identity=" + data["key_identity"] + "&key_credential=" + data["key_credential"]

    while loop_flg:
        url = api_url + "/sites?page=" + str(
            page) + query
        print(url)

        page += 1

        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                oid = str(obj["o:id"])

                with open(dir+"/"+oid+".json", 'w') as outfile:
                    json.dump(obj, outfile, ensure_ascii=False,
                              indent=4, sort_keys=True, separators=(',', ': '))

        else:
            loop_flg = False


if __name__ == "__main__":
    properties_generator()
