#!/bin/bash

declare -a arr=("eng-cat" "deu-cat" "fra-cat" "ita-cat" "spa-cat" "por-cat" "nld-cat" "jpn-cat" "glg-cat" "oci-cat")
#declare -a arr=("eng-cat")

for dirname in "${arr[@]}"; do
    echo Processing $dirname
    pushd $dirname
    # Done at pre-process-all.sh
    #./preprocess.sh
    rm -r -f run/
    ./voc.sh
    ./train.sh
    ./export.sh
    popd
done


