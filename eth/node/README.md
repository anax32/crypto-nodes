# Geth

run an ethereum node using the official client

see:
+ https://hub.docker.com/r/ethereum/client-go/
+ https://docs.ethhub.io/using-ethereum/running-an-ethereum-node/

# Usage

## run

```bash
docker run \
  -d \
  --rm \
  -v $(pwd)/data:/root \
  ethereum/client-go
```
