variables {
  vpc_id      = "vpc-12345678"  # This should be replaced with actual VPC ID in real test
  my_ip_cidr = "1.2.3.4/32"
}

run "test_public_security_group" {
  command = plan

  assert {
    condition     = aws_security_group.public_ec2_sg.name == "public_ec2_sg"
    error_message = "Public security group name should be 'public_ec2_sg'"
  }

  assert {
    condition     = aws_security_group.public_ec2_sg.vpc_id == var.vpc_id
    error_message = "Public security group should be in the correct VPC"
  }
}

run "test_private_security_group" {
  command = plan

  assert {
    condition     = aws_security_group.private_ec2_sg.name == "private_ec2_sg"
    error_message = "Private security group name should be 'private_ec2_sg'"
  }

  assert {
    condition     = aws_security_group.private_ec2_sg.vpc_id == var.vpc_id
    error_message = "Private security group should be in the correct VPC"
  }
} 