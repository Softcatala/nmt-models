#!/bin/bash

git clone --depth=1 https://github.com/Softcatala/parallel-catalan-corpus corpus-raw
cd corpus-raw

declare -a arr=("eng-cat" "deu-cat" "ita-cat" "fra-cat" "spa-cat" "nld-cat" "por-cat" "jpn-cat" "glg-cat" "oci-cat")

for dirname in "${arr[@]}"; do
    echo Copying $dirname
    target_dir=../$dirname/corpus-raw/
    rm -f -r $target_dir
    mkdir -p $target_dir
    cp -r $dirname/* $target_dir
    pushd .
    cd $target_dir
    if compgen -G "*.xz" > /dev/null; then
         xz -f -d *.xz
    fi
    popd
done


