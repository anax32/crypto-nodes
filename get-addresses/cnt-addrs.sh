#!/bin/bash
set -u

echo "sort+count addresses"

# separate the addresses and count the number of occurances
gzip -d --stdout $LOCAL_DATA_DIR/$ADDRESS_FILE \
  | cut -d' ' -f1 \
  | sort --numeric-sort \
  | uniq --count \
  | sort --numeric-sort \
  | gzip -9 > $LOCAL_DATA_DIR/$COUNT_FILE

echo "sort+count completed"
