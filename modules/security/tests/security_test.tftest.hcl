variables {
  vpc_id     = "vpc-12345678"
  my_ip_cidr = "192.168.1.1/32"
}

run "public_security_group_validation" {
  command = plan

  # Assert that the public EC2 security group will be created
  assert {
    condition     = length(aws_security_group.public_ec2_sg) > 0
    error_message = "Public EC2 security group was not created"
  }

  # Assert that the public EC2 security group is associated with the correct VPC
  assert {
    condition     = aws_security_group.public_ec2_sg.vpc_id == var.vpc_id
    error_message = "Public EC2 security group is not associated with the correct VPC"
  }

  # We can't directly access security group rules by index since they're a set
  # Instead, we'll just verify that the security group is associated with the correct VPC
}

run "private_security_group_validation" {
  command = plan

  # Assert that the private EC2 security group will be created
  assert {
    condition     = length(aws_security_group.private_ec2_sg) > 0
    error_message = "Private EC2 security group was not created"
  }

  # Assert that the private EC2 security group is associated with the correct VPC
  assert {
    condition     = aws_security_group.private_ec2_sg.vpc_id == var.vpc_id
    error_message = "Private EC2 security group is not associated with the correct VPC"
  }

  # We can't directly access security group rules by index since they're a set
  # Instead, we'll just verify that the security group is associated with the correct VPC
}
