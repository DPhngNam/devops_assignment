variables {
  aws_region     = "us-west-2"
  aws_access_key = "YOUR_ACCESS_KEY"
  aws_secret_key = "YOUR_SECRET_KEY"
  my_ip_cidr     = "1.2.3.4/32"
  ami_id         = "ami-0abcdef1234567890"
  instance_type  = "t2.micro"
  key_pair_name  = "test-key"
}

run "test_vpc_integration" {
  command = plan

  assert {
    condition     = aws_vpc.vpc.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block should be 10.0.0.0/16"
  }
}

run "test_security_groups_integration" {
  command = plan

  assert {
    condition     = aws_security_group.public_ec2_sg.vpc_id == aws_vpc.vpc.id
    error_message = "Public security group should be in the VPC"
  }

  assert {
    condition     = aws_security_group.private_ec2_sg.vpc_id == aws_vpc.vpc.id
    error_message = "Private security group should be in the VPC"
  }
}

run "test_ec2_integration" {
  command = plan

  assert {
    condition     = aws_instance.public_instance.subnet_id == aws_subnet.public_subnet[0].id
    error_message = "Public instance should be in the public subnet"
  }

  assert {
    condition     = aws_instance.private_instance.subnet_id == aws_subnet.private_subnet[0].id
    error_message = "Private instance should be in the private subnet"
  }

  assert {
    condition     = aws_instance.public_instance.vpc_security_group_ids[0] == aws_security_group.public_ec2_sg.id
    error_message = "Public instance should use the public security group"
  }

  assert {
    condition     = aws_instance.private_instance.vpc_security_group_ids[0] == aws_security_group.private_ec2_sg.id
    error_message = "Private instance should use the private security group"
  }
} 