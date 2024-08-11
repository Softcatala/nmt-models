#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>


import yaml
import os
import datetime
import unicodedata
from optparse import OptionParser
import resource
import re

g_configuration = None

def set_configuration(dictionary):
    global g_configuration
    g_configuration = dictionary

# In src-tgt pair (jpn-cat), tgt is always 'cat' and tgt-src (e.g. cat-jpn) pair src is always 'cat'
#
# 0 - Disabled
AUGMENTATION_CAP_DISABLED=0
# 1 - Generate a src and tgt sentences in upper case for both 'src-tgt' (e.g. eng-cat) and 'tgt-src' (e.g. cat-eng) language pairs
AUGMENTATION_CAP_BOTH_LANGUAGE_PAIRS=1
# 2 - Generate a src in upper case with the same target only for 'tgt-src' language pair (e.g. cat-jpn)
AUGMENTATION_CAP_FOR_SECOND_LANGUAGE_PAIR=2

def read_configuration():

    with open("corpus.yml", 'r') as stream:
        content = yaml.safe_load(stream)

    sources = content['source_files']
    targets = content['target_files']
    max_lines = content.get('max_lines')

    if len(sources) != len(targets):
        print("Different number of sources and targets")
        exit()

    ensure_dots = content.get('ensure_dots', True)
    augmentation_cap = content.get('augmentation_cap', 1)
    size_diff_percentage = content.get('size_diff_percentage', 70)

    d = {}
    d['sources'] = sources
    d['targets'] = targets
    d['max_lines'] = max_lines
    d['ensure_dots'] = ensure_dots
    d['augmentation_cap'] = augmentation_cap
    d['size_diff_percentage'] = size_diff_percentage
    return d

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

def _remove_special_newlines(result):
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

    if t[-1:]== '.' or t[-1:] == '…' or t[-1:] == '?' or t[-1:] == '!' or t[-1:] == ',' or t[-1:] == ':':
        return True

    if t[-2:] == '.)' or t[-2:] == '."' or t[-2:] == '.\'':
        return True

    return False

def _add_punctuation_at_the_end(text, char):
    pos = len(text) - (len(text) - len(text.rstrip()))
    new = text[:pos] + char + text[pos:]
    return new

def _process_dot(src, trg, dots):
    s = src.rstrip()
    t = trg.rstrip()

    if s[-1:] == '.' and _has_dot_or_equivalent(t) is False:
        trg = _add_punctuation_at_the_end(trg, ".")
        dots = dots + 1
    elif t[-1:] == '.' and _has_dot_or_equivalent(s) is False:
        src = _add_punctuation_at_the_end(src, ".")
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
        size_diff_percentage = g_configuration['size_diff_percentage']
        if size_diff_percentage > 0:
            if lsrc < ltrg:
               tmp = lsrc
               lsrc = ltrg
               ltrg = tmp

            diff = (lsrc - ltrg) / lsrc * 100
            if diff > size_diff_percentage:
                return False

    return True

# How to split test-val sets based on https://en.wikipedia.org/wiki/Per_mille
def _get_val_test_split_steps(lines, per_mille_val, per_mille_test):
    lines_val = round(lines * per_mille_val / 1000)
    steps_val = round(lines / lines_val)

    lines_test = round(lines * per_mille_test / 1000)
    steps_test = round(lines / lines_test)

    return steps_val, steps_test

def _create_dir_if_does_exist(directory):
    if not os.path.exists(directory):
       os.makedirs(directory)

def _clean_for_dup_detection(string):
    return re.sub(r'\s+', '', string)

