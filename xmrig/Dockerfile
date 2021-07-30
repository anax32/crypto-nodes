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

from ubuntu as host

run apt-get update; \
    apt-get install -q -y --no-install-recommends \
      libssl1.1 \
      hwloc \
      msr-tools \
      kmod

copy --from=xmrig /xmrig/build/xmrig /usr/bin
copy random_boost.sh /usr/bin/random_boost.sh

# ref:
#   https://xmrig.com/docs/miner/command-line-options
CMD /bin/bash -c 'random_boost.sh && xmrig --donate-level 2 -o ${XMR_POOL_ADDR} -u ${XMR_ADDR} -k --tls -p ${WORKER_NAME} --randomx-1gb-pages'
