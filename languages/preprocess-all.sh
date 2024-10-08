#!/bin/bash

declare -a arr=("ita-cat" "fra-cat" "spa-cat" "por-cat" "eng-cat" "deu-cat" "nld-cat" "jpn-cat" "glg-cat" "oci-cat" "eus-cat")

for dirname in "${arr[@]}"; do
    echo Processing $dirname
    pushd $dirname
    ./preprocess.sh &
    popd
done
wait

