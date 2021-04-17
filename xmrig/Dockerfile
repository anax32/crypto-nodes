from ubuntu as xmrig

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Europe/London"

run apt-get update; \
    apt-get install -q -y --no-install-recommends \
      git \
      build-essential \
      ca-certificates \
      cmake \
      libhwloc-dev \
      libssl-dev \
      libuv1-dev

run git clone https://github.com/xmrig/xmrig.git

run mkdir /xmrig/build && \
    cd /xmrig/build && \
    cmake .. && \
    make -j$(nproc)

from nvidia/cuda:11.2.1-devel as xmrig-cuda

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Europe/London"

run apt-get update; \
    apt-get install -q -y --no-install-recommends \
      git \
      build-essential \
      ca-certificates \
      cmake

run git clone https://github.com/xmrig/xmrig-cuda.git

run mkdir /xmrig-cuda/build && \
    cd /xmrig-cuda/build && \
    cmake .. \
      -DCUDA_LIB=/usr/local/cuda/lib64/stubs/libcuda.so \
      -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
    && \
    make -j$(nproc)

from nvidia/cuda:11.2.1-runtime as host

run apt-get update; \
    apt-get install -q -y --no-install-recommends \
      hwloc

copy --from=xmrig /xmrig/build/xmrig /usr/bin
copy --from=xmrig-cuda /xmrig-cuda/build/libxmrig-cuda.so /usr/lib
