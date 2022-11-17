echo oci-cat
sacrebleu ../flores101.cat  -i flores101.cat-apertium -m bleu chrf --format text 

echo cat-oci
sacrebleu ../flores101.oci  -i flores101.oci-apertium -m bleu chrf --format text 