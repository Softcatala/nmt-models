#!/bin/bash

echo Setup experiments
cp -r eng-cat eng-cat-v1
cp -r eng-cat eng-cat-v2
cp -r eng-cat eng-cat-v3
cp -r eng-cat eng-cat-v4
cp -r eng-cat eng-cat-v5

echo Copy single voc.sh
cp master-language/voc.sh eng-cat-v1/
cp master-language/voc.sh eng-cat-v2/
cp master-language/voc.sh eng-cat-v3/
cp master-language/voc.sh eng-cat-v4/
cp master-language/voc.sh eng-cat-v5/

echo Setup voc.sh for experiments
sed -i 's/50000/10000/g' eng-cat-v1/voc.sh
sed -i 's/50000/20000/g' eng-cat-v2/voc.sh
sed -i 's/50000/30000/g' eng-cat-v3/voc.sh
sed -i 's/50000/40000/g' eng-cat-v4/voc.sh
#sed -i 's/50000/50000/g' eng-cat-v5/voc.sh