# https://arxiv.org/abs/1907.01279 contains an overview of some of the techniques used here
def split_in_six_files(src_filename, tgt_filename, directory, source_lang, target_lang):

    pairs = set()
    strings = 0
    duplicated = 0

    print("Split src and tgt files in 6 files for training, text and validation")

    total_lines = file_len(src_filename)
    SAMPLE_PER_MILLE_VAL = 1
    SAMPLE_PER_MILLE_TEST = 1
    steps_val, steps_test = _get_val_test_split_steps(total_lines, SAMPLE_PER_MILLE_VAL, SAMPLE_PER_MILLE_TEST)
    clean_src = clean_trg = 0
    equal = 0
    bad_length = 0
    dots = 0

    ensure_dots = g_configuration['ensure_dots']
    augmentation_cap = g_configuration['augmentation_cap']

    src_dir = os.path.join(directory, f"{source_lang}-{target_lang}")
    tgt_dir = os.path.join(directory, f"{target_lang}-{source_lang}")
    _create_dir_if_does_exist(src_dir)
    _create_dir_if_does_exist(tgt_dir)
        
    with open(os.path.join(src_dir, "src-val.txt"), "w") as src_source_val,\
        open(os.path.join(src_dir, "tgt-val.txt"), "w") as src_target_val,\
        open(os.path.join(src_dir, "src-test.txt"), "w") as src_source_test,\
        open(os.path.join(src_dir, "tgt-test.txt"), "w") as src_target_test,\
        open(os.path.join(src_dir, "src-train.txt"), "w") as src_source_train,\
        open(os.path.join(src_dir, "tgt-train.txt"), "w") as src_target_train,\
        open(os.path.join(tgt_dir, "src-val.txt"), "w") as tgt_source_val,\
        open(os.path.join(tgt_dir, "tgt-val.txt"), "w") as tgt_target_val,\
        open(os.path.join(tgt_dir, "src-test.txt"), "w") as tgt_source_test,\
        open(os.path.join(tgt_dir, "tgt-test.txt"), "w") as tgt_target_test,\
        open(os.path.join(tgt_dir, "src-train.txt"), "w") as tgt_source_train,\
        open(os.path.join(tgt_dir, "tgt-train.txt"), "w") as tgt_target_train,\
        open(src_filename, "r") as read_source,\
        open(tgt_filename, "r") as read_target:

        print("total_lines {0}".format(total_lines))

        cnt_steps_val = cnt_steps_test = clean_src = clean_trg = 0
        while True:

            src = read_source.readline()
            trg = read_target.readline()

            if not (src and trg):
                break

            if _is_sentence_len_good(src, trg) is False:
                bad_length = bad_length + 1
                continue

            src, _ = _remove_special_newlines(src)
            trg, _ = _remove_special_newlines(trg)

            src, cleaned_src = _normalize_string_src(src)
            trg, cleaned_trg = _normalize_string_trg(trg)

            if src == trg and len(src) > 50 and len(trg) > 50:
                equal += 1
                continue

            with_no_spaces = _clean_for_dup_detection(src + trg)
            pair = hash(with_no_spaces)
            if pair in pairs:
                duplicated = duplicated + 1
                continue
            else:
                pairs.add(pair)

            if cleaned_src:
                clean_src = clean_src + 1

            if cleaned_trg:
                clean_trg = clean_trg + 1

            if cnt_steps_val >= steps_val:
                src_source = src_source_val
                src_target = src_target_val
                tgt_source = tgt_source_val
                tgt_target = tgt_target_val
                cnt_steps_val = 0
            elif cnt_steps_test >= steps_test:
                src_source = src_source_test
                src_target = src_target_test
                tgt_source = tgt_source_test
                tgt_target = tgt_target_test
                cnt_steps_test = 0
            else:
                src_source = src_source_train
                src_target = src_target_train
                tgt_source = tgt_source_train
                tgt_target = tgt_target_train

            if ensure_dots:
                src, trg, dots = _process_dot(src, trg, dots)

            src_source.write(src)
            src_target.write(trg)
            tgt_source.write(trg)
            tgt_target.write(src)

            # Duplicate corpus in upper case to translate properly uppercase text
            if augmentation_cap == AUGMENTATION_CAP_BOTH_LANGUAGE_PAIRS:
                src_source.write(src.upper())
                src_target.write(trg.upper())
                tgt_source.write(trg.upper())
                tgt_target.write(src.upper())
            elif augmentation_cap == AUGMENTATION_CAP_FOR_SECOND_LANGUAGE_PAIR:
                tgt_source.write(trg.upper())
                tgt_target.write(src)

            strings += 1
            cnt_steps_val += 1
            cnt_steps_test += 1

    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
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
    print(f"max_rss {max_rss:.2f} MB")

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


def join_multiple_sources_and_target_into_two_files(src_filename, tgt_filename):

    src_lines = 0
    trg_lines = 0

    sources = g_configuration['sources']
    targets = g_configuration['targets']
    max_lines = g_configuration['max_lines']

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

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-o',
        '--output',
        type='string',
        action='store',
        default=None,
        dest='directory',
        help="Output directory"
    )

    parser.add_option(
        '-s',
        '--source',
        type='string',
        action='store',
        default=None,
        dest='source',
        help="Name of the source language"
    )

    parser.add_option(
        '-t',
        '--target',
        type='string',
        action='store',
        default=None,
        dest='target',
        help="Name of the target language"
    )

    (options, args) = parser.parse_args()
    if options.source is None:
        parser.error('No source language given')

    if options.target is None:
        parser.error('No target language given')

    if options.directory is None:
        parser.error('No output directory given')
    
    return options.directory, options.source, options.target

def main():

    print("Joins several corpus and creates a final train, validation and test dataset for both language pairs")
    start_time = datetime.datetime.now()
    directory, source_lang, target_lang = read_parameters()
    set_configuration(read_configuration())

    single_src = 'src.txt'
    single_tgt = 'tgt.txt'
    join_multiple_sources_and_target_into_two_files(single_src, single_tgt)
    split_in_six_files(single_src, single_tgt, directory, source_lang, target_lang)
    os.remove(single_src)
    os.remove(single_tgt)
    s = 'Time used: {0}'.format(datetime.datetime.now() - start_time)
    print(s)

if __name__ == "__main__":
    main()
