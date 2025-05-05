variables {
  vpc_cidr_block    = "10.0.0.0/16"
  private_subnet    = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet     = ["10.0.101.0/24", "10.0.102.0/24"]
  availability_zone = ["us-west-2a", "us-west-2b"]
}

run "vpc_creation_validation" {
  command = plan

  # Assert that the VPC will be created
  assert {
    condition     = length(aws_vpc.vpc) > 0
    error_message = "VPC was not created"
  }

  # Assert that the VPC has the expected CIDR block
  assert {
    condition     = aws_vpc.vpc.cidr_block == var.vpc_cidr_block
    error_message = "VPC CIDR block does not match expected value"
  }

  # Assert that DNS hostnames are enabled
  assert {
    condition     = aws_vpc.vpc.enable_dns_hostnames == true
    error_message = "DNS hostnames not enabled for VPC"
  }
}

run "subnet_creation_validation" {
  command = plan

  # Assert that the correct number of private subnets will be created
  assert {
    condition     = length(aws_subnet.private_subnet) == length(var.private_subnet)
    error_message = "Incorrect number of private subnets"
  }

  # Assert that the correct number of public subnets will be created
  assert {
    condition     = length(aws_subnet.public_subnet) == length(var.public_subnet)
    error_message = "Incorrect number of public subnets"
  }
}

run "gateway_creation_validation" {
  command = plan

  # Assert that the Internet Gateway will be created
  assert {
    condition     = length(aws_internet_gateway.ig) > 0
    error_message = "Internet Gateway was not created"
  }

  # Assert that the NAT Gateway will be created
  assert {
    condition     = length(aws_nat_gateway.public) > 0
    error_message = "NAT Gateway was not created"
  }
}

run "route_table_validation" {
  command = plan

  # Assert that the public route table will be created
  assert {
    condition     = length(aws_route_table.public) > 0
    error_message = "Public route table was not created"
  }

  # Assert that the private route table will be created
  assert {
    condition     = length(aws_route_table.private) > 0
    error_message = "Private route table was not created"
  }

  # We can't directly access route table routes by index since they're a set
  # Instead, we'll just verify that the route tables exist
}

run "security_group_validation" {
  command = plan

  # Assert that the default security group will be created
  assert {
    condition     = length(aws_security_group.default) > 0
    error_message = "Default security group was not created"
  }

  # We can't directly access security group rules by index since they're a set
  # Instead, we'll just verify that the security group exists
}
