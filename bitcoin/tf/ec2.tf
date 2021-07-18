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

module "ec2" {
  source                 = "terraform-aws-modules/ec2-instance/aws"
  version                = "~> 2.0"

  name                   = "${var.project_name}-node"
  instance_count         = 1

  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t4g.small"
  key_name               = "${var.project_name}-node"
  monitoring             = true
  vpc_security_group_ids = [module.sg.this_security_group_id]
  subnet_ids             = module.vpc.private_subnets

  user_data              = templatefile("startup.tpl", {
    foo = "bar"
    node_repository = data.aws_ecr_image.btc_node.repository_name
    node_tag = data.aws_ecr_image.btc_node.image_tag
    logger_repository = data.aws_ecr_image.btc_logger.repository_name
    logger_tag = data.aws_ecr_image.btc_logger.image_tag
  })

  tags = merge(var.project_tags)
}
