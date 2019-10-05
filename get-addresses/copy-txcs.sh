#!/bin/sh
set -u

echo $AWS_BUCKET_NAME
echo $AWS_FILE_PREFIX
echo $UPLOADING_HOST

aws s3 cp \
  s3://$AWS_BUCKET_NAME/$AWS_FILE_PREFIX/$UPLOADING_HOST \
  $AWS_DOWNLOAD_DIR \
  --recursive
