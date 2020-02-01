#!/bin/bash
set -u

echo "using '$LOCAL_DATA_DIR'"
echo "finding files matching: '$FILE_PATTERN'"
echo "writing to '$LOCAL_DATA_DIR/$GRAPH_FILE'"

# FIXME: coinbase transactions have no input, so discard
#        empty vin elements. otherwise we get a 'null' entry
#        which buggers up the graph search
EDGE_KEY="\"'\(.vin[].txid) \(.txid)'\"" # to find input txid and txid

# clean previous results
rm $LOCAL_DATA_DIR/$GRAPH_FILE

echo "writing edges to '$GRAPH_FILE'"

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
    | jq -r "$EDGE_KEY" \
      2>>/dev/null \
    | gzip -9 \
    > $LOCAL_DATA_DIR/$GRAPH_FILE
done

echo "trimming output"
# HACK jq with two outputs writes a load of shit, so crop the crap
gzip -d --stdout $LOCAL_DATA_DIR/$GRAPH_FILE \
  | cut -c 7- \
  | rev \
  | cut -c 2- \
  | rev \
  | gzip -9 > $LOCAL_DATA_DIR/graph.tmp

mv $LOCAL_DATA_DIR/graph.tmp $LOCAL_DATA_DIR/$GRAPH_FILE
echo "get-graph completed"
# HACK END
