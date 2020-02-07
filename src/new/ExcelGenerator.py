import sys
import urllib
import json
import argparse
import urllib.request
import unicodedata
import pandas as pd
import collections
import os
import glob


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'site_name',
        action='store',
        type=str,
        help='Site name. ex: hyakki')

    parser.add_argument(
        'item_set_id',
        action='store',
        type=str,
        help='ID of itemSet. ex: 2')

    return parser.parse_args(args)


def excel_generator(site_name, arg_item_set_id):
    label_map = collections.OrderedDict()
    label_map["dcterms:title"] = "タイトル"

    # 共用サーバで利用する独自語彙集
    default_map = collections.OrderedDict()
    default_map["iiif viewer"] = "iiif viewer"
    default_map["bibo:identifier"] = "ID"
    default_map["dcterms:isPartOf"] = "ウェブサイトURL"
    default_map["dcterms:relation"] = "アイテムURL"
    default_map["dcterms:rights"] = "利用条件"
    default_map["foaf:thumbnail"] = "サムネイル"
    default_map["rdfs:seeAlso"] = "機械可読ドキュメント"
    default_map["sc:attributionLabel"] = "帰属"
    default_map["sc:viewingDirection"] = "viewingDirection"
    default_map["sc:viewingHint"] = "viewingHint"
    default_map["uterms:databaseLabel"] = "コレクション"
    default_map["uterms:sort"] = "ソート用項目"
    default_map["uterms:year"] = "西暦"
    default_map["uterms:manifestUri"] = "IIIFマニフェストURI"
    default_map["uterms:searchApiUri"] = "IIIF Search API URI"
    default_map["uterms:annotedManifest"] = "アノテーション付きIIIFマニフェストURI"
    default_map["uterms:linkToTapas"] = "Link to TAPAS Project"
    default_map["uterms:rtf"] = "Text with Rich Text Format"
    

    '''
    igs = ["dcterms:isPartOf", "uterms:manifestUri",
           "rdfs:seeAlso", "dcterms:isPartOf", #"foaf:thumbnail", 
           "sc:attributionLabel", "dcterms:relation"]
    '''

    # templateで規定されていない語彙集
    etc_map = collections.OrderedDict()

    table = []
    rows = []
    template_arr = []

    api_url = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api"

    # output_path = "../docs/collections/" + site_name + "/metadata/data.xlsx"
    output_path = "data/test.xlsx"

    '''
    etc_dir = "../docs/collections/" + site_name + "/etc"
    os.makedirs(etc_dir, exist_ok=True)
    etc_path = etc_dir + "/data.xlsx"
    '''

    param_item_set_arr = arg_item_set_id.split(",")

    print(param_item_set_arr)

    files = glob.glob("../data/item/*.json")

    for i in range(len(files)):
        if i % 100 == 0:
            print(str(i+1)+"/" + str(len(files)))
        file = files[i]
        with open(file) as f:
            obj = json.load(f)

            item_sets = obj["o:item_set"]
            flg = False
            for item_set in item_sets:
                if str(item_set["o:id"]) in param_item_set_arr:
                    flg = True
                    break

            if flg:
                # テンプレート情報の保存
                if obj["o:resource_template"] != None:

                    template_id = obj["o:resource_template"]["@id"]
                    if template_id not in template_arr:
                        template_arr.append(template_id)

                for key in obj:

                    if not key.startswith("o:") and key != "@type":
                        if key not in default_map and key not in etc_map and isinstance(obj[key], list):
                            if "property_label" in obj[key][0]:
                                etc_map[key] = obj[key][0]["property_label"]

                rows.append(obj)

    print(len(rows))

    # テンプレート項目の追加
    for template_id in template_arr:
        response = urllib.request.urlopen(template_id)
        response_body = response.read().decode("utf-8")
        data = json.loads(response_body)
        property_arr = data["o:resource_template_property"]
        for property in property_arr:

            property_label = property["o:alternate_label"]

            property_id = property["o:property"]["@id"]

            response = urllib.request.urlopen(property_id)
            response_body = response.read().decode("utf-8")
            data = json.loads(response_body)

            term = data["o:term"]

            if property_label:
                label_map[term] = property_label

    # 例外語彙の追加
    for key in etc_map:
        if key not in label_map:
            label_map[key] = etc_map[key]

    # 独自語彙の追加
    for key in default_map:
        if key not in label_map:
            label_map[key] = default_map[key]

    '''
    for key in igs:
        if key in label_map:
            label_map.pop(key)
    '''

    label_map["dcterms:relation"] = "アイテムURL"

    # ラベル行
    row1 = []
    table.append(row1)
    # term行
    row2 = []
    table.append(row2)

    for term in label_map:
        if term in label_map:
            row1.append(label_map[term])
            row2.append(term)
        else:
            row1.append(term)
            row2.append(term)

    media_sum = 0

    # 3行目以降
    for obj in rows:
        row = []
        table.append(row)
        for term in label_map:
            text = ""

            if term == "iiif viewer":
                text = "http://tify.sub.uni-goettingen.de/demo.html?manifest=https://archdataset.dl.itc.u-tokyo.ac.jp/manifest/" + \
                    obj["bibo:identifier"][0]["@value"]+".json"
            elif term in obj:
                values = obj[term]
                for i in range(len(values)):
                    value = values[i]
                    if "@value" in value:
                        text += value["@value"]
                    else:
                        text += value["@id"]
                    if i != len(values) - 1:
                        # 複数ある場合にはパイプでつなぐ
                        text += "|"
            row.append(unicodedata.normalize("NFKC", text))

        media_num = len(obj["o:media"])
        row.append(media_num)
        media_sum += media_num

    row1.append("# of media")
    row2.append(media_sum)

    df = pd.DataFrame(table)

    df.to_excel(output_path, index=False, header=False)
    df.to_csv(output_path.replace("xlsx", "csv"), index=False, header=False)
    df.to_csv(output_path.replace("xlsx", "tsv"),
              index=False, header=False, sep='\t')


if __name__ == "__main__":
    args = parse_args()

    site_name = args.site_name
    arg_item_set_id = args.item_set_id

    excel_generator(site_name, arg_item_set_id)
