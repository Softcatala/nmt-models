# Introduction

This repository contains the scripts to train neuronal translation models for [OpenNMT](https://opennmt.net/) and also the Softcatalà published models.

For more information about training see the [TRAINING](TRAINING.md) document.

The corpus used to train these models are available here: https://github.com/Softcatala/parallel-catalan-corpus/

And here the tools that at Softcatalà to serve these models in production: https://github.com/Softcatala/nmt-softcatala

# Models
Language pair | SC model BLEU | SC Flores200 BLEU | Google BLEU | Meta NLLB200 BLEU | Opus-MT BLEU | Sentences | Download model
|---|---|---|---|---|---|---|---
|German-Catalan | 34.8 |28.9 |35.5 |30.7|18.5| 3142257 | [deu-cat-2022-11-14.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/deu-cat-2022-11-14.zip)
|Catalan-German | 28.5 |25.4 |32.9 |29.1|15.8| 3142257 | [cat-deu-2022-11-16.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-deu-2022-11-16.zip)
|English-Catalan | 46.9 |43.8 |46.0 |41.7|29.8| 7856208 | [eng-cat-2023-10-30.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/eng-cat-2023-10-30.zip)
|Catalan-English | 47.4 |43.5 |47.0 |48.0|29.6| 7856208 | [cat-eng-2023-10-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-eng-2023-10-29.zip)
|Basque-Catalan | 38.8 |24.9 |29.6 |N/A|N/A| 9546180 | [eus-cat-2024-08-09.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/eus-cat-2024-08-09.zip)
|Catalan-Basque | 27.3 |17.1 |18.0 |N/A|N/A| 9546180 | [cat-eus-2024-08-12.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-eus-2024-08-12.zip)
|French-Catalan | 41.3 |31.6 |37.3 |33.3|27.2| 2566302 | [fra-cat-2022-11-09.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/fra-cat-2022-11-09.zip)
|Catalan-French | 41.4 |35.4 |41.7 |39.6|27.9| 2566302 | [cat-fra-2022-11-14.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-fra-2022-11-14.zip)
|Galician-Catalan | 74.1 |31.4 |36.5 |33.2|N/A| 2710149 | [glg-cat-2022-11-17.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/glg-cat-2022-11-17.zip)
|Catalan-Galician | 80.7 |31.9 |33.1 |31.7|N/A| 2710149 | [cat-glg-2022-11-21.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-glg-2022-11-21.zip)
|Italian-Catalan | 39.7 |26.5 |30.6 |27.8|22.0| 2584598 | [ita-cat-2022-11-11.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/ita-cat-2022-11-11.zip)
|Catalan-Italian | 36.2 |24.5 |27.5 |26.0|19.2| 2584598 | [cat-ita-2022-11-15.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-ita-2022-11-15.zip)
|Japanese-Catalan | 24.9 |17.8 |23.4 |N/A|N/A| 1997740 | [jpn-cat-2023-02-17.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/jpn-cat-2023-02-17.zip)
|Catalan-Japanese | 21.3 |19.8 |32.5 |N/A|N/A| 1997740 | [cat-jpn-2023-02-18.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-jpn-2023-02-18.zip)
|Dutch-Catalan | 30.4 |20.3 |27.1 |24.8|15.8| 2208538 | [nld-cat-2022-11-19.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/nld-cat-2022-11-19.zip)
|Catalan-Dutch | 27.6 |18.2 |23.4 |21.8|13.4| 2208538 | [cat-nld-2022-11-19.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-nld-2022-11-19.zip)
|Occitan-Catalan | 74.9 |32.5 |N/A |36.2|N/A| 2711350 | [oci-cat-2022-11-17.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/oci-cat-2022-11-17.zip)
|Catalan-Occitan | 78.8 |28.9 |N/A |27.8|N/A| 2711350 | [cat-oci-2022-11-21.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-oci-2022-11-21.zip)
|Portuguese-Catalan | 41.6 |33.9 |38.7 |34.5|28.1| 2043019 | [por-cat-2022-11-16.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/por-cat-2022-11-16.zip)
|Catalan-Portuguese | 39.0 |32.3 |40.0 |36.5|27.5| 2043019 | [cat-por-2022-11-18.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-por-2022-11-18.zip)
|Spanish-Catalan | 88.8 |22.6 |23.6 |25.8|22.5| 7596985 | [spa-cat-2022-11-16.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/spa-cat-2022-11-16.zip)
|Catalan-Spanish | 87.5 |24.2 |24.2 |25.5|23.2| 7596985 | [cat-spa-2022-11-17.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/cat-spa-2022-11-17.zip)

Legend:
* *SC Model BLEU* column indicates the Softcatalà models' BLEU score against the corpus test dataset (from train/dev/test)
* *SC Flores200 BLEU* column indicates the Softcatalà models' BLEU score against [Flores200 benchmark dataset](https://github.com/facebookresearch/flores) devtest split. This provides an external evaluation
* *Google BLEU* is the BLUE score of Google Translate using the Flores200 benchmark
* *Opus-MT BLEU* is the BLUE score of the [Opus-MT models](https://github.com/Helsinki-NLP/Opus-MT) using the Flores200 benchmark (our ambition is to outperform them)
* *Sentences* is the number of sentences in the corpus used for training
* Meta NLLB200 refers to nllb-200-3.3B model from Meta. This is a very slow model and it's distilled version performs significantly worse.

Notes:
* All models are based on TransformerRelative and SentencePiece has been used as tokenizer.
* We use [Sacrebleu](https://github.com/mjpost/sacrebleu) to calculate BLUE scores with the 13a tokenizer.
* These models are used in production with modest hardware (CPU). As result, these models are a balance between precision and latency. It is possible to further improve BLUE scores by ~+1 BLEU, but at a significant latency cost at inference.
* BLEU is the most popular metric for evaluating machine translation but also broadly acknowledged that it is not perfect. It's estimated that has a [~80% correlation](https://aclanthology.org/W05-0909.pdf) with human judgment
* Flores200 has some limitations. It was produced translating from English to many of the other languages. When you use flores for example to benchmark Catalan - Spanish translations, consider that the Catalan -> Spanish corpus was produced by translating from English to Catalan and from English to Spanish. The resulting Spanish and Catalan translations are different from what a translator will do translating directly from Spanish to Catalan. As a summary, Flores200 is more reliable for benchmarks where English is the source or target language.
* Occitan model is based on Languedocian variant

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
wget https://www.softcatala.org/pub/softcatala/opennmt/models/2022-11-22/eng-cat-2023-10-30.zip
unzip eng-cat-2023-10-30.zip
```

Install dependencies:

```pip3 install ctranslate2 pyonmttok```

Simple translation using Python:

```python

import ctranslate2
translator = ctranslate2.Translator("eng-cat/ctranslate2/")
translator.translate_batch([["▁Hello", "▁world", "!"]])
[[{'tokens': ['▁Hola', '▁món', '!']}]]

```

Simple tokenization & translation using Python:


```python

import pyonmttok
tokenizer=pyonmttok.Tokenizer(mode="none", sp_model_path = "eng-cat/tokenizer/sp_m.model")
tokenized=tokenizer.tokenize("Hello world!")

import ctranslate2
translator = ctranslate2.Translator("eng-cat/ctranslate2/")
translated = translator.translate_batch([tokenized[0]])
print(tokenizer.detokenize(translated[0][0]['tokens']))
Hola món!
```
# Training the models

In order to train models you should have a GPU.

## Training in a machine

First you need to install the necessary packages:

```shell

make install
```

After this, you download be all the corpuses:


```shell

make get-corpus
```

To train the English - Catalan model type:

```shell

make train-eng-cat
```

## Training using a Jupyter notebook

We recommend using [Kaggle](https://www.kaggle.com/) which provides [Jupyter notebooks](https://www.kaggle.com/) with GPU access.

We have a [Jupyter notebook](https://github.com/Softcatala/nmt-models/tree/master/notebook) which allows to trains simple models to learn how to use this toolset.



