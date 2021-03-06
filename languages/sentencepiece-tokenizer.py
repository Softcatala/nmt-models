#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Jordi Mas i Hernandez <jmas@softcatala.org>
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

import pyonmttok
from optparse import OptionParser
from shutil import copyfile

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-v',
        '--vocabulary-size',
        type='int',
        action='store',
        default='32000',
        dest='vocabulary_size',
        help='Size of the vocabulary'
    )

    parser.add_option(
        '-l',
        '--language_pair',
        type='string',
        action='store',
        default='',
        dest='language_pair',
        help="Language pair for flores dataset"
    )

    (options, args) = parser.parse_args()
    return options.vocabulary_size, options.language_pair

def _get_file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def ingest_file(learner, ingest_file):
    MAX_LINES = 1000000

    file_len = _get_file_len(ingest_file)

    if file_len < MAX_LINES:
        return learner.ingest_file(ingest_file)

    percentage = MAX_LINES / file_len * 100
    print(f"Ingesting only {percentage:.2f}% of {ingest_file}")

    cnt = 0
    reduced_file = ingest_file + "-reduced.txt"
    with open(ingest_file, "r") as source,\
         open(reduced_file, "w") as target:

        while True:
            src = source.readline()
            if not src:
                break

            cnt = cnt + 1

            if cnt > 100:
                cnt = 0

            if cnt > percentage:
                continue

            target.write(src)

    return learner.ingest_file(reduced_file)

def src(vocabulary_size, model, language_pair):
    learner = pyonmttok.SentencePieceLearner(vocab_size=vocabulary_size,
                                            keep_vocab = True)
    ingest_file(learner, "src-train.txt")
    ingest_file(learner, "tgt-train.txt")

    tokenizer = learner.learn(model, verbose=True)
    tokens = tokenizer.tokenize_file("src-train.txt", "src-train.txt.token")
    tokens = tokenizer.tokenize_file("src-test.txt", "src-test.txt.token")
    tokens = tokenizer.tokenize_file("src-val.txt", "src-val.txt.token")

    tokens = tokenizer.tokenize_file("tgt-train.txt", "tgt-train.txt.token")
    tokens = tokenizer.tokenize_file("tgt-test.txt", "tgt-test.txt.token")
    tokens = tokenizer.tokenize_file("tgt-val.txt", "tgt-val.txt.token")

    source_language, target_language = language_pair.split("-")
    flores_src = f"flores101.{source_language}"
    flores_tgt = f"flores101.{target_language}"
    
    tokens = tokenizer.tokenize_file(flores_src, flores_src + ".token")
    tokens = tokenizer.tokenize_file(flores_tgt, flores_tgt + ".token")


def main():

    print("Creates tokenized output corpus using SentencePiece")
    vocabulary_size, language_pair = read_parameters()
    model_name = 'sp_m'
    print("Vocabulary size {0}".format(vocabulary_size))

    src(vocabulary_size, model_name, language_pair)

if __name__ == "__main__":
    main()
