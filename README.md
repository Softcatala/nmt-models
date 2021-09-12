# Introduction

This repository contains the scripts to train neuronal translation models for OpenNMT and also the published models.

For more information about training see the [TRAINING](TRAINING.md) document

# Models

Language pair | Model BLEU | Flores101 BLEU |Sentences| Download model
|---|---|---|---|---
|German-Catalan | 32.31 |20.67 | 5376403 | [deu-cat-2021-09-04-1630760056.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/deu-cat-2021-09-04-1630760056.zip)
|Catalan-German | 25.37 |17.31 | 5376403 | [cat-deu-2021-09-07-1630976658.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-deu-2021-09-07-1630976658.zip)
|English-Catalan | 41.03 |36.06 | 4459276 | [eng-cat-2021-09-04-1630790361.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/eng-cat-2021-09-04-1630790361.zip)
|Catalan-English | 42.33 |36.13 | 0 | [cat-eng-2021-09-05-1630856013.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-eng-2021-09-05-1630856013.zip)
|French-Catalan | 35.92 |26.95 | 2223070 | [fra-cat-2021-09-04-1630729544.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/fra-cat-2021-09-04-1630729544.zip)
|Catalan-French | 35.93 |29.65 | 0 | [cat-fra-2021-09-05-1630884602.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-fra-2021-09-05-1630884602.zip)
|Italian-Catalan | 35.75 |22.09 | 2563642 | [ita-cat-2021-09-03-1630696965.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/ita-cat-2021-09-03-1630696965.zip)
|Catalan-Italian | 32.37 |15.31 | 2563642 | [cat-ita-2021-09-06-1630941629.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-ita-2021-09-06-1630941629.zip)
|Dutch-Catalan | 28.04 |15.79 | 1838820 | [nld-cat-2021-09-07-1631023781.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/nld-cat-2021-09-07-1631023781.zip)
|Catalan-Dutch | 26.00 |14.89 | 1838820 | [cat-nld-2021-09-07-1631052167.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-nld-2021-09-07-1631052167.zip)
|Spanish-Catalan | 91.27 |18.09 | 6545128 | [spa-cat-2021-09-03-1630697264.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/spa-cat-2021-09-03-1630697264.zip)
|Catalan-Spanish | 89.70 |14.10 | 6545128 | [cat-spa-2021-09-06-1630913216.zip](https://www.softcatala.org/pub/softcatala/opennmt/models/baseline/cat-spa-2021-09-06-1630913216.zip)


# Using the models

You can use the models using https://github.com/OpenNMT/CTranslate2

At Softcatalà we built also command line tools to translate TXT and PO files. See: https://github.com/Softcatala/nmt-softcatala/tree/master/use-models-tools
