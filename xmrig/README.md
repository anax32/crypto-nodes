# Monero mining with xmrig

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
