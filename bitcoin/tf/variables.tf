variable "aws_access_key_id"     { type = string }
variable "aws_secret_access_key" { type = string }
variable "aws_region"            { type = string }

variable "project_name"    { type = string }

variable "btc_node_image_tag" { type = string }
variable "btc_logger_image_tag" { type = string }

variable "availability_zones" {
  type = set(string)
  default = ["eu-west-2c"]
}

variable "project_tags" {
  type = map
  default = {
    project = "btc-logger"
    mode    = "infrastructure"
    env     = "dev"
  }
}
