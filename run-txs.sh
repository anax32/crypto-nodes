#!/bin/bash

# setup paths to the data in variables used by the scripts
export LOCAL_DATA_DIR=data/btc/unc
export ADDRESS_FILE=addrs.txt.gz
export FILE_PATTERN=*.log.gz
export COUNT_FILE=addr-count.txt.gz
export TRANSACTION_FILE=transactions.txt.gz
export TRANSACTION_LABELS=tx-labels.txt.gz

# run the scripts to extract data from the decoded transactions
transaction-extractor/get-addresses.sh
transaction-extractor/count-addresses.sh
transaction-extractor/get-transaction-ids.sh
