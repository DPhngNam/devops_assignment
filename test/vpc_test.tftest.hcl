variables {
  vpc_cidr_block    = "10.0.0.0/16"
  private_subnet    = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet     = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zone = ["us-west-2a", "us-west-2b"]
}

run "test_vpc_creation" {
  command = plan

  assert {
    condition     = aws_vpc.vpc.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block should be 10.0.0.0/16"
  }
}

run "test_subnet_creation" {
  command = plan

  assert {
    condition     = length(aws_subnet.private_subnet) == 2
    error_message = "Should create 2 private subnets"
  }

  assert {
    condition     = length(aws_subnet.public_subnet) == 2
    error_message = "Should create 2 public subnets"
  }
}

run "test_security_group" {
  command = plan

  assert {
    condition     = aws_security_group.default.name == "default-sg"
    error_message = "Default security group name should be 'default-sg'"
  }
} 