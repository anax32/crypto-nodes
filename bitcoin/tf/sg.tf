module "sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "3.17.0"

  name        = "${var.project_name}-sg"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = module.vpc.public_subnets_cidr_blocks

  ingress_with_cidr_blocks = [
    {
      from_port   = 8332
      to_port     = 8332
      protocol    = "TCP"
      description = "network"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_rules = ["all-all"]

  tags = merge(var.project_tags)
}
