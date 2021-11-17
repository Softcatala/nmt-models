#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>


import yaml
import os
import datetime
import unicodedata

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def _normalize_string_src(result):

    original = result
    result = unicodedata.normalize('NFC', result)

    cleaned = original != result
    return result, cleaned

def _normalize_string_trg(result):

    original = result
    result = unicodedata.normalize('NFC', result)

    mapping = {
                '’' : '\'',
    }

    for char in mapping.keys():
        result = result.replace(char, mapping[char])

    cleaned = original != result
    return result, cleaned

def _convert_newlines(result):
    original = result
    mapping = {
                u"\u2028" : '',
                u"\u2029" : '',
              }

    for char in mapping.keys():
        result = result.replace(char, mapping[char])

    cleaned = original != result
    return result, cleaned

def _has_dot_or_equivalent(text):
    t = text

    if t[-1:]== '.' or t[-1:] == '…' or t[-1:] == '?' or t[-1:] == '!':
        return True

    if t[-2:] == '.)' or t[-2:] == '."' or t[-2:] == '.\'':
        return True

    return False

def _process_dot(src, trg, dots):
    s = src.rstrip()
    t = trg.rstrip()

    if s[-1:] == '.' and _has_dot_or_equivalent(t) is False:
        src = src.rstrip()
        trg = trg.rstrip() + "."
        dots = dots + 1
    elif t[-1:] == '.' and _has_dot_or_equivalent(s) is False:
        trg = trg.rstrip()
        src = src.rstrip() + "."
        dots = dots + 1

    return src, trg, dots

def _is_sentence_len_good(src, trg):
    src = src.strip()
    trg = trg.strip()
    lsrc = len(src)
    ltrg = len(trg)

    if lsrc == 0 or ltrg == 0:
        return False

    MIN_CHARS = 50
    if max(lsrc, ltrg) > MIN_CHARS:
        if lsrc < ltrg:
           tmp = lsrc
           lsrc = ltrg
           ltrg = tmp

        diff = (lsrc - ltrg) / lsrc * 100
        if diff > 70:
            return False

    return True

# https://arxiv.org/abs/1907.01279 contains an overview of some of the techniques used here
def split_in_six_files(src_filename, tgt_filename):

    pairs = set()
    number_validation = 3000
    number_test = 3007 # number_test != number_validation

    strings = 0
    duplicated = 0

    print("Split src and tgt files in 6 files for training, text and validation")

    total_lines = file_len(src_filename)
    validation_each = round(total_lines / number_validation)
    test_each = round(total_lines / number_test)
    bad_length = 0
    dots = 0

    if test_each == validation_each:
        print("test_each ({0}) and validation_each  ({0}) cannot be equal".format(test_each, validation_each))
        return
        
    with open("src-val.txt", "w") as source_val,\
        open("tgt-val.txt", "w") as target_val,\
        open("src-test.txt", "w") as source_test,\
        open("tgt-test.txt", "w") as target_test,\
        open("src-train.txt", "w") as source_train,\
        open("tgt-train.txt", "w") as target_train,\
        open(src_filename, "r") as read_source,\
        open(tgt_filename, "r") as read_target:


        print("total_lines {0}".format(total_lines))
        print("number_validation {0}".format(number_validation))
        print("number_test {0}".format(number_test))
        print("validation_each {0}".format(validation_each))
        print("test_each {0}".format(test_each))

        clean_src = clean_trg = 0
        equal = 0
        while True:

            src = read_source.readline()
            trg = read_target.readline()

            if not (src and trg):
                break

            if _is_sentence_len_good(src, trg) is False:
                bad_length = bad_length + 1
                continue

            src, _ = _convert_newlines(src)
            trg, _ = _convert_newlines(trg)

            src, cleaned_src = _normalize_string_src(src)
            trg, cleaned_trg = _normalize_string_trg(trg)

            if src == trg and len(src) > 50 and len(trg) > 50:
                equal += 1
                continue

            pair = src + trg
            if pair in pairs:
                duplicated = duplicated + 1
                continue
            else:
                pairs.add(pair)

            if cleaned_src:
                clean_src = clean_src + 1

            if cleaned_trg:
                clean_trg = clean_trg + 1

            if strings % validation_each == 0:
                source = source_val
                target = target_val
            elif strings % test_each == 0:
                source = source_test
                target = target_test
            else:
                source = source_train
                target = target_train

            src, trg, dots = _process_dot(src, trg, dots)

            source.write(src)
            target.write(trg)

            # Duplicate corpus in upper case to translate properly uppercase text
            source.write(src.upper())
            target.write(trg.upper())

            strings = strings + 1

    pduplicated = duplicated * 100 / strings
    pdots = dots * 100 / strings
    pclean_src = clean_src * 100 / strings
    pclean_trg = clean_trg * 100 / strings
    pbad_length = bad_length * 100 / strings
    pequal = equal * 100 / strings
    print(f"Strings: {strings}, duplicated {duplicated} ({pduplicated:.2f}%)")
    print(f"Cleaned acute accents. src: {clean_src} ({pclean_src:.2f}%), tgt: {clean_trg} ({pclean_trg:.2f}%)")
    print(f"Empty sentences or diff len too long: {bad_length} ({pbad_length:.2f}%)")
    print(f"Dots: {dots} ({pdots:.2f}%), equal: {equal} ({pequal:.2f}%)")

def append_lines_from_file(src_filename, trg_file, max_lines):
    lines = 0
    with open(src_filename, 'r') as tf:
        line = tf.readline()
        while line:
            if max_lines and lines >= max_lines:
                break

            lines += 1
            trg_file.write(line)
            line = tf.readline()

    print("Appended {0} lines from {1}".format(lines, src_filename))
    return lines

def read_configuration():

    with open("corpus.yml", 'r') as stream:
        content = yaml.safe_load(stream)

    sources = content['source_files']
    targets = content['target_files']
    max_lines = content.get('max_lines')

    if max_lines:
        print(f"max_lines: {max_lines}")

    if len(sources) != len(targets):
        print("Different number of sources and targets")
        exit()

    return sources, targets, max_lines
    

def join_multiple_sources_and_target_into_two_files(src_filename, tgt_filename):

    src_lines = 0
    trg_lines = 0

    sources, targets, max_lines = read_configuration()

    print("Join multiple files in two src and tgt files")
    with open(src_filename, "w") as tf_source,\
         open(tgt_filename, "w") as tf_target:

        print("**Sources")
        for source in sources:
            src_lines += append_lines_from_file(source, tf_source, max_lines)

        print("**Targets")
        for target in targets:
            trg_lines += append_lines_from_file(target, tf_target, max_lines)

    print("src lines: " + str(src_lines))
    print("trg lines: " + str(trg_lines))

    if src_lines != trg_lines:
        raise Exception(f"Source and target corpus have different lengths.")

def main():

    print("Joins several corpus and creates a final train, validation and test dataset")
    start_time = datetime.datetime.now()

    single_src = 'src.txt'
    single_tgt = 'tgt.txt'
    join_multiple_sources_and_target_into_two_files(single_src, single_tgt)
    split_in_six_files(single_src, single_tgt)
    os.remove(single_src)
    os.remove(single_tgt)
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)

if __name__ == "__main__":
    main()
