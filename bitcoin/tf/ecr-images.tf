data "aws_ecr_repository" "btc_node" {
  name = "${var.project_name}/node"
  tags = merge(var.project_tags)
}

data "aws_ecr_repository" "btc_logger" {
  name = "${var.project_name}/logger"
  tags = merge(var.project_tags)
}

data "aws_ecr_image" "btc_node" {
  repository_name = data.aws_ecr_repository.btc_node.name
  image_tag       = var.btc_node_image_tag
}

data "aws_ecr_image" "btc_logger" {
  repository_name = data.aws_ecr_repository.btc_logger.name
  image_tag       = var.btc_logger_image_tag
}
