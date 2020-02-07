import sys
import urllib
import json
import argparse
import urllib.request
import os
import yaml

dir = "../docs/item_sets"
os.makedirs(dir, exist_ok=True)

def item_sets_generator():
    f = open("config.yml", "r+")
    data = yaml.load(f)

    api_url = data["api_url"]

    loop_flg = True
    page = 1

    while loop_flg:
        url = api_url + "/item_sets?page=" + str(
            page)
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
    item_sets_generator()
