#!/bin/bash
export QUICK_PREPROCESSING=1

# 1. ./preprocess.sh has been run before over spa-cat once
# 2. https://huggingface.co/datasets/jordimas/spa-cat/tree/main expected

cp -r spa-cat spa-cat-e4


echo Setup experiment e4
cd spa-cat-e4
cp ../../../spa-cat/paracrawl.es-ca.* corpus-raw/
cp corpus-e4.yml corpus.yml 
./preprocess.sh
cd ..


echo "Setup finished"
