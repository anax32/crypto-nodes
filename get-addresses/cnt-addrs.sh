#!/bin/bash
set -u

ADDRESS_OUT=addr.txt.gz
ADDRESS_CNT=cnts.txt.gz

# separate the addresses and count the number of occurances
gzip -d --stdout $ADDRESS_OUT \
  | cut -d' ' -f1 \
  | sort --numeric-sort \
  | uniq --count \
  | sort --numeric-sort \
  | gzip -9 > $ADDRESS_CNT
