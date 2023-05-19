echo "English - Catalan" > bleu.txt
sacrebleu flores200.cat -i flores200-predict.cat -m bleu chrf --format text >> bleu.txt

echo "Catalan - English" >> bleu.txt
sacrebleu flores200.eng -i flores200-predict.eng -m bleu chrf --format text >> bleu.txt
cat bleu.txt


