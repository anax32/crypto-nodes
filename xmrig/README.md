# Monero mining with xmrig

## usage

```bash
docker run \
  -d \
  --dns 8.8.8.8 \
  --name xmrminer \
  --privileged \
  -v /lib/modules:/lib/modules \
  -e XMR_POOL_ADDR=gulf.moneroocean.stream:20128 \
  -e XMR_ADDR=4AJin9Rwi4KE93rgyPKnds569UeXKgxdW7G9vvKUQCKrPYzHQMQmGrFezLq5GuX3Pfjo1wkiHu3jmGRUhRRufjYPBQPtKaH \
  -e WORKER_NAME=$(hostname) \
  anax32/crn:xmr-latest
```

The host requires `msr-tools` and `kmod` are installed for the msr hashrate optimisations (this
is achived in the docker run command with `-v /lib...` and `--privileged`).

**NB**: I also set `--dns` resolved because my IP blocks `gulf.moneroocean.stream`

## CUDA setup

XMRig is a CUDA-enabled monero mining available at https://xmrig.com/

This docker image builds the binary from source and includes
the `CUDA` plugin for NVIDIA gpu mining.

see https://github.com/xmrig for the source and documentation of XMRig
see https://github.com/xmrig/xmrig-cuda for the `CUDA` plugin.


`docker build` requires access to the `CUDA` libraries so you
must set the `/etc/docker/daemon.conf` to contain
`"default-runtime": "nvidia"` at the root

i.e.:
```bash
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "default-runtime": "nvidia"
}
```

and then stop and start your docker service:
```bash
service docker stop
service docker start
```

build the container:
```bash
docker build -t xmrig:cuda .
```

build the xmrig config file using the wonderful wizard at https://xmrig.com/wizard

run the container:
```bash
docker run -v $(pwd):/conf xmrig:cuda /usr/bin/xmrig -c /conf/xmrig.conf
```

# Jetson

To build containers for NVIDIA Jetson devices, find the base containers
here https://ngc.nvidia.com/catalog/containers/nvidia:cuda-arm64/tags
