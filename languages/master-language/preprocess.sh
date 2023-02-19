currentDir=${PWD##*/}
srcModelName=${currentDir:0:7}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}
tgtModelName=$tgtLanguage"-"$srcLanguage
modificaIEC="../../data-processing-tools/MTUOC-novaIEC/modificaIEC.py"

echo "Source model name:" $srcModelName
echo "Target model name:" $tgtModelName

# Generate final src-val-test single files
python3 ../../data-processing-tools/join-single-file.py -s $srcLanguage -t $tgtLanguage -o corpus

# Migrate target language to new grammar rules
if [[ -z "${QUICK_PREPROCESSING}" ]]; then
    for split in "tgt-train.txt" "tgt-val.txt" "tgt-test.txt"; do
        file="corpus"/$srcModelName/$split
        filebak=$file".bak"
        cp $file $filebak
        python3 $modificaIEC $filebak $file
    done
fi

# Copy datasets for evaluation and metadata
cp corpus/$srcModelName/src-test.txt .
cp corpus/$srcModelName/tgt-test.txt .
cp corpus/$srcModelName/tgt-train.txt .
cp corpus/$srcModelName/src-train.txt .
cp corpus/$srcModelName/tgt-val.txt .
cp corpus/$srcModelName/src-val.txt .
cp ../../evaluate/flores200.$srcLanguage .
cp ../../evaluate/flores200.$tgtLanguage .

