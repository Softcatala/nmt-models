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
# but WITHOUT ANY WARRANTY; without even the implied warranty of
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

import ctranslate2
from transformers import AutoTokenizer
from huggingface_hub import snapshot_download


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
    with open("ct2-gemma-translate-bleu.json", "w") as outfile:
        json.dump(scores, outfile, indent=4)


def get_prompt(text, src_lang_code, tgt_lang_code):
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "source_lang_code": src_lang_code,
                    "target_lang_code": tgt_lang_code,
                    "text": text,
                }
            ],
        }
    ]

    return str(messages)


def _translate(tokenizer, generator, src, source_language, target_language):
    src = src.strip()
    prompt = get_prompt(src, source_language, target_language)
    tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(prompt))

    result = generator.generate_batch(
        [tokens],
        max_length=2048,
        sampling_temperature=0.1,
        sampling_topk=1,
        sampling_topp=0.1,
        include_prompt_in_result=False,
    )

    translated = tokenizer.convert_tokens_to_string(result[0].sequences[0])
    return translated.strip()


def main():
    print("Translates flores200 datasets using ctranslate2 Gemma translate models")

    pair_languages = [
        "eng-cat",
    ]

    # Language code to full name mapping for prompts
    language_names = {
        "cat": "Catalan",
        "eng": "English",
        "spa": "Spanish",
        "fra": "French",
        "deu": "German",
        "jpn": "Japanese",
    }

    # Model configuration
    model_path = "translategemma_4b_it.ct2"  # Path to converted ctranslate2 model
    tokenizer_name = "google/translategemma-4b-it"

    blue_scores = {}

    for pair_language in pair_languages:
        source_language, target_language = pair_language.split("-")

        source_lang_name = language_names.get(source_language, source_language)
        target_lang_name = language_names.get(target_language, target_language)

        model_name = f"translate-{pair_language}"
        hypotesis_file = (
            f"ct2-gemma-translate/sc-flores200-{model_name}.{target_language}"
        )
        print(f"Output file: {hypotesis_file}")

        input_file = f"flores200.{source_language}"

        # Load tokenizer and generator
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        generator = ctranslate2.Generator(model_path)

        start_time = datetime.datetime.now()

        LINES_IN_DATA_SET = 1012

        if file_len(hypotesis_file) != LINES_IN_DATA_SET:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(hypotesis_file), exist_ok=True)

            cnt = 0
            with open(input_file, "r") as source, open(hypotesis_file, "w") as target:
                while True:
                    src = source.readline()
                    if not src:
                        break

                    translated = _translate(
                        tokenizer, generator, src, source_lang_name, target_lang_name
                    )
                    print(f"{cnt} - {src} - {translated}")
                    target.write(translated + "\n")
                    cnt += 1
                    if cnt % 100 == 0:
                        print(f"Processed {cnt} lines")

        reference_file = f"flores200.{target_language}"
        sacrebleu = get_sacrebleu(reference_file, hypotesis_file, target_language)
        blue_scores[f"{source_language}-{target_language}"] = sacrebleu
        print(f"'{source_language}-{target_language}', BLEU: '{sacrebleu}'")

    s = "Time used: {0}".format(datetime.datetime.now() - start_time)
    print(s)
    save_json(blue_scores)


if __name__ == "__main__":
    main()
