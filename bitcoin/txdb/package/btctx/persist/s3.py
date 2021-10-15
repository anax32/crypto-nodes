import os
import boto3
import socket
import logging


logger = logging.getLogger(__name__)


def upload_file_to_s3(aws_s3_bucket, aws_s3_prefix, fileobj, filename, extra_args=None):
  """write a fileobj to an s3 bucket
  """
  s3 = boto3.client("s3", endpoint_url=os.getenv("AWS_S3_ENDPOINT", None))

  if any([len(v) == 0 for v in [aws_s3_bucket, aws_s3_prefix, filename]]):
    logger.error("AWS bucket, prefix or filename contains empty values")
    return False

  key_name = os.path.join(aws_s3_prefix,
                          socket.gethostname(),
                          os.path.basename(filename))

  logger.info("uploading to '%s/%s'", aws_s3_bucket, key_name)

  # upload the file
  s3.upload_fileobj(fileobj, Bucket=aws_s3_bucket, Key=key_name, ExtraArgs=extra_args)

  return True
