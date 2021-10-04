#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
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
from transformers import MarianMTModel, MarianTokenizer
import json

def file_len(fname):
    if not os.path.isfile(fname):
        return 0

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

    return data['score']


def main():
    print("Translates Flores101 datasets using HuggingFace opus-mt models")

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
    }

    for pair_language in pair_languages:
        source_language = pair_languages[pair_language][0]
        target_language = pair_languages[pair_language][1]
#        print(f"source_language: {source_language}")
#        print(f"target_language: {target_language}")

        model_name = f'Helsinki-NLP/opus-mt-{pair_language}'
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        hypotesis_file = f"translated/flores101-{pair_language}.{target_language}"
        input_file = f"flores101.{source_language}"

#        print(f"hypo {hypotesis_file}")
#        print(f"input_file {input_file}")

        LINES_IN_DATA_SET = 1012
        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            with open(input_file, "r") as source, open(hypotesis_file, "w") as target:

                while True:
                    src = source.readline()

                    if not src:
                        break

                    translated = model.generate(**tokenizer(src, return_tensors="pt", padding=True))
                    t = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
                    t = str(t[0])
                    target.write(t + "\n")

        reference_file = f"flores101.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file)
        print(f"'{source_language}-{target_language}' : '{sacrebleu:0.2f}',")

if __name__ == "__main__":
    main()
