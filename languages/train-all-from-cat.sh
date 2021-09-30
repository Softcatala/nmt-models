#!/bin/bash

declare -a arr=("cat-ita" "cat-fra" "cat-spa" "cat-por" "cat-eng" "cat-deu" "cat-nld")
#declare -a arr=("cat-ita")

for dirname in "${arr[@]}"; do
    echo Processing $dirname

    if [ ! -d $dirname ]; then
        mkdir $dirname
    fi

    pushd $dirname

    cp ../master-language/* .
    ./copy-corpus.sh
    ./train.sh
    ./export.sh
    popd
done


