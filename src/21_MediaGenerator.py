import json
import argparse
import yaml
from classes.downloader import Downloader 

dir = "../docs/api/media"
Downloader.initDir(dir)

def base_generator():

    f = open("settings.yml", "r+")
    settings = yaml.load(f)

    loop_flg = True
    page = 1

    while loop_flg:
        print("page\t"+str(page))
        data = Downloader.main(settings, "media" , page)

        page += 1

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

    base_generator()
