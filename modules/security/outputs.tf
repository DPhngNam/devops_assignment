output "public_sg_id" {
  value = aws_security_group.public_ec2_sg.id
}

output "private_sg_id" {
  value = aws_security_group.private_ec2_sg.id
}

output "public_sg_name" {
  value = aws_security_group.public_ec2_sg.name
}

output "private_sg_name" {
  value = aws_security_group.private_ec2_sg.name
}

output "public_sg_vpc_id" {
  value = aws_security_group.public_ec2_sg.vpc_id
}

output "private_sg_vpc_id" {
  value = aws_security_group.private_ec2_sg.vpc_id
}

output "public_sg_ingress_count" {
  value = length(aws_security_group.public_ec2_sg.ingress)
}

output "private_sg_ingress_count" {
  value = length(aws_security_group.private_ec2_sg.ingress)
}
