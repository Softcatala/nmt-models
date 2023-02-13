currentDir=${PWD##*/}
srcModelName=${currentDir:0:7}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}
tgtModelName=$tgtLanguage"-"$srcLanguage

echo "Source model name:" $srcModelName
echo "Target model name:" $tgtModelName

# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py

mkdir -p corpus/$srcModelName
cp src-train.txt corpus/$srcModelName/src-train.txt
cp src-val.txt corpus/$srcModelName/src-val.txt
cp src-test.txt corpus/$srcModelName/src-test.txt

if [[ -z "${QUICK_PREPROCESSING}" ]]; then
    # Migrate target language to new grammar rules
    python3 ../../data-processing-tools/MTUOC-novaIEC/modificaIEC.py tgt-train.txt corpus/$srcModelName/tgt-train.txt
    python3 ../../data-processing-tools/MTUOC-novaIEC/modificaIEC.py tgt-val.txt corpus/$srcModelName/tgt-val.txt
    python3 ../../data-processing-tools/MTUOC-novaIEC/modificaIEC.py tgt-test.txt corpus/$srcModelName/tgt-test.txt

else
    cp tgt-train.txt corpus/$srcModelName/tgt-train.txt
    cp tgt-val.txt corpus/$srcModelName/tgt-val.txt
    cp tgt-test.txt corpus/$srcModelName/tgt-test.txt

fi

# Prepare corpus in subdir
mkdir -p corpus/$tgtModelName
mv src-train.txt corpus/$tgtModelName/tgt-train.txt
mv src-val.txt corpus/$tgtModelName/tgt-val.txt
mv src-test.txt corpus/$tgtModelName/tgt-test.txt

mv tgt-train.txt corpus/$tgtModelName/src-train.txt
mv tgt-val.txt corpus/$tgtModelName/src-val.txt
mv tgt-test.txt corpus/$tgtModelName/src-test.txt

# Copy datasets for evaluation and metadata
cp corpus/$srcModelName/src-test.txt .
cp corpus/$srcModelName/tgt-test.txt .
cp corpus/$srcModelName/tgt-train.txt .
cp corpus/$srcModelName/src-train.txt .
cp corpus/$srcModelName/tgt-val.txt .
cp corpus/$srcModelName/src-val.txt .
cp ../../evaluate/flores200.$srcLanguage .
cp ../../evaluate/flores200.$tgtLanguage .

