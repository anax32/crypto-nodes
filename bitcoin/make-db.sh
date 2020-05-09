#!/bin/bash

# setup paths to the data in variables used by the scripts
export LOCAL_DATA_DIR=data/btc/unc
export ADDRESS_FILE=addrs.txt.gz
export FILE_PATTERN=*.log.gz
export COUNT_FILE=addr-count.txt.gz
export TRANSACTION_FILE=transactions.txt.gz
export TRANSACTION_LABELS=tx-labels.txt.gz

# get the confirmation status of the transactions
export RPC_HOST=localhost
export RPC_PORT=8332
export RPC_USER=ed
export RPC_PASS=ed
export TX_READ_COUNT=2000

#
# DATABASE
#

# list of addresses
gzip -d $LOCAL_DATA_DIR/$COUNT_FILE -c | tr -s ' ' | cut -d' ' -f3 > database/addresses.csv

# address to transaction mapping
gzip -d $LOCAL_DATA_DIR/$ADDRESS_FILE -c > database/address-to-transaction.csv

# transaction info
python3 transaction-confirmer/gettransactioninfo.py \
       $LOCAL_DATA_DIR/$TRANSACTION_FILE > database/transactions.csv

# transaction-to-block mapping
cut -d' ' -f1,4 database/transactions.csv > database/transaction-to-block.csv
