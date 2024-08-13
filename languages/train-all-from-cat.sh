#!/bin/bash

declare -a arr=("cat-eng" "cat-deu" "cat-fra" "cat-ita" "cat-spa" "cat-por" "cat-nld" "cat-jpn" "cat-glg" "cat-oci" "cat-eus")
#declare -a arr=("cat-eng")

for dirname in "${arr[@]}"; do

    echo Processing $dirname

    src_lang="${dirname%-*}"  # Extract everything before the last '-'
    tgt_lang="${dirname##*-}" # Extract everything after the last '-'
    inverted_pair="$tgt_lang-$src_lang"

    if [ ! -d $dirname ]; then
        mkdir $dirname
    fi

    pushd $dirname

    cp ../$inverted_pair/*.sh .
    cp ../$inverted_pair/*.yml .
    cp ../$inverted_pair/*.py .
    ./copy-corpus.sh
    rm -r -f run/
    ./train.sh
    ./export.sh
    popd
done


