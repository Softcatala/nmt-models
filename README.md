# Introduction

This repository contains the scripts to train neuronal translation models for [OpenNMT](https://opennmt.net/) and also the Softcatalà published models.

For more information about training see the [TRAINING](TRAINING.md) document.

The corpus used to train these models are available here: https://github.com/Softcatala/parallel-catalan-corpus/

And here the tools that at Softcatalà to serve these models in production: https://github.com/Softcatala/nmt-softcatala

# Models
Language pair | SC model BLEU | SC Flores101 BLEU | Google BLEU | Meta NLLB200 BLEU | Opus-MT BLEU | Sentences | Download model
|---|---|---|---|---|---|---|---
|German-Catalan | 35.8 |28.5 |35.5 |30.7|18.5| 2961962 | [deu-cat-2022-07-09.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/deu-cat-2022-07-09.zip)
|Catalan-German | 30.0 |24.5 |32.9 |29.1|15.8| 2961962 | [cat-deu-2022-07-10.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-deu-2022-07-10.zip)
|English-Catalan | 46.2 |42.2 |46.0 |41.7|29.8| 4499272 | [eng-cat-2022-06-18.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/eng-cat-2022-06-18.zip)
|Catalan-English | 46.8 |42.4 |47.0 |48.0|29.6| 4499272 | [cat-eng-2022-06-24.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-eng-2022-06-24.zip)
|French-Catalan | 41.9 |31.8 |37.3 |33.3|27.2| 2566302 | [fra-cat-2022-06-20.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/fra-cat-2022-06-20.zip)
|Catalan-French | 41.8 |35.1 |41.7 |39.6|27.9| 2566302 | [cat-fra-2022-06-25.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-fra-2022-06-25.zip)
|Italian-Catalan | 40.0 |26.8 |30.6 |27.8|22.0| 2584598 | [ita-cat-2022-06-21.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/ita-cat-2022-06-21.zip)
|Catalan-Italian | 36.5 |24.6 |27.5 |26.0|19.2| 2584598 | [cat-ita-2022-06-26.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-ita-2022-06-26.zip)
|Japanese-Catalan | 24.1 |16.9 |23.4 |N/A|N/A| 1974248 | [jpn-cat-2022-06-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/jpn-cat-2022-06-29.zip)
|Catalan-Japanese | 26.9 |19.5 |32.5 |N/A|N/A| 1974248 | [cat-jpn-2022-07-02.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-jpn-2022-07-02.zip)
|Dutch-Catalan | 31.5 |19.8 |27.1 |24.8|15.8| 1844622 | [nld-cat-2022-06-23.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/nld-cat-2022-06-23.zip)
|Catalan-Dutch | 29.2 |18.0 |23.4 |21.8|13.4| 1844622 | [cat-nld-2022-06-29.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-nld-2022-06-29.zip)
|Portuguese-Catalan | 41.7 |34.2 |38.7 |34.5|28.1| 2043019 | [por-cat-2022-06-22.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/por-cat-2022-06-22.zip)
|Catalan-Portuguese | 39.4 |32.4 |40.0 |36.5|27.5| 2043019 | [cat-por-2022-06-28.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-por-2022-06-28.zip)
|Spanish-Catalan | 89.8 |22.7 |23.6 |25.8|22.5| 7596985 | [spa-cat-2022-06-21.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/spa-cat-2022-06-21.zip)
|Catalan-Spanish | 88.4 |24.3 |24.2 |25.5|23.2| 7596985 | [cat-spa-2022-06-27.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/cat-spa-2022-06-27.zip)

Legend:
* *SC Model BLEU* column indicates the Softcatalà models' BLEU score against the corpus test dataset (from train/dev/test)
* *SC Flores101 BLEU* column indicates the Softcatalà models' BLEU score against [Flores101 benchmark dataset](https://github.com/facebookresearch/flores). This provides an external evaluation
* *Google BLEU* is the BLUE score of Google Translate using the Flores101 benchmark
* *Opus-MT BLEU* is the BLUE score of the [Opus-MT models](https://github.com/Helsinki-NLP/Opus-MT) using the Flores101 benchmark (our ambition is to outperform them)
* *Sentences* is the number of sentences in the corpus used for training
* Meta NLLB200 refers to nllb-200-3.3B model from Meta. This is a very slow model and it's distilled version performs significantly worse.
Notes:
* All models are based on TransformerRelative and SentencePiece has been used as tokenizer.
* We use [Sacrebleu](https://github.com/mjpost/sacrebleu) to calculate BLUE scores with the 13a tokenizer.
* These models are used in production with modest hardware (CPU). As result, these models are a balance between precision and latency. It is possible to further improve BLUE scores by ~+1 BLEU, but at a significant latency cost at inference.
* BLEU is the most popular metric for evaluating machine translation but also broadly acknowledged that it is not perfect. It's estimated that has a [~80% correlation](https://aclanthology.org/W05-0909.pdf) with human judgment
* Flores101 has some limitations. It was produced translating from English to the other 100 languages. When you use flores for example to benchmark Catalan - Spanish translations, consider that the Catalan -> Spanish corpus was produced by translating from English to Catalan and from English to Spanish. The resulting Spanish and Catalan translations are different from what a translator will do translating directly from Spanish to Catalan. As a summary, Flores101 is more reliable for benchmarks where English is the source or target language. 

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
https://www.softcatala.org/pub/softcatala/opennmt/models/2022-06-17/eng-cat-2022-06-18.zip
unzip eng-cat-2022-06-18.zip
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
translator = ctranslate2.Translator("ctranslate2/")
translated = translator.translate_batch([tokenized[0]])
print(tokenizer.detokenize(translated[0][0]['tokens']))
Hola món!
```
