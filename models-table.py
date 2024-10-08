#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

import os
import shutil
import re
import json
from urllib.parse import urlparse
from remotemodels import RemoteModels


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
        BLEU_REGEX_SACRE = "([ ]*)?BLEU([^=]*)=[ ]([0-9\.]*)"
        with open(filename) as f:
            lines = f.readlines()

            m = re.match(BLEU_REGEX_SACRE, lines[4])
            bleu_model = m[3]

            m = re.match(BLEU_REGEX_SACRE, lines[7])
            bleu_flores = m[3]

            return bleu_model, bleu_flores

    except Exception as e:
        print(f"Error: {e}")
        return bleu_model, bleu_flores

def load_mt_scores(filename):

    with open(filename, 'r') as openfile:
        return json.load(openfile)

opus_mt_scores = load_mt_scores('evaluate/opusmt-bleu.json')
google_scores = load_mt_scores('evaluate/google-bleu.json')
meta_scores = load_mt_scores('evaluate/meta-bleu.json')

def get_blue_score(language_pair, scores):

    bleu = scores.get(language_pair)
    if not bleu:
        bleu = "N/A"

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
        "por" : "Portuguese",
        "jpn" : "Japanese",
        "glg" : "Galician",
        "oci" : "Occitan",
        "eus" : "Basque",
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

    RemoteModels().download_file(url, ZIP_FILE)

    cmd = 'unzip {0} > /dev/null'.format(ZIP_FILE)
    os.system(cmd)

    segments = get_segments(language_pair)
    if segments > 0:
        segments = (int) (segments / 2) # Segments are duplicated upper case, lower case

    bleu_model, bleu_flores = get_bleu_scores(language_pair)

    return segments, bleu_model, bleu_flores

def main():
    print("Builds a table with available models")

    cnt_models = 0
    with open("table.md", "w") as table_md, open("table.csv", "w") as table_cvs:
        head = "Language pair | SC model BLEU | SC Flores200 BLEU | Google BLEU | Meta NLLB200 BLEU | Opus-MT BLEU | Sentences | Download model"
        table_md.write(f"{head}\n")
        table_cvs.write("{0}\n".format(head.replace("|",",")))
        table_md.write("|---|---|---|---|---|---|---|---\n")
        models = RemoteModels().get_list_of_models()
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
            
            opus_mt = get_blue_score(language_pair, opus_mt_scores)
            print(f"opus mt '{opus_mt}'")
            meta_mt = get_blue_score(language_pair, meta_scores)
            print(f"meta '{meta_mt}'")
            google = get_blue_score(language_pair, google_scores)
            print(f"Google '{google}'")

            filename = get_filename(url)
            entry = f"{language_names} | {bleu_model} |{bleu_flores} |{google} |{meta_mt}|{opus_mt}| {segments} | [{filename}]({url})"
            table_md.write(f"|{entry}\n")
            table_cvs.write("{0}\n".format(entry.replace("|",",")))
            cnt_models +=1

    print(f"\nProcessed {cnt_models} models")


if __name__ == "__main__":
    main()
