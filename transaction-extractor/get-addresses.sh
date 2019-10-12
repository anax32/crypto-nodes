#!/bin/bash
set -u

echo "using '$LOCAL_DATA_DIR'"
echo "finding files matching: '$FILE_PATTERN'"
echo "writing to '$LOCAL_DATA_DIR/$ADDRESS_FILE'"

#ADDRESS_KEY=".vout[].scriptPubKey.addresses[]" # to find addresses only
ADDRESS_KEY="\" . | '\(.vout[].scriptPubKey.addresses[]) \(.txid)'\"" # to find add and txcs

# clean previous results
rm $LOCAL_DATA_DIR/$ADDRESS_FILE

echo "writing addresses to '$ADDRESS_FILE'"

gzip --version | head -n 1
jq --version

# parse the logs
for i in $LOCAL_DATA_DIR/$FILE_PATTERN
do
  echo "parsing '$i'"

  # extract the gz
  # get all addresses from teh file
  # append to the address file output
  gzip -d --stdout "$i" \
    | jq -r "$ADDRESS_KEY" \
      2>>/dev/null \
    | gzip -9 \
    > $LOCAL_DATA_DIR/$ADDRESS_FILE
done

echo "trimming output"
# HACK jq with two outputs writes a load of shit, so crop the crap
gzip -d --stdout $LOCAL_DATA_DIR/$ADDRESS_FILE \
  | cut -c 7- \
  | rev \
  | cut -c 2- \
  | rev \
  | gzip -9 > $LOCAL_DATA_DIR/addr.tmp

mv $LOCAL_DATA_DIR/addr.tmp $LOCAL_DATA_DIR/$ADDRESS_FILE
echo "get address completed"
# HACK END
