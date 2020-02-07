import sys
import csv
import urllib.request, json
import argparse
import yaml
import os


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'output_path',
        action='store',
        type=str,
        help='Ful path to output csv file.')

    parser.add_argument(
        'item_set',
        action='store',
        type=str,
        help='item set id.')

    return parser.parse_args(args)


def get_thumbnail(manifest_iri):
    try:
        response = urllib.request.urlopen(manifest_iri)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body)

        return data["sequences"][0]["canvases"][0]["thumbnail"]["@id"]
    except:
        return ""


def main(output_path, item_set):
    f = open("../settings.yml", "r+")
    settings = yaml.load(f)

    api_url = settings["api_url"]
    identifier = settings["identifier"]

    flg = True
    page = 1

    fo = open(output_path, 'w')
    writer = csv.writer(fo, lineterminator='\n')
    writer.writerow(
        [identifier, "dcterms:title", "OmekaID", "dcterms:relation", "uterms:manifestUri", "rdfs:seeAlso",
         "foaf:thumbnail"])

    while flg:

        if item_set == "all":
            item_set = ""

        url = api_url + "/items?item_set_id=" + item_set + "&page=" + str(page)
        print(url)

        page += 1

        response = urllib.request.urlopen(url)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body.split('\n')[0])

        if len(data) > 0:
            for i in range(len(data)):
                obj = data[i]

                id = ""

                if identifier in obj:
                    id = obj[identifier][0]["@value"]

                omeka_id = obj["o:id"]

                title = ""
                if "dcterms:title" in obj:
                    title = obj["dcterms:title"][0]["@value"]

                see_also = api_url + "/items/" + str(omeka_id)

                manifest_uri = ""
                thumbnail_url = ""

                tmp_id = (str(omeka_id) if id == "" else str(id))
                relation = settings["base_url"] + "/" + tmp_id

                if len(obj["o:media"]) > 0:
                    manifest_uri = api_url.replace("/api", "/iiif") + "/" + tmp_id + "/manifest"
                    thumbnail_url = get_thumbnail(manifest_uri)

                writer.writerow([id, title, omeka_id, relation, manifest_uri, see_also, thumbnail_url])

        else:
            flg = False

    fo.close()

    print("output_path:\t" + output_path)


if __name__ == "__main__":
    args = parse_args()

    main(args.output_path, args.item_set)
