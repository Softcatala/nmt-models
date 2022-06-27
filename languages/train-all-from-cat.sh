#!/bin/bash

declare -a arr=("cat-eng" "cat-deu" "cat-fra" "cat-ita" "cat-spa" "cat-por"  "cat-nld")
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


