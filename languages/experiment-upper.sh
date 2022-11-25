#!/bin/bash

pushd ../evaluate
python3 ../data-processing-tools/upper.py flores101.cat flores101-upper.cat
python3 ../data-processing-tools/upper.py flores101.eng flores101-upper.eng

cp flores101-upper.cat flores101.cat
cp flores101-upper.eng flores101.eng
popd

echo Setup experiments
cp -r eng-cat eng-cat-u1
cp -r eng-cat eng-cat-u2


echo Setup voc.sh for experiments
sed -i 's/augmentation_cap: 100/augmentation_cap: 100/g' eng-cat-u1/corpus.yml
sed -i 's/augmentation_cap: 100/augmentation_cap: 50/g' eng-cat-u2/corpus.yml

exit
export QUICK_PREPROCESSING=1
cd eng-cat-u1 && ./preprocess.sh && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 1" > results-upper.txt
cat eng-cat-u1/bleu.txt >> results-upper.txt

cd eng-cat-u2 && ./preprocess.sh && ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 2" >> results-upper.txt
cat eng-cat-u2/bleu.txt >> results-upper.txt

