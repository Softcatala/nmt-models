#!/bin/bash
# Requieres machine with 300GB

# Note: ./prerprocess.sh done before 
echo Setup experiments
rm -r -f eng-cat/run/*
#cp -r eng-cat eng-cat-v1
#cp -r eng-cat eng-cat-v2
cp -r eng-cat eng-cat-v3
cp -r eng-cat eng-cat-v4
cp -r eng-cat eng-cat-v5
cp -r eng-cat eng-cat-v6
cp -r eng-cat eng-cat-v7
cp -r eng-cat eng-cat-v8

echo Copy single voc.sh
#rm eng-cat-v1/voc.sh && cp master-language/voc.sh eng-cat-v1/
#rm eng-cat-v2/voc.sh && cp master-language/voc.sh eng-cat-v2/
rm eng-cat-v3/voc.sh && cp master-language/voc.sh eng-cat-v3/
rm eng-cat-v4/voc.sh && cp master-language/voc.sh eng-cat-v4/
rm eng-cat-v5/voc.sh && cp master-language/voc.sh eng-cat-v5/
rm eng-cat-v6/voc.sh && cp master-language/voc.sh eng-cat-v6/
rm eng-cat-v7/voc.sh && cp master-language/voc.sh eng-cat-v7/
rm eng-cat-v8/voc.sh && cp master-language/voc.sh eng-cat-v8/

echo Setup voc.sh for experiments
#sed -i 's/50000/10000/g' eng-cat-v1/voc.sh
#sed -i 's/50000/20000/g' eng-cat-v2/voc.sh
sed -i 's/50000/30000/g' eng-cat-v3/voc.sh
sed -i 's/50000/40000/g' eng-cat-v4/voc.sh
sed -i 's/50000/50000/g' eng-cat-v5/voc.sh
sed -i 's/50000/60000/g' eng-cat-v6/voc.sh
sed -i 's/50000/70000/g' eng-cat-v7/voc.sh
sed -i 's/50000/80000/g' eng-cat-v8/voc.sh

#export QUICK_PREPROCESSING=1
#cd eng-cat-v1 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
#echo "Experiment 1" > results.txt
#cat eng-cat-v1/bleu.txt >> results.txt

#cd eng-cat-v2 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
#echo "Experiment 2" >> results.txt
#cat eng-cat-v2/bleu.txt >> results.txt

cd eng-cat-v3 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 3" >> results.txt
cat eng-cat-v3/bleu.txt >> results.txt

cd eng-cat-v4 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 4" > results.txt
cat eng-cat-v4/bleu.txt >> results.txt

cd eng-cat-v5 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 5" >> results.txt
cat eng-cat-v5/bleu.txt >> results.txt

cd eng-cat-v6 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 6" >> results.txt
cat eng-cat-v6/bleu.txt >> results.txt

cd eng-cat-v7 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 7" >> results.txt
cat eng-cat-v7/bleu.txt >> results.txt

cd eng-cat-v8 &&  ./voc.sh && ./train.sh && ./export.sh && cd ..
echo "Experiment 8" >> results.txt
cat eng-cat-v8/bleu.txt >> results.txt
