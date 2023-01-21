#!/bin/bash

echo Run experiments spa-cat

cd spa-cat-e4 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 4" > results-g2-spa-cat.txt
cat spa-cat-e4/bleu.txt >> results-g2-spa-cat.txt

