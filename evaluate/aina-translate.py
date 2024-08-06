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
    print(cmd)
    with open(JSON_FILE) as f:
        data = json.load(f)

    return f"{data['score']:0.1f}"

def save_json(scores):
	with open("mt-aina-bleu.json", "w") as outfile:
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
    print("Translates flores200 datasets using HuggingFace Aina models")

    pair_languages = {
        "eng-cat" : ["en", "ca"],
        "cat-eng" : ["ca", "en"],
        "deu-cat" : ["de", "ca"],
        "cat-deu" : ["ca", "de"],
    }

    blue_scores = {}
 
    for pair_language in pair_languages:
        source_language_two_digits = pair_languages[pair_language][0]
        target_language_two_digits = pair_languages[pair_language][1]
        source_language_three_digits, target_language_three_digits = pair_language.split("-")

        model_name = f"aina-translator-{source_language_two_digits}-{target_language_two_digits}"

        hypotesis_file = f"mt-aina/flores200-{model_name}.{target_language_three_digits}"
        print(hypotesis_file)
        input_file = f"flores200.{source_language_three_digits}"
        hf_path = f"projecte-aina/{model_name}"
        model_dir = snapshot_download(repo_id=hf_path, revision="main")
        tokenizer=pyonmttok.Tokenizer(mode="none", sp_model_path = model_dir + "/spm.model")
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
                    

        reference_file = f"flores200.{target_language_three_digits}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file)
        blue_scores[f'{source_language_three_digits}-{target_language_three_digits}'] = sacrebleu
        print(f"'{source_language_three_digits}-{target_language_three_digits}', BLEU: '{sacrebleu}'")
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)
    save_json(blue_scores)

if __name__ == "__main__":
    main()
