import requests
import json
import os
import shutil

class Downloader:

    @classmethod
    def main(self, settings, path, page):
        api_url = settings["api_url"]

        query = ""
        if "key_identity" in settings:
            query += "&key_identity=" + settings["key_identity"] + "&key_credential=" + settings["key_credential"]

        url = api_url + "/"+path+"?page=" + str(
            page) + query

        # page += 1

        response = requests.get(url)

        # ★ポイント3    
        data = response.json()
        return data

    @classmethod
    def initDir(self, dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path, exist_ok=True)

        