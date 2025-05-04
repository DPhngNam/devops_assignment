output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.vpc.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.vpc.cidr_block
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = [for subnet in aws_subnet.private_subnet : subnet.id]
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = [for subnet in aws_subnet.public_subnet : subnet.id]
}

output "default_security_group_id" {
  description = "The ID of the default security group"
  value       = aws_security_group.default.id
}

output "default_sg_name" {
  description = "The name of the default security group"
  value       = aws_security_group.default.name
}

output "private_subnet_count" {
  description = "Number of private subnets"
  value       = length(aws_subnet.private_subnet)
}

output "public_subnet_count" {
  description = "Number of public subnets"
  value       = length(aws_subnet.public_subnet)
}
