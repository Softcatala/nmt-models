#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

from bs4 import BeautifulSoup
import requests
import os
import shutil
import re
from urllib.request import Request, urlopen
from urllib.parse import urlparse


URL = 'https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/'
EXT = 'zip'

def get_list_of_models(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


def download_file(url, filename):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    infile = urlopen(req)
    output = open(filename, 'wb')
    output.write(infile.read())
    output.close()
#    print(f"Downloaded {url}")

def get_language_pair(url):
    a = urlparse(url)
    filename = os.path.basename(a.path)
    return filename[0:7]

def get_filename(url):
    a = urlparse(url)
    return os.path.basename(a.path)


def get_segments():
    try:
        filename = "metadata/inputs_used.txt"
        with open(filename) as f:
            line = f.readline()
            idx = line.find(" ")
            return int(line[0:idx])
    except:
        return 0
    
def get_bleu_scores():
    bleu_model = 0
    bleu_flores = 0

    try:
        filename = "metadata/model_description.txt"
        BLEU_REGEX_SACRE = "BLEU([^=]*)=[ ]([0-9\.]*)"
        with open(filename) as f:
            lines = f.readlines()

            m = re.match(BLEU_REGEX_SACRE, lines[3])
            bleu_model = m[2]

            m = re.match(BLEU_REGEX_SACRE, lines[6])
            bleu_flores = m[2]

            return bleu_model, bleu_flores

    except:
        return bleu_model, bleu_flores

def get_opus_mt(language_pair):

    languages = {
        'fra-cat' : '27.20',
        'cat-fra' : '27.90',
        'spa-cat' : '22.50',
        'cat-spa' : '23.20',
        'ita-cat' : '22.00',
        'cat-ita' : '19.20',
        'nld-cat' : '15.80',
        'cat-nld' : '13.40',
        'eng-cat' : '29.80',
        'cat-eng' : '29.60',
        'deu-cat' : '18.50',
        'cat-deu' : '15.80',
        'por-cat' : '28.10',
        'cat-por' : '27.50'
    }

    bleu = languages[language_pair]
    return bleu

def convert_iso_639_3_to_string(language_pair):
    languages = {
        "eng" : "English",
        "spa" : "Spanish",
        "fra" : "French",
        "cat" : "Catalan",
        "deu" : "German",
        "ita" : "Italian",
        "nld" : "Dutch",
        "por" : "Portuguese"
    }

    for iso in languages.keys():
        language_pair = language_pair.replace(iso, languages[iso])

    return language_pair

# Make sure that related parts (e.g. eng-cat & cat-eng are shown together)
def get_sorted_models(urls):
    new_list = []
    from_cat = []
    to_cat = []

    for url in urls:
        language_pair = get_language_pair(url)
        if language_pair[0:3].lower() == "cat":
            from_cat.append(url)
        else:
            to_cat.append(url)

    to_cat.sort()

    current_item = 0
    while len(to_cat) > 0:
        language_pair = get_language_pair(to_cat[current_item])
        opossite_pair = language_pair[4:7] + "-" + language_pair[0:3]

        found = -1
        for i in range(0, len(from_cat)):
            if opossite_pair in from_cat[i]:
                found = i

        item1 = to_cat[current_item]
        new_list.append(item1)

        if found >= 0:
            item2 = from_cat[found]
            new_list.append(item2)
            from_cat.remove(item2)

        to_cat.remove(item1)

    return new_list

def main():
    print("Builds a table with available models")

    ZIP_FILE = "model.zip"
    DIR = "tmp/"

    with open("table.md", "w") as table:
        table.write("Language pair | Model BLEU | Flores101 BLEU | Opus-MT BLEU | Sentences | Download model\n")
        table.write("|---|---|---|---|---|---\n")
        models = get_list_of_models(URL, EXT)
        models = get_sorted_models(models)
        for url in models:
            
            if os.path.isdir(DIR):
                shutil.rmtree(DIR)

            os.mkdir(DIR)
            os.chdir(DIR)

            download_file(url, ZIP_FILE)

            cmd = 'unzip {0} > /dev/null'.format(ZIP_FILE)
            os.system(cmd)
            
            language_pair = get_language_pair(url)
            language_names = convert_iso_639_3_to_string(language_pair)
            print("")
            print(f"model '{url}'")
            print(f"language pair '{language_pair}' ('{language_names}')")
            segments = get_segments()
            if segments > 0:
                segments = (int) (segments / 2) # Segments are duplicated upper case, lower case
 
            print(f"segments '{segments}'")
            bleu_model, bleu_flores = get_bleu_scores()
            print(f"bleu model '{bleu_model}'")
            print(f"bleu flores '{bleu_flores}'")
            opus_mt = get_opus_mt((language_pair))
            print(f"opus mt '{opus_mt}'")
            
            filename = get_filename(url)
            table.write(f"|{language_names} | {bleu_model} |{bleu_flores} |{opus_mt} | {segments} | [{filename}]({url})\n")

if __name__ == "__main__":
    main()