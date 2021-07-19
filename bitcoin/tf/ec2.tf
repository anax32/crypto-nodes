data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "tls_private_key" "ec2" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "ec2" {
  key_name_prefix   = var.project_name
  public_key = tls_private_key.ec2.public_key_openssh
}

resource "random_string" "rpc_username" {
  length           = 16
  special          = false
}

resource "random_password" "rpc_password" {
  length           = 16
  special          = false
}

module "ec2" {
  source                 = "terraform-aws-modules/ec2-instance/aws"
  version                = "~> 2.0"

  name                   = "${var.project_name}-node"
  instance_count         = 1

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.small"
  key_name               = aws_key_pair.ec2.key_name
  monitoring             = true
  vpc_security_group_ids = [module.sg.this_security_group_id]
  subnet_ids             = module.vpc.public_subnets

  iam_instance_profile   = aws_iam_instance_profile.ec2.name

  associate_public_ip_address = true

  user_data              = templatefile("startup.tpl", {
    node_repository = data.aws_ecr_repository.btc_node.repository_url
    node_tag = data.aws_ecr_image.btc_node.image_tag
    logger_repository = data.aws_ecr_repository.btc_logger.repository_url
    logger_tag = data.aws_ecr_image.btc_logger.image_tag
    aws_region = var.aws_region
    aws_bucket_name = aws_s3_bucket.mempool.id
    rpc_username = random_string.rpc_username.result
    rpc_password = random_password.rpc_password.result
  })

  tags = merge(var.project_tags)
}

output "sshkey" {
  value = tls_private_key.ec2.private_key_pem
}

output "ec2ip" {
  value = module.ec2.public_ip
}

output "rpc_username" {
  value = random_string.rpc_username.result
}
