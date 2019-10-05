#!/bin/sh
set -u

echo "downloading data from '$AWS_BUCKET_NAME/$AWS_SOURCE_PREFIX/$UPLOADING_HOST' to '$LOCAL_DATA_DIR'"

aws s3 cp \
  s3://$AWS_BUCKET_NAME/$AWS_SOURCE_PREFIX/$UPLOADING_HOST \
  $LOCAL_DATA_DIR \
  --recursive
