#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 Jordi Mas i Hernandez <jmas@softcatala.org>
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

def file_len(fname):
    if not os.path.isfile(fname):
        return 0

    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass

    return i + 1

def get_sacrebleu(reference_file, hypotesis_file, target_language):
    JSON_FILE = "bleu.json"
    tokenizer = ""

    if target_language == "jpn":
        tokenizer = "--tokenize ja-mecab"

    cmd = f"sacrebleu {tokenizer} {reference_file}  -i {hypotesis_file} -m bleu > {JSON_FILE}"
    os.system(cmd)
    with open(JSON_FILE) as f:
        data = json.load(f)

    return f"{data['score']:0.1f}"

def save_json(scores):
	with open("sc-translate-bleu.json", "w") as outfile:
		json.dump(scores, outfile, indent=4)

import ctranslate2
import pyonmttok
from huggingface_hub import snapshot_download


def _translate(tokenizer, translator, src):
    tokenized=tokenizer.tokenize(src)

    translated = translator.translate_batch([tokenized[0]])
    translated = tokenizer.detokenize(translated[0][0]['tokens'])
    return translated
    
def main():
    print("Translates flores200 datasets using HuggingFace Softcatalà models")

    pair_languages = [
        "cat-eng",
    ]

    blue_scores = {}
 
    for pair_language in pair_languages:
        source_language, target_language = pair_language.split("-")
        model_name = f"translate-{pair_language}"

        hypotesis_file = f"sc-translate/sc-flores200-{model_name}.{target_language}"
        print(hypotesis_file)
        input_file = f"flores200.{source_language}"

        model_dir = snapshot_download(repo_id=f"softcatala/{model_name}", revision="main")
        tokenizer=pyonmttok.Tokenizer(mode="none", sp_model_path = model_dir + "/sp_m.model")
        translator = ctranslate2.Translator(model_dir)

        start_time = datetime.datetime.now()
        LINES_IN_DATA_SET = 1012
        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            cnt = 0
            with open(input_file, "r") as source, open(hypotesis_file, "w") as target:

                while True:
                    src = source.readline()

                    if not src:
                        break
                    
                    t = _translate(tokenizer, translator, src)
          #          print(t)
                    target.write(t + "\n")
                    cnt += 1
                    if cnt % 100 == 0:
                        print(cnt)
                    

        reference_file = f"flores200.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file, target_language)
        blue_scores[f'{source_language}-{target_language}'] = sacrebleu
        print(f"'{source_language}-{target_language}', BLEU: '{sacrebleu}'")
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)
    save_json(blue_scores)

if __name__ == "__main__":
    main()
