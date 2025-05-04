variables {
  ami_id            = "ami-0abcdef1234567890"
  instance_type     = "t2.micro"
  key_pair_name     = "test-key"
  public_subnet_id  = "subnet-12345678"  # This should be replaced with actual subnet ID in real test
  private_subnet_id = "subnet-87654321"  # This should be replaced with actual subnet ID in real test
  public_sg_id      = "sg-12345678"      # This should be replaced with actual security group ID in real test
  private_sg_id     = "sg-87654321"      # This should be replaced with actual security group ID in real test
}

run "test_public_instance" {
  command = plan

  assert {
    condition     = aws_instance.public_instance.ami == var.ami_id
    error_message = "Public instance should use the correct AMI"
  }

  assert {
    condition     = aws_instance.public_instance.instance_type == var.instance_type
    error_message = "Public instance should use the correct instance type"
  }

  assert {
    condition     = aws_instance.public_instance.subnet_id == var.public_subnet_id
    error_message = "Public instance should be in the correct subnet"
  }
}

run "test_private_instance" {
  command = plan

  assert {
    condition     = aws_instance.private_instance.ami == var.ami_id
    error_message = "Private instance should use the correct AMI"
  }

  assert {
    condition     = aws_instance.private_instance.instance_type == var.instance_type
    error_message = "Private instance should use the correct instance type"
  }

  assert {
    condition     = aws_instance.private_instance.subnet_id == var.private_subnet_id
    error_message = "Private instance should be in the correct subnet"
  }
} 