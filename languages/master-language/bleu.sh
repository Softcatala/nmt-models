currentDir=${PWD##*/}
srcModelName=${currentDir:0:7}
regex='([a-z]{3})-([a-z]{3})'
[[ $srcModelName =~ $regex ]]
srcLanguage=${BASH_REMATCH[1]}
tgtLanguage=${BASH_REMATCH[2]}

if ! [ -x "$(command -v model_to_txt)" ]; then
    pip3 install git+https://github.com/Softcatala/nmt-softcatala#subdirectory=use-models-tools
fi


if [ $tgtLanguage = "jpn" ]; then
    tokenizer="--tokenize ja-mecab"
fi


modelRootDir=exported/
echo "Test data set" > bleu.txt
model_to_txt -m $srcModelName -f src-test.txt -t predictions-test.txt -x $modelRootDir
sacrebleu tgt-test.txt $tokenizer --confidence -i predictions-test.txt -m bleu chrf --format text >> bleu.txt

echo "Flores data set" >> bleu.txt
model_to_txt -m $srcModelName -f flores200.$srcLanguage -t predictions-flores.txt -x $modelRootDir
sacrebleu $tokenizer flores200.$tgtLanguage --confidence -i predictions-flores.txt -m bleu chrf --format text >> bleu.txt

cat bleu.txt


