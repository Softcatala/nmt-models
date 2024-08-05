#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

class RemoteModels:
    URL = "https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/"
    EXT = "zip"

    @staticmethod
    def get_list_of_models(url=URL, ext=EXT):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        return [
            url + node.get("href")
            for node in soup.find_all("a")
            if node.get("href").endswith(ext)
        ]

    @staticmethod
    def download_file(url, filename):
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        infile = urlopen(req)
        output = open(filename, "wb")
        output.write(infile.read())
        output.close()
        print(f"Downloaded {url}")