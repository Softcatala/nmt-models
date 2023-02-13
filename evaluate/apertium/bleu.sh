echo oci-cat
sacrebleu ../flores200.cat  -i flores200.cat-apertium -m bleu chrf --format text

echo cat-oci
sacrebleu ../flores200.oci  -i flores200.oci-apertium -m bleu chrf --format text
