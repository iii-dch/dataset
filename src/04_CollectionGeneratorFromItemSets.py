import sys
import json
import argparse
import requests
import os
import glob
import yaml
import shutil
import datetime

from classes.downloader import Downloader

manifest_path = "../docs/iiif/collection"
Downloader.initDir(manifest_path)

f = open("settings.yml", "r+")
settings = yaml.load(f)

prefix = settings["github_pages_url"]

# ldファイルを使う
files = glob.glob("../docs/api/item_sets/*.json")
api_url = settings["api_url"]


for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1)+"/" + str(len(files)))
    file = files[i]
    with open(file) as f:
        obj = json.load(f)


        id = str(obj["o:id"])

        url = api_url.replace(
            "/api", "/iiif") + "/collection/" + id

        collection = requests.get(url).json()

        '''
        manifest_uri = api_url.replace(
            "/api", "/iiif") + "/" + str(id) + "/manifest"

        # 画像なし
        if len(obj["o:media"]) == 0:
            continue

        new_manifest_uri = manifest_uri_prefix + \
            "/" + id + "/manifest.json"
        

        medias = obj["o:media"]

        canvases = []

        metadata = []

        for key in obj:
            if ":" in key and "o:" not in key:
                values = obj[key]
                for value in values:

                    metadata.append({
                        "label" : value["property_label"],
                        "value" : value["@id"] if "@id" in value else value["@value"],
                        "term" : key
                    })

        thumbnail = None

        for j in range(len(medias)):

            mid = medias[j]["@id"]

            mpath = "../docs/api/media/" + mid.split("/")[-1]+".json"

            with open(mpath) as f:
                mdata = json.load(f)
            
            url = mdata["o:source"]

            h = 1
            w = 1

            index = str(j+1)

            canvas =  {
                "@id": manifest_uri_prefix +"/" + id + "/canvas/p"+index,
                "@type": "sc:Canvas",
                "height": h,
                "images": [
                    {
                        "@id": manifest_uri_prefix +"/" + id + "/annotation/p"+index.zfill(4)+"-image",
                        "@type": "oa:Annotation",
                        "motivation": "sc:painting",
                        "on": manifest_uri_prefix +"/" + id + "/canvas/p"+index,
                        "resource": {
                            "@id": url,
                            "@type": "dctypes:Image",
                            "format": "image/jpeg",
                            "height": h,
                            "width": w
                        }
                    }
                ],
                "label": "["+index+"]",
                "thumbnail": {
                    "@id": url,
                },
                "width": w
            }

            canvases.append(canvas)

            if j == 0:
                thumbnail = url
        
        
        manifest_json = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": new_manifest_uri,
            "@type": "sc:Manifest",
            "label": obj["dcterms:title"][0]["@value"],
            "metadata" : metadata,
            "thumbnail" : thumbnail,
            "attribution" : "東洋文庫 / Toyo Bunko",
            "seeAlso" : prefix + "/api/items/"+ id + ".json",
            "sequences": [
                {
                    "@id": manifest_uri_prefix +"/" + id + "/sequence/normal",
                    "@type": "sc:Sequence",
                    "canvases" : canvases
                }
            ]
        }

        if "dcterms:rights" in obj:
            manifest_json["license"] = obj["dcterms:rights"][0]["@id"]

        manifest_dir = manifest_path+"/"+id
        os.makedirs(manifest_dir, exist_ok=True)

        with open(manifest_dir+"/manifest.json", 'w') as outfile:
            json.dump(manifest_json, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))

        manifest = dict()
        manifests.append(manifest)
        manifest["@id"] = new_manifest_uri
        manifest["@type"] = "sc:Manifest"
        manifest["label"] = obj["dcterms:title"][0]["@value"]
        manifest["thumbnail"] = thumbnail
        manifest["metadata"] = metadata

        if i == 0:
            collection["thumbnail"] = thumbnail

        '''

        output_path = "../docs/iiif/collection/{}.json".format(id)

        fw = open(output_path, 'w')
        json.dump(collection, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))