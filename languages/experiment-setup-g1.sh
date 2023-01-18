#!/bin/bash
export QUICK_PREPROCESSING=1

# 1. ./preprocess.sh has been run before over spa-cat once
# 2. https://huggingface.co/datasets/jordimas/spa-cat/tree/main expected


echo Copying files
cp -r spa-cat spa-cat-e1 # Calculated base line
cp -r spa-cat spa-cat-e2 # Plus All DOGC 
cp -r spa-cat spa-cat-e3 # Paracrawl (alone) 


echo Setup experiments e1
cd spa-cat-e1
./preprocess.sh
cd ..

echo Setup experiment e2
cd spa-cat-e2
cp corpus-e2.yml corpus.yml
./preprocess.sh
cd ..

echo Setup experiment e3
cd spa-cat-e3
cp ../../../spa-cat/paracrawl.es-ca.* corpus-raw/
cp corpus-e3.yml corpus.yml 
./preprocess.sh
cd ..


echo "Setup finished"
