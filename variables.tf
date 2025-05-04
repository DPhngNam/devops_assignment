variable "ami_id" {}
variable "key_pair_name" {}
variable "my_ip_cidr" {}
variable "aws_region" {}
variable "vpc_cidr_block" {
  type    = string
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-west-1a", "us-west-1b", "us-west-1c"]
}

variable "public_subnet_cidr_blocks" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidr_blocks" {
  type    = list(string)
  default = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}
