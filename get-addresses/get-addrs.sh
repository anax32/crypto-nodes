#!/bin/bash
set -u

QUERY=${1:-"*.log.gz"}

ADDRESS_OUT=addr.txt.gz
ADDRESS_CNT=cnts.txt.gz
FOUND_KEYS=found-keys.txt

#ADDRESS_KEY=".vout[].scriptPubKey.addresses[]" # to find addresses only
ADDRESS_KEY="\" . | '\(.vout[].scriptPubKey.addresses[]) \(.txid)'\"" # to find add and txcs

# clean previous results
rm $ADDRESS_OUT
rm $FOUND_KEYS

# parse the logs
for i in $QUERY
do
  echo "parsing '$i'"

  # extract the gz
  # get all addresses from teh file
  # append to the address file output
  gzip -d --stdout "$i" \
    | jq -r "$ADDRESS_KEY" \
      2>>/dev/null \
    | gzip -9 \
    > $ADDRESS_OUT
done

# HACK jq with two outputs writes a load of shit, so crop the crap
gzip -d --stdout $ADDRESS_OUT \
  | cut -c 7- \
  | rev \
  | cut -c 2- \
  | rev \
  | gzip -9 > tmp

mv tmp $ADDRESS_OUT
# HACK END
