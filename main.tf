provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-west-1"
}

module "vpc" {
  source = "./modules/vpc"

  vpc_cidr_block    = var.vpc_cidr_block
  private_subnet    = var.private_subnet_cidr_blocks
  public_subnet     = var.public_subnet_cidr_blocks
  availability_zone = var.availability_zones
}

module "security" {
  source    = "./modules/security"
  vpc_id    = module.vpc.vpc_id
  my_ip_cidr = var.my_ip_cidr
}

module "ec2" {
  source           = "./modules/ec2"
  ami_id           = var.ami_id
  instance_type    = var.instance_type
  key_pair_name    = var.key_pair_name

  public_subnet_id  = module.vpc.public_subnet_ids[0]
  private_subnet_id = module.vpc.private_subnet_ids[0]

  public_sg_id  = module.security.public_sg_id
  private_sg_id = module.security.private_sg_id
}
