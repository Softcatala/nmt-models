srcModelName=${PWD##*/}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}

src=$tgtLanguage-$srcLanguage
tgt=$srcLanguage-$tgtLanguage

# Training
cp ../$src/corpus/$tgt/src-train.txt .
cp ../$src/corpus/$tgt/tgt-train.txt .
cp ../$src/corpus/$tgt/src-val.txt .
cp ../$src/corpus/$tgt/tgt-val.txt .

# Used for evaluation & metadata
cp ../$src/corpus/$tgt/src-test.txt .
cp ../$src/corpus/$tgt/tgt-test.txt .
cp ../$src/sp-vocab.txt.token .
cp ../$src/sp_m.model .
cp ../$src/flores* .

python3 ../sentencepiece-tokenizer.py

