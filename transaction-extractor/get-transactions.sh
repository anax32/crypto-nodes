#!/bin/bash
set -u

echo "getting transactions"

# separate the addresses and count the number of occurances
gzip -d --stdout $LOCAL_DATA_DIR/$ADDRESS_FILE \
  | cut -d' ' -f2 \
  | sort --numeric-sort \
  | gzip -9 > $LOCAL_DATA_DIR/$TRANSACTION_FILE

echo "transactions completed"
