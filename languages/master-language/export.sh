modelName=${PWD##*/}
exportDir=exported/$modelName
rm $exportDir -r -f
mkdir -p $exportDir/metadata
mkdir -p $exportDir/tokenizer


#
# Export model
#
modelDescription="$exportDir/metadata/model_description.txt"
currentDate=`date +"%Y-%m-%d"`
#read -p 'Describe model: ' uservar
onmt-main --config data.yml --auto_config export --export_dir $exportDir/tensorflow/
echo "Model description: $modelName" >> $modelDescription
echo "Date: $currentDate" >> $modelDescription
python3 ../../install-scripts/stack-versions.py >> $modelDescription
wc corpus/$modelName/src-train.txt -l > $exportDir/metadata/inputs_used.txt
ls corpus/$modelName/*.txt -l >> $exportDir/metadata/inputs_used.txt
cp *.model $exportDir/tokenizer/
cp data.yml $exportDir/metadata/
cp corpus.yml $exportDir/metadata/
cp sp-vocab.txt.token $exportDir/tensorflow/assets/
ct2-opennmt-tf-converter --model_path run/ --model_type TransformerBaseRelative --output_dir $exportDir/ctranslate2 --src_vocab sp-vocab.txt.token --tgt_vocab sp-vocab.txt.token --quantization int8

#
# Run evaluation
#
source bleu.sh
cat bleu.txt >>  $modelDescription

#
# Package results
#
cd exported && zip -r ../$modelName-$currentDate.zip *
#scp -i ~/.ssh/sc_key -P 2662 ../$modelName-$currentDate.zip baixades@softcatala.org:/home/baixades/models/2022-06-17/
