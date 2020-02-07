import sys
import urllib
import json
import argparse
import urllib.request
import os
import glob
import yaml

prefix = "https://iii-dch.github.io/dataset"

f = open("settings.yml", "r+")
settings = yaml.load(f)

# ldファイルを使う
files = glob.glob("../docs/ld/*.json")
api_url = "https://dch.iii.u-tokyo.ac.jp/api"

collection_uri = prefix + "/iiif/collection.json"

output_path = "../docs/iiif/collection.json"

manifest_path = "../docs/iiif/item"

manifest_uri_prefix = prefix +  "/iiif/item"

collection = dict()
collection["@context"] = "http://iiif.io/api/presentation/2/context.json"
collection["@id"] = collection_uri
collection["@type"] = "sc:Collection"
manifests = []
collection["manifests"] = manifests

for i in range(len(files)):
    if i % 100 == 0:
        print(str(i+1)+"/" + str(len(files)))
    file = files[i]
    with open(file) as f:
        obj = json.load(f)

        id = obj["o:id"]
        if settings["identifier"] in obj:
            id = obj[settings["identifier"]][0]["@value"]

        manifest_uri = api_url.replace(
            "/api", "/iiif") + "/" + str(id) + "/manifest"

        new_manifest_uri = manifest_uri_prefix + \
            "/" + id + "/manifest.json"

        manifest = dict()
        manifests.append(manifest)
        manifest["@id"] = new_manifest_uri
        manifest["@type"] = "sc:Manifest"
        manifest["label"] = obj["dcterms:title"][0]["@value"]

        if "dcterms:rights" in obj:
            manifest["license"] = obj["dcterms:rights"][0]["@id"]

        res = urllib.request.urlopen(manifest_uri)
        # json_loads() でPythonオブジェクトに変換
        manifest_json = json.loads(res.read().decode('utf-8'))

        manifest["metadata"] = manifest_json["metadata"]

        if "@id" in manifest_json["sequences"][0]["canvases"][0]["thumbnail"]:
            manifest["thumbnail"] = manifest_json["sequences"][0]["canvases"][0]["thumbnail"]["@id"]
        else:
            manifest_json["sequences"][0]["canvases"] = []

        manifest_json["@id"] = new_manifest_uri
        manifest_json["seeAlso"] = prefix + "/ld/"+id+".json"

        manifest_dir = manifest_path+"/"+id
        os.makedirs(manifest_dir, exist_ok=True)

        with open(manifest_dir+"/manifest.json", 'w') as outfile:
            json.dump(manifest_json, outfile, ensure_ascii=False,
                      indent=4, sort_keys=True, separators=(',', ': '))

fw = open(output_path, 'w')
json.dump(collection, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
