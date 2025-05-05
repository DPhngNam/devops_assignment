variables {
  ami_id           = "ami-0f88e80871fd81e91"  # Use a valid AMI ID for testing
  instance_type    = "t2.micro"
  key_pair_name    = "test-key"
  public_subnet_id = "subnet-public12345"
  private_subnet_id = "subnet-private12345"
  public_sg_id     = "sg-public12345"
  private_sg_id    = "sg-private12345"
}

run "public_instance_validation" {
  command = plan

  # Assert that the public instance will be created
  assert {
    condition     = length(aws_instance.public_instance) > 0
    error_message = "Public instance was not created"
  }

  # Assert that the public instance has the correct AMI
  assert {
    condition     = aws_instance.public_instance.ami == var.ami_id
    error_message = "Public instance does not have the correct AMI"
  }

  # Assert that the public instance has the correct instance type
  assert {
    condition     = aws_instance.public_instance.instance_type == var.instance_type
    error_message = "Public instance does not have the correct instance type"
  }

  # Assert that the public instance is in the correct subnet
  assert {
    condition     = aws_instance.public_instance.subnet_id == var.public_subnet_id
    error_message = "Public instance is not in the correct subnet"
  }

  # Assert that the public instance has the correct key pair
  assert {
    condition     = aws_instance.public_instance.key_name == var.key_pair_name
    error_message = "Public instance does not have the correct key pair"
  }

  # We can't directly access security group IDs by index since they're a set
  # Instead, we'll verify that the instance has a public IP
  assert {
    condition     = aws_instance.public_instance.associate_public_ip_address == true
    error_message = "Public instance does not have a public IP"
  }
}

run "private_instance_validation" {
  command = plan

  # Assert that the private instance will be created
  assert {
    condition     = length(aws_instance.private_instance) > 0
    error_message = "Private instance was not created"
  }

  # Assert that the private instance has the correct AMI
  assert {
    condition     = aws_instance.private_instance.ami == var.ami_id
    error_message = "Private instance does not have the correct AMI"
  }

  # Assert that the private instance has the correct instance type
  assert {
    condition     = aws_instance.private_instance.instance_type == var.instance_type
    error_message = "Private instance does not have the correct instance type"
  }

  # Assert that the private instance is in the correct subnet
  assert {
    condition     = aws_instance.private_instance.subnet_id == var.private_subnet_id
    error_message = "Private instance is not in the correct subnet"
  }

  # Assert that the private instance has the correct key pair
  assert {
    condition     = aws_instance.private_instance.key_name == var.key_pair_name
    error_message = "Private instance does not have the correct key pair"
  }

  # We can't directly access security group IDs by index since they're a set
  # Instead, we'll verify that the instance does not have a public IP
  assert {
    condition     = aws_instance.private_instance.associate_public_ip_address == false
    error_message = "Private instance has a public IP"
  }
}
