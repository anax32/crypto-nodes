import os
import sys
import boto3
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def upload_file_to_s3(filename):
  """read a file from disk
     and upload to s3
  """
  logger.info("uploading '%s' to s3")

  # get the credentials
  aws_s3_creds = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region_name": os.environ["AWS_REGION_NAME"]
  }

  aws_s3_bucket = os.environ["AWS_BUCKET_NAME"]
  aws_s3_prefix = os.environ["AWS_FILE_PREFIX"]

  # create the boto client
  s3 = boto3.client("s3", **aws_s3_creds)

  # upload the file
  s3.upload_file(Filename=filename,
                 Bucket=aws_s3_bucket,
                 Key=os.path.join(aws_s3_prefix, os.path.basename(filename)))

if __name__ == "__main__":
  logger.info("invoking from cli")
  upload_file_to_s3(sys.argv[1])
