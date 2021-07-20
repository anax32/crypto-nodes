module "sg" {
  for_each = module.vpc

  source  = "terraform-aws-modules/security-group/aws"
  version = "3.17.0"

  name        = "${var.project_name}-sg-${each.key}"
  vpc_id      = each.value.vpc_id

  ingress_cidr_blocks = each.value.public_subnets_cidr_blocks

  ingress_with_cidr_blocks = [
    {
      from_port   = 8333
      to_port     = 8333
      protocol    = "TCP"
      description = "network"
      cidr_blocks = "0.0.0.0/0"
    },
    {
      from_port = 22
      to_port = 22
      protocol = "TCP"
      description = "ssh"
      cidr_blocks = "82.16.164.173/32"
    }
  ]

  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_rules = ["all-all"]

  tags = merge(var.project_tags)
}
