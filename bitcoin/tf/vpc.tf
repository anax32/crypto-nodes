module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "2.64.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = var.availability_zones
  public_subnets  = ["10.0.101.0/24"]

  enable_nat_gateway = false
  enable_vpn_gateway = true

  tags = merge(var.project_tags)
}
