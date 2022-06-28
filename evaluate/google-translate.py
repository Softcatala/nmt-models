#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WAR   RANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os
import datetime
import json
import urllib
import urllib.request
from optparse import OptionParser

def file_len(fname):
    if not os.path.isfile(fname):
        return 0

    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass

    return i + 1

def get_sacrebleu(reference_file, hypotesis_file):
    JSON_FILE = 'bleu.json'

    cmd = f'sacrebleu {reference_file}  -i {hypotesis_file} -m bleu > {JSON_FILE}'
    os.system(cmd)
    with open(JSON_FILE) as f:
        data = json.load(f)

    return f"{data['score']:0.1f}"

def save_json(scores):
	with open("google-bleu.json", "w") as outfile:
		json.dump(scores, outfile, indent=4)


def _translate_text_google(text, key, pair):
   
    SERVER = "https://translation.googleapis.com/language/translate/v2"

    src_lang, tgt_lang = pair.split("-")

    url = f"{SERVER}/?key={key}&source={src_lang}&target={tgt_lang}"
    url += "&q=" + urllib.parse.quote_plus(text.encode('utf-8'))
#    print(url)
    response = urllib.request.urlopen(url)
    r = response.read().decode("utf-8")
    data = json.loads(r)
    translated = data['data']['translations'][0]
    translated = translated['translatedText']
    translated = translated.replace("&#39;", "'")
    return translated.rstrip()


def translate_google(source, target, key, pair):

    strings = 0
    with open(source, 'r') as tf_en, open(target, 'w') as tf_ca:
        en_strings = tf_en.readlines()

        cnt = 0
        for string in en_strings:
            cnt = cnt + 1
    
            try:
                translated = _translate_text_google(string, key, pair)
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

            except Exception as e:
                print(e)
                print(string)

                translated = 'Error'
                tf_ca.write("{0}\n".format(translated))
                strings = strings + 1

    print("Translated {0} strings".format(strings))
    
    
    

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-k',
        '--key',
        action='store',
        type='string',
        dest='key',
        default='',
        help='API Key to use (if applies)'
    )

    (options, args) = parser.parse_args()

    return options.key




def main():
    print("Translates Flores101 datasets using Google Translate")
    
    
    api_key = read_parameters()
    
    if len(api_key) == 0:
        print("You need to provide an Google Translate API key")
        exit()

    pair_languages = {
       
        "fr-ca" : ["fra", "cat"],
        "ca-fr" : ["cat", "fra"],

        "es-ca" : ["spa", "cat"],
        "ca-es" : ["cat", "spa"],

        "it-ca" : ["ita", "cat"],
        "ca-it" : ["cat", "ita"],

        "nl-ca" : ["nld", "cat"],
        "ca-nl" : ["cat", "nld"],

        "en-ca" : ["eng", "cat"],
        "ca-en" : ["cat", "eng"],

        "de-ca" : ["deu", "cat"],
         "ca-de" : ["cat", "deu"],

        "pt-ca" : ["por", "cat"],
        "ca-pt" : ["cat", "por"],

        "jpn-ca" : ["jpn", "cat"],
        "ca-jpn" : ["cat", "jpn"],
    }

    blue_scores = {}
    for pair_language in pair_languages:
        source_language = pair_languages[pair_language][0]
        target_language = pair_languages[pair_language][1]
#        print(f"source_language: {source_language}")
#        print(f"target_language: {target_language}")

        hypotesis_file = f"google-translate/flores101-{source_language}-{target_language}.{target_language}"
        input_file = f"flores101.{source_language}"

        print(f"hypo {hypotesis_file}")
        print(f"input_file {input_file}")

        start_time = datetime.datetime.now()
        LINES_IN_DATA_SET = 1012
        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            translate_google(input_file, hypotesis_file, api_key, f"{pair_language}")
            

        reference_file = f"flores101.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file)
        blue_scores[f'{source_language}-{target_language}'] = sacrebleu
        print(f"'{source_language}-{target_language}', BLEU: '{sacrebleu}'")
    save_json(blue_scores)
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)

if __name__ == "__main__":
    main()
