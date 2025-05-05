variables {
  aws_region                = "us-west-2"
  vpc_cidr_block            = "10.0.0.0/16"
  private_subnet_cidr_blocks = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnet_cidr_blocks  = ["10.0.101.0/24", "10.0.102.0/24"]
  availability_zones        = ["us-west-2a", "us-west-2b"]
  my_ip_cidr                = "192.168.1.1/32"
  ami_id                    = "ami-0f88e80871fd81e91"  # Use a valid AMI ID for testing
  instance_type             = "t2.micro"
  key_pair_name             = "test-key"
}

# Test input variables
run "verify_input_variables" {
  command = plan

  # Check that the required variables are set
  assert {
    condition     = var.vpc_cidr_block != null
    error_message = "VPC CIDR block is not set"
  }

  assert {
    condition     = length(var.private_subnet_cidr_blocks) > 0
    error_message = "Private subnet CIDR blocks are not set"
  }

  assert {
    condition     = length(var.public_subnet_cidr_blocks) > 0
    error_message = "Public subnet CIDR blocks are not set"
  }

  assert {
    condition     = length(var.availability_zones) > 0
    error_message = "Availability zones are not set"
  }

  assert {
    condition     = var.my_ip_cidr != null
    error_message = "my_ip_cidr is not set"
  }

  assert {
    condition     = var.ami_id != null
    error_message = "AMI ID is not set"
  }

  assert {
    condition     = var.instance_type != null
    error_message = "Instance type is not set"
  }

  assert {
    condition     = var.key_pair_name != null
    error_message = "Key pair name is not set"
  }
}

# Test module structure
run "verify_module_structure" {
  command = plan

  # Verify that the modules are correctly structured
  assert {
    condition     = module.vpc != null
    error_message = "VPC module is not defined"
  }

  assert {
    condition     = module.security != null
    error_message = "Security module is not defined"
  }

  assert {
    condition     = module.ec2 != null
    error_message = "EC2 module is not defined"
  }
}

# Test VPC module configuration
run "verify_vpc_configuration" {
  command = plan

  # Verify VPC module configuration
  assert {
    condition     = module.vpc.vpc_cidr_block == var.vpc_cidr_block
    error_message = "VPC CIDR block output does not match input"
  }
}
