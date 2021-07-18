data "aws_ecr_repository" "images" {
  name = var.project_name
  tags = merge(var.project_tags)
}

data "aws_ecr_image" "btc_node" {
  repository_name = data.aws_ecr_repository.images.name
  image_tag       = var.btc_node_image_tag
}

data "aws_ecr_image" "btc_logger" {
  repository_name = data.aws_ecr_repository.images.name
  image_tag       = var.btc_logger_image_tag
}
