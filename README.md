# Introduction

This repository contains the scripts to train neuronal translation models for [OpenNMT](https://opennmt.net/) and also the Softcatalà published models.

For more information about training see the [TRAINING](TRAINING.md) document.

The corpus used to train these models are available here: https://github.com/Softcatala/parallel-catalan-corpus/

And here the tools that at Softcatalà to serve these models in production: https://github.com/Softcatala/nmt-softcatala

# Models

Language pair | Model BLEU | Flores101 BLEU | Opus-MT BLEU | Sentences | Download model
|---|---|---|---|---|---
|German-Catalan | 37.3 |24.6 |18.50 | 5376400 | [deu-cat-2021-09-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/deu-cat-2021-09-27.zip)
|Catalan-German | 30.6 |21.6 |15.80 | 5376400 | [cat-deu-2021-09-30.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-deu-2021-09-30.zip)
|English-Catalan | 45.1 |40.4 |29.80 | 4459276 | [eng-cat-2021-09-26.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/eng-cat-2021-09-26.zip)
|Catalan-English | 46.9 |41.2 |29.60 | 4459276 | [cat-eng-2021-09-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-eng-2021-09-29.zip)
|French-Catalan | 42.2 |31.7 |27.20 | 2555707 | [fra-cat-2021-09-24.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/fra-cat-2021-09-24.zip)
|Catalan-French | 42.3 |34.6 |27.90 | 2555707 | [cat-fra-2021-09-28.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-fra-2021-09-28.zip)
|Italian-Catalan | 40.9 |26.7 |22.00 | 2563550 | [ita-cat-2021-09-23.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/ita-cat-2021-09-23.zip)
|Catalan-Italian | 37.9 |24.1 |19.20 | 2563550 | [cat-ita-2021-09-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-ita-2021-09-27.zip)
|Dutch-Catalan | 32.0 |19.0 |15.80 | 1838820 | [nld-cat-2021-09-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/nld-cat-2021-09-27.zip)
|Catalan-Dutch | 28.8 |17.6 |13.40 | 1838820 | [cat-nld-2021-09-30.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-nld-2021-09-30.zip)
|Portuguese-Catalan | 42.2 |32.6 |28.10 | 2037197 | [por-cat-2021-09-25.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/por-cat-2021-09-25.zip)
|Catalan-Portuguese | 39.3 |31.6 |27.50 | 2037197 | [cat-por-2021-09-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-por-2021-09-29.zip)
|Spanish-Catalan | 89.4 |22.7 |22.50 | 10278209 | [spa-cat-2021-09-25.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/spa-cat-2021-09-25.zip)
|Catalan-Spanish | 88.5 |23.8 |23.20 | 10278209 | [cat-spa-2021-09-28.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-09-30/cat-spa-2021-09-28.zip)

Legend:
* *Model BLEU* column indicates the models' BLEU score against the corpus test dataset (from train/dev/test)
* *Flores101 BLEU* column indicates the models' BLEU score against [Flores101 benchmark dataset](https://github.com/facebookresearch/flores). This provides an external evaluation
* *Opus-MT BLEU* is the BLUE score of the [Opus-MT models](https://github.com/Helsinki-NLP/Opus-MT) using the Flores101 benchmark (our ambition is to outperform them)
* *Sentences* Number of sentences in the corpus used for training

All models are based on TransformerRelative and SentencePiece has been used as tokenizer. We use [Sacrebleu](https://github.com/mjpost/sacrebleu) to calculate BLUE scores.


## Structure of the models

Description of the directories on the contained in the models zip file:

* *tensorflow*: model exported in Tensorflow format
* *ctranslate2*: model exported in CTranslate2 format (used for inference)
* *metadata*: description of the model
* *tokenizer*: SentencePiece models for both languages

# Using the models

You can use the models with https://github.com/OpenNMT/CTranslate2 which offers fast inference.

At Softcatalà we built also command line tools to translate TXT and PO files. See: https://github.com/Softcatala/nmt-softcatala/tree/master/use-models-tools


Download the model and unpack it:

```bash
wget https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/eng-cat-2021-09-04-1630790361.zip
unzip eng-cat-2021-09-04-1630790361.zip
```

Simple translation using Python:

```python

import ctranslate2
translator = ctranslate2.Translator("ctranslate2/")
translator.translate_batch([["▁Hello", "▁world", "!"]])
[[{'tokens': ['▁Hola', '▁món', '!']}]]

```

Simple tokenization & translation using Python:


```python

import pyonmttok
tokenizer=pyonmttok.Tokenizer(mode="none", sp_model_path = "tokenizer/sp_m.model")
tokenized=tokenizer.tokenize("Hello world!")

import ctranslate2
translator = ctranslate2.Translator("ctranslate2/")
translated = translator.translate_batch([tokenized[0]])
print(tokenizer.detokenize(translated[0][0]['tokens']))
Hola món!
```
