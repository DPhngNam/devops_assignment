variable "ami_id" {}
variable "key_pair_name" {}
variable "my_ip_cidr" {}
variable "region" {}
variable "vpc_cidr_block" {}
variable "public_subnet_cidr_blocks" { type = list(string) }
variable "private_subnet_cidr_blocks" { type = list(string) }
variable "availability_zones" { type = list(string) }
variable "instance_type" {}
variable "key_pair_name" {}