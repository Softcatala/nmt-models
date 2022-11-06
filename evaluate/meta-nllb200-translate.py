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
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import datetime
import json

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
	with open("meta-bleu.json", "w") as outfile:
		json.dump(scores, outfile, indent=4)


def main():
    print("Translates Flores101 datasets using HuggingFace Facebook nllb200 models")

    pair_languages = {
        "de-ca" : ["deu", "cat"],
        "ca-de" : ["cat", "deu"],

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

        "pt-ca" : ["por", "cat"],
        "ca-pt" : ["cat", "por"],

        "gl-ca" : ["glg", "cat"],
        "ca-gl" : ["cat", "glg"],
    }

    blue_scores = {}

#    model_name = f'nllb-200-distilled-600M'
    model_name = f'nllb-200-3.3B'
                
    tokenizer = AutoTokenizer.from_pretrained(f"facebook/{model_name}")
    model = AutoModelForSeq2SeqLM.from_pretrained(f"facebook/{model_name}")
    print(f"Model name: {model_name}")
    
    for pair_language in pair_languages:
        source_language = pair_languages[pair_language][0]
        target_language = pair_languages[pair_language][1]
#        print(f"source_language: {source_language}")
#        print(f"target_language: {target_language}")
        
        hypotesis_file = f"meta-nllb-200/flores101-{model_name}-{source_language}-{target_language}.{target_language}"
        input_file = f"flores101.{source_language}"

#        print(f"hypo {hypotesis_file}")
#        print(f"input_file {input_file}")

        start_time = datetime.datetime.now()
        LINES_IN_DATA_SET = 1012
        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            cnt = 0
            translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=f'{source_language}' + "_Latn", tgt_lang=f'{target_language}' + "_Latn", max_length=400)
            with open(input_file, "r") as source, open(hypotesis_file, "w") as target:

                while True:
                    src = source.readline()

                    if not src:
                        break

                    translated = translator(src)
#                    print(translated)
                    t = translated[0]['translation_text']
                    target.write(t + "\n")
                    cnt += 1
                    if cnt % 100 == 0:
                        print(cnt)
                    

        reference_file = f"flores101.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file)
        blue_scores[f'{source_language}-{target_language}'] = sacrebleu
        print(f"'{source_language}-{target_language}', BLEU: '{sacrebleu}'")
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)
    save_json(blue_scores)

if __name__ == "__main__":
    main()
