# Introduction

This repository contains the scripts to train neuronal translation models for [OpenNMT](https://opennmt.net/) and also the Softcatalà published models.

For more information about training see the [TRAINING](TRAINING.md) document.

The corpus used to train these models are available here: https://github.com/Softcatala/parallel-catalan-corpus/

And here the tools that at Softcatalà to serve these models in production: https://github.com/Softcatala/nmt-softcatala

# Models

Language pair | Model BLEU | Flores101 BLEU | Google BLEU | Opus-MT BLEU | Sentences | Download model
|---|---|---|---|---|---|---
|German-Catalan | 37.4 |24.7 |35.50 |18.50| 5376400 | [deu-cat-2021-10-23.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/deu-cat-2021-10-23.zip)
|Catalan-German | 30.5 |22.0 |32.90 |15.80| 5408192 | [cat-deu-2021-10-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-deu-2021-10-27.zip)
|English-Catalan | 45.2 |40.7 |46.00 |29.80| 4459276 | [eng-cat-2021-10-23.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/eng-cat-2021-10-23.zip)
|Catalan-English | 46.9 |41.0 |47.00 |29.60| 4493908 | [cat-eng-2021-10-24.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-eng-2021-10-24.zip)
|French-Catalan | 42.1 |31.6 |37.30 |27.20| 2555707 | [fra-cat-2021-10-25.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/fra-cat-2021-10-25.zip)
|Catalan-French | 42.1 |34.4 |41.70 |27.90| 2573723 | [cat-fra-2021-10-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-fra-2021-10-27.zip)
|Italian-Catalan | 40.6 |26.4 |30.60 |22.00| 2563550 | [ita-cat-2021-10-25.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/ita-cat-2021-10-25.zip)
|Catalan-Italian | 38.0 |24.0 |27.50 |19.20| 2689004 | [cat-ita-2021-10-26.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-ita-2021-10-26.zip)
|Dutch-Catalan | 31.8 |19.2 |27.10 |15.80| 1838820 | [nld-cat-2021-10-24.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/nld-cat-2021-10-24.zip)
|Catalan-Dutch | 28.9 |17.4 |23.40 |13.40| 1852678 | [cat-nld-2021-10-28.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-nld-2021-10-28.zip)
|Portuguese-Catalan | 42.1 |32.8 |38.70 |28.10| 2037197 | [por-cat-2021-10-26.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/por-cat-2021-10-26.zip)
|Catalan-Portuguese | 39.6 |31.4 |40.00 |27.50| 2052812 | [cat-por-2021-10-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-por-2021-10-27.zip)
|Spanish-Catalan | 89.3 |22.6 |23.60 |22.50| 10278209 | [spa-cat-2021-10-28.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/spa-cat-2021-10-28.zip)
|Catalan-Spanish | 88.6 |23.9 |24.20 |23.20| 10328129 | [cat-spa-2021-10-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2021-10-27/cat-spa-2021-10-29.zip)

Legend:
* *Model BLEU* column indicates the models' BLEU score against the corpus test dataset (from train/dev/test)
* *Flores101 BLEU* column indicates the models' BLEU score against [Flores101 benchmark dataset](https://github.com/facebookresearch/flores). This provides an external evaluation
* *Google BLEU* is the BLUE score of Google Translate using the Flores101 benchmark
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

Install dependencies:

```pip3 install ctranslate2 pyonmttok```

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
