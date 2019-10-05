#!/bin/bash
set -u

ADDRESS_OUT=addr.txt.gz
ADDRESS_CNT=cnts.txt.gz
FOUND_KEYS=found-keys.txt

# search the addresses for particular keys in a list
gzip -d --stdout $ADDRESS_OUT \
  | grep -F -f search-keys.txt \
  | sort \
  > $FOUND_KEYS
