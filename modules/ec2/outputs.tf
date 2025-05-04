output "public_instance_id" {
  value = aws_instance.public_instance.id
}

output "private_instance_id" {
  value = aws_instance.private_instance.id
}

output "public_instance_ami" {
  value = aws_instance.public_instance.ami
}

output "private_instance_ami" {
  value = aws_instance.private_instance.ami
}

output "public_instance_type" {
  value = aws_instance.public_instance.instance_type
}

output "private_instance_type" {
  value = aws_instance.private_instance.instance_type
}

output "public_instance_subnet_id" {
  value = aws_instance.public_instance.subnet_id
}

output "private_instance_subnet_id" {
  value = aws_instance.private_instance.subnet_id
}

output "public_instance_has_public_ip" {
  value = aws_instance.public_instance.public_ip != null
}

output "private_instance_has_public_ip" {
  value = aws_instance.private_instance.public_ip != null
}


output "public_instance_sg_id" {
  value = tolist(aws_instance.public_instance.vpc_security_group_ids)[0]
}

output "private_instance_sg_id" {
  value = tolist(aws_instance.private_instance.vpc_security_group_ids)[0]
}
