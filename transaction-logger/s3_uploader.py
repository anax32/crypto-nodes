import os
import sys
import boto3
import socket
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def upload_file_to_s3(aws_s3_bucket, aws_s3_prefix, filename):
  """read a file from disk
     and upload to s3
  """
  # get the credentials
  aws_s3_creds = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region_name": os.environ["AWS_REGION_NAME"]
  }

  key_name = os.path.join(aws_s3_prefix,
                          socket.gethostname(),
                          os.path.basename(filename))

  # create the boto client
  try:
    s3 = boto3.client("s3", **aws_s3_creds)
  except Exception as e:
    logger.exception("Could not get boto3.client")
    return

  logger.info("uploading to '%s'" % (key_name))

  # upload the file
  try:
    s3.upload_file(Filename=filename,
                   Bucket=aws_s3_bucket,
                   Key=key_name)
  except Exception as e:
    logger.exception("Could not upload_file()")

if __name__ == "__main__":
  logger.info("invoking from cli")
  logger.info("bucket: '%s', prefix: '%s', filename: '%s'" % (
              sys.argv[1],
              sys.argv[2],
              sys.argv[3]))

  upload_file_to_s3(sys.argv[1], sys.argv[2], sys.argv[3])
