resource "aws_s3_bucket" "mempool" {
  bucket_prefix = "${var.project_name}-mempool"
  acl    = "private"

  tags = merge(var.project_tags)
}
