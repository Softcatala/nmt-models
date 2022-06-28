#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

from bs4 import BeautifulSoup
import requests
import os
import shutil
import re
import json
from urllib.request import Request, urlopen
from urllib.parse import urlparse


URL = 'https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/'
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

# To address a bug introduced in June 2022 training
# can be removed after
buggy_segment = {}

def get_segments(language_pair):
    try:
        source_language = language_pair[0:3]
        target_language = language_pair[4:]
        filename = f"{language_pair}/metadata/inputs_used.txt"
        with open(filename) as f:
            line = f.readline()
            idx = line.find(" ")
            value = int(line[0:idx])

            if source_language != "cat":
                buggy_segment[target_language] = value
            return value
    except:
        if source_language in buggy_segment:
            return buggy_segment[source_language]

        return 0
    
def get_bleu_scores(language_pair):
    bleu_model = 0
    bleu_flores = 0

    try:
        filename = f"{language_pair}/metadata/model_description.txt"
        BLEU_REGEX_SACRE = "BLEU([^=]*)=[ ]([0-9\.]*)"
        with open(filename) as f:
            lines = f.readlines()

            m = re.match(BLEU_REGEX_SACRE, lines[4])
            bleu_model = m[2]

            m = re.match(BLEU_REGEX_SACRE, lines[6])
            bleu_flores = m[2]

            return bleu_model, bleu_flores

    except:
        return bleu_model, bleu_flores

def load_mt_scores(filename):

    with open(filename, 'r') as openfile:
        return json.load(openfile)

opus_mt_scores = load_mt_scores('evaluate/opusmt-bleu.json')
google_scores = load_mt_scores('evaluate/google-bleu.json')

def get_opus_mt(language_pair):

    bleu = opus_mt_scores[language_pair]
    return bleu

def get_google(language_pair):

    bleu = google_scores[language_pair]
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

def get_metrics_from_model_zipfile(url, language_pair):
    ZIP_FILE = "model.zip"
    DIR = "tmp/"

    if os.path.isdir(DIR):
        shutil.rmtree(DIR)

    os.mkdir(DIR)
    os.chdir(DIR)

    download_file(url, ZIP_FILE)

    cmd = 'unzip {0} > /dev/null'.format(ZIP_FILE)
    os.system(cmd)

    segments = get_segments(language_pair)
    if segments > 0:
        segments = (int) (segments / 2) # Segments are duplicated upper case, lower case

    bleu_model, bleu_flores = get_bleu_scores(language_pair)

    return segments, bleu_model, bleu_flores

def main():
    print("Builds a table with available models")

    with open("table.md", "w") as table_md, open("table.csv", "w") as table_cvs:
        head = "Language pair | Model BLEU | Flores101 BLEU | Google BLEU | Opus-MT BLEU | Sentences | Download model"
        table_md.write(f"{head}\n")
        table_cvs.write("{0}\n".format(head.replace("|",",")))
        table_md.write("|---|---|---|---|---|---|---\n")
        models = get_list_of_models(URL, EXT)
        models = get_sorted_models(models)
        for url in models:
                         
            language_pair = get_language_pair(url)
            segments, bleu_model, bleu_flores = get_metrics_from_model_zipfile(url, language_pair)
            language_names = convert_iso_639_3_to_string(language_pair)
            print("")
            print(f"model '{url}'")
            print(f"language pair '{language_pair}' ('{language_names}')")
            print(f"segments '{segments}'")
            print(f"bleu model '{bleu_model}'")
            print(f"bleu flores '{bleu_flores}'")
            
            opus_mt = get_opus_mt(language_pair)
            print(f"opus mt '{opus_mt}'")
            
            google = get_google(language_pair)
            print(f"Google '{google}'")
            filename = get_filename(url)
            entry = f"{language_names} | {bleu_model} |{bleu_flores} |{google} |{opus_mt}| {segments} | [{filename}]({url})"
            table_md.write(f"|{entry}\n")
            table_cvs.write("{0}\n".format(entry.replace("|",",")))

if __name__ == "__main__":
    main()
