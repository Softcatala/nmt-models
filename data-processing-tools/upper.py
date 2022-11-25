#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>


import sys


def main():

    print("Makes file upper-case")
    
    src_fn = sys.argv[1]
    trg_fn = sys.argv[2]

    cnt = 0
    with open(src_fn, "r") as source_val,\
        open(trg_fn, "w") as target_val:

        for src in source_val.readlines():
            target_val.write(src.upper())
            cnt += 1

    print(f"Wrote {trg_fn} - {cnt} lines")

if __name__ == "__main__":
    main()
