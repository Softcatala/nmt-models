#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

import os
from remotemodels import RemoteModels


def main():
    models = RemoteModels().get_list_of_models()
    for model_url in models:
        for language_pair in [
            "eng-cat",
            "cat-eng",
            "deu-cat",
            "cat-deu",
            "fra-cat",
            "cat-fra",
            "spa-cat",
            "cat-spa",
            "eus-cat",
            "cat-eus",
            "nld-cat",
            "cat-nld",
            "ita-cat",
            "cat-ita",
            "glg-cat",
            "cat-glg",
            "jpn-cat",
            "cat-jpn",
            "oci-cat",
            "cat-oci",
        ]:

            if language_pair in model_url:
                print(f"model: {model_url}")
                PATH = f"translate-{language_pair}"
                GIT_URL = f"https://huggingface.co/softcatala/{PATH}"
                if os.path.exists(PATH):
                    cmd = f"cd {PATH} && git pull && cd .."
                else:
                    cmd = f"git clone {GIT_URL}"
                os.system(cmd)

                ZIP_FILE = os.path.join(PATH, "model.zip")
                RemoteModels().download_file(model_url, ZIP_FILE)

                for subdir in ["ctranslate2", "tokenizer", "metadata"]:
                    files = "model_description.txt" if subdir == "metadata" else "*"
                    cmd = f'unzip -d {PATH} -o -j {ZIP_FILE} "{language_pair}/{subdir}/{files}"'
                    os.system(cmd)

                os.remove(ZIP_FILE)


if __name__ == "__main__":
    main()
