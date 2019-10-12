#!/bin/bash
set -u

echo "getting transactions"

# separate the addressess and transaction ids
# uniq the transaction ids because we may have
# multiple inputs/outputs for each transaction
gzip -d --stdout $LOCAL_DATA_DIR/$ADDRESS_FILE \
  | cut -d' ' -f2 \
  | sort --numeric-sort \
  | uniq \
  | gzip -9 > $LOCAL_DATA_DIR/$TRANSACTION_FILE

echo "transactions completed"
