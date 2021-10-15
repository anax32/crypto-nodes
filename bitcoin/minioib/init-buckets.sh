#!/bin/bash

for x in $(echo $MINIO_INITIAL_BUCKETS | sed 's/,/\n/g')
do
  mkdir -p /data/$x
done

/usr/bin/docker-entrypoint.sh

minio server /data --console-address :9001
