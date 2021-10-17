# bitcoin fullnode and friends

## fullnode

`./bitcoind-from-repo` and `./bitcoind-from-src` contain dockerfiles to download/build
the bitcoin core client.

## transaction logger

`./txdb` contains a python package which will listen to the bitcoin core zmq service
and log raw transactions to gzipped csv, mongodb, etc. Optionally upload the csv file
to AWS S3 bucket.

`./Dockerfile` builds a container to host and run this package

##

## lnd lightning node

running `lnd` against the fullnode container requires `lnd` to be setup as if running
against a remote fullnode (IP address, RPC auth, etc).

# usage

+ create a `logger.env` file with the configured environment variables
+ `docker-compose up`

```bash
cat << EOF > logger.env
FILE_LOGGER=1
RAWTX_SOURCE_ADDR=tcp://127.0.0.1:28832
RAWTX_COUNT_PER_FILE=200
BITCOIND_RPC_USER=lolmyuser
BITCOIND_RPC_PASSWORD=lolmypass
BITCOIND_HOST=127.0.0.1
BITCOIND_PORT=8332
AWS_BUCKET_NAME=transactions
AWS_FILE_PREFIX=txlog
AWS_S3_ENDPOINT=http://minioserver:9000
FILENAME_STUB=txn
MINIO_ROOT_USER=lolmybad
MINIO_ROOT_PASSWORD=lolmybadlol
MINIO_INITIAL_BUCKETS=transactions
LOG_LEVEL=DEBUG
AWS_ACCESS_KEY_ID=lolmybad
AWS_SECRET_ACCESS_KEY=lolmybadlol
EOF

docker-compose up
```

this will log every 200 transactions to the `transactions` bucket on a local `minio` server (at `http://localhost:9001`)

**TODO**: many of these vars are not easily set from compose (require static IPs, etc) and should be refactored.
