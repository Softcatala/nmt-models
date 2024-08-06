VOCSIZE=50000
python3 ../sentencepiece-tokenizer.py -v $VOCSIZE -c
onmt-build-vocab --from_vocab sp_m.vocab --from_format sentencepiece --save_vocab sp-vocab.txt.token

