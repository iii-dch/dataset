import sys
import urllib
import json
import argparse
import requests
import os
import shutil
import yaml

f = open("settings.yml", "r+")
settings = yaml.load(f)

dir = "../docs/ld"
if os.path.exists(dir):
    shutil.rmtree(dir)
os.makedirs(dir, exist_ok=True)

uri_prefix = "https://iii-dch.github.io/dataset/ld"

def base_generator():
    api_url = "https://dch.iii.u-tokyo.ac.jp/api"

    loop_flg = True
    page = 1

    while loop_flg:
        url = api_url + "/items?page=" + str(
            page)
        print(url)

        page += 1

        headers = {"content-type": "application/json"}
        r = requests.get(url, headers=headers)
        data = r.json()

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                id = str(obj["o:id"])
                if settings["identifier"] in obj:
                    id = obj[settings["identifier"]][0]["@value"]

                uri = uri_prefix + "/" + id + ".json"

                obj["@id"] = uri

                with open(dir+"/"+id+".json", 'w') as outfile:
                    json.dump(obj, outfile, ensure_ascii=False,
                              indent=4, sort_keys=True, separators=(',', ': '))

        else:
            loop_flg = False


if __name__ == "__main__":

    base_generator()
