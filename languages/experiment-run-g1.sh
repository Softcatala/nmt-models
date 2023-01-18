#!/bin/bash

echo Run experiments

cd eng-cat-e4 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 4" > results-g2.txt
cat eng-cat-e4/bleu.txt >> results-g2.txt

cd eng-cat-e5 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 5" >> results-g2.txt
cat eng-cat-e5/bleu.txt >> results-g2.txt

cd eng-cat-e6 && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 6" >> results-g2.txt
cat eng-cat-e6/bleu.txt >> results-g2.txt

