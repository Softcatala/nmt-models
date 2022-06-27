srcModelName=${PWD##*/}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}

if [ ! -f model-to-txt.py ]
then
    echo "Downloading model-to-txt"
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/requirements.txt
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/model-to-txt.py
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/segment.srx
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/srx_segmenter.py
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/texttokenizer.py
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/ctranslate.py
    wget -q https://raw.githubusercontent.com/Softcatala/nmt-softcatala/master/use-models-tools/preservemarkup.py
fi

modelRootDir=exported/
echo "Test data set" > bleu.txt
python3 model-to-txt.py -m $srcModelName -f src-test.txt -t predictions-test.txt -x $modelRootDir
sacrebleu tgt-test.txt -i predictions-test.txt -m bleu >> bleu.txt

echo "Flores data set" >> bleu.txt
python3 model-to-txt.py -m $srcModelName -f flores101.$srcLanguage -t predictions-flores.txt -x $modelRootDir
sacrebleu flores101.$tgtLanguage -i predictions-flores.txt -m bleu >> bleu.txt

cat bleu.txt


