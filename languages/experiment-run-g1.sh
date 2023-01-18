#!/bin/bash

echo Run experiments spa-cat

cd spa-cat-e1 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 1" > results-g2-spa-cat.txt
cat spa-cat-e1/bleu.txt >> results-g2-spa-cat.txt

cd spa-cat-e2 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 2" >> results-g2-spa-cat.txt
cat spa-cat-e2/bleu.txt >> results-g2-spa-cat.txt

cd spa-cat-e3 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 3" >> results-g2-spa-cat.txt
cat spa-cat-e3/bleu.txt >> results-g2-spa-cat.txt

echo Run experiments cat-spa

cd cat-spa-e1 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 1" > results-g2-cat-spa.txt
cat cat-spa-e1/bleu.txt >> results-g2-cat-spa.txt

cd cat-spa-e2 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 2" >> results-g2-cat-spa.txt
cat cat-spa-e2/bleu.txt >> results-g2-cat-spa.txt

cd cat-spa-e3 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 3" >> results-g2-cat-spa.txt
cat cat-spa-e3/bleu.txt >> results-g2-cat-spa.txt

