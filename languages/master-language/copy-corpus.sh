srcModelName=${PWD##*/}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}

src=$tgtLanguage-$srcLanguage

# Copy from xxx-cat and invert order for cat-xxx
cp ../$src/src-train.txt.token tgt-train.txt.token
cp ../$src/src-val.txt.token tgt-val.txt.token
cp ../$src/tgt-train.txt.token src-train.txt.token
cp ../$src/tgt-val.txt.token src-val.txt.token

# Used for evaluation & metadata
cp ../$src/src-test.txt tgt-test.txt
cp ../$src/tgt-test.txt src-test.txt
cp ../$src/src-train.txt tgt-train.txt
cp ../$src/tgt-train.txt src-train.txt


cp ../$src/sp-vocab.txt.token .
cp ../$src/sp_m.model .
cp ../$src/flores* .
 


