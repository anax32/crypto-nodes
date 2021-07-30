#.env
environment variables for user accounts and data storage locations
ensure $DATA_DIR is writable
$DATA_DIR can be an external drive when mounted normally

#fullnode.yaml
A bunch of services which log bitcoin transaction data to a mongodb

services
--------
+ bitcoind - bitcoin full node which recieves the data. It has to be
             set to reindex on each restart, so restarts will take some
             time. The ZMQ and RPC ports are exposed, RPC is restricted
             to the subnet mask setup by the docker-compose system.
             ZMQ is exposed by 0.0.0.0.
+ txlog - the transaaction logger. This connects to the ZMQ port on
          bitcoind (the logger must be on the same subnet for the DNS
          lookup to work). Once bitcoind is up and running a stream
          of transactions will pass through ZMQ into the logger; the
          transactions are raw hashes, we decode them using the RPC
          methods of bitcoind ("decoderawtransaction"). The decoded
          data is pushed into the mongo database.
+ mongo-storage - database to hold the transaction data
+ mongo-export - service to export the mongodb contents. This service
                 will auto-start then shutdown; to export the data just
                 restart the service ("docker-compose up mongo-export")
+ test-rpc-curl - service to test the bitcoind rpc server with curl
+ test-rpc-py - service to test the bitcoind rpc server from python

# restore.yaml
create a mongodb database and restore a backup file into it so we
have a test dataset with which to work

# process.yaml
process the transaction data in a mongodb database to produce graphs


# usage

+ build the bitcoind container
    + run the fullnode
```bash
docker run \
  -d \
  --rm \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -v $(pwd)/data:/block-data \
  -v $(pwd)/config:/config \
  --name btc-node \
  anax32/bitcoind
```
    + set the bitcoind logger output
```bash
docker exec \
  -it \
  btc-node \
  bitcoin-cli \
    -rpcuser=$RPCU \
    -rpcpassword=$RPCP \
    logging "[\"all\"]" "[\"http\", \"bench\", \"tor\", \"qt\", \"leveldb\", \"net\", \"addrman\", \"selectcoins\", \"rand\", \"prune\", \"libevent\", \"walletdb\"]"
```

+ build and run the `transaction-logger`

```bash
docker build \
  -t anax32/btc-tx-log \
  .

docker run \
  -d \
  --rm \
  -e FILE_LOGGER=1 \
  -e RAWTX_SOURCE_ADDR="tcp://127.0.0.1:28832" \
  -e RAWTX_COUNT_PER_FILE=20000 \
  -e RAWTX_COMPRESSED_LOGS=1 \
  -e OUTPUT_FILE=/data/mempool \
  -e BITCOIND_RPC_USER=${RPC_USERNAME} \
  -e BITCOIND_RPC_PASSWORD=${RPC_PASSWORD} \
  -e BITCOIND_HOST=127.0.0.1 \
  -e BITCOIND_PORT=8332 \
  -e LOG_LEVEL=DEBUG \
  --network=host \
  -v $(pwd)/data:/data \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  --name btc-tx-logger \
  anax32/btc-tx-log
```
