# AWS CloudFormation Templates

This directory contains CloudFormation templates that implement the required AWS infrastructure with modular components.

## Architecture Overview

The infrastructure includes:

1. **VPC Infrastructure**:
   - Public and Private Subnets
   - Internet Gateway for Public Subnet
   - NAT Gateway for Private Subnet
   - Default Security Group for VPC

2. **Route Tables**:
   - Public Route Table (routing through Internet Gateway)
   - Private Route Table (routing through NAT Gateway)

3. **Security Groups**:
   - Public EC2 Security Group (allowing SSH from specific IP)
   - Private EC2 Security Group (allowing connections from Public EC2)

4. **EC2 Instances**:
   - Public instance (accessible from internet)
   - Private instance (only accessible from Public instance)

## Template Structure

The CloudFormation templates are organized as modules:

- **vpc.yaml**: Creates the VPC, subnets, Internet Gateway, NAT Gateway, and route tables
- **security.yaml**: Creates security groups for EC2 instances
- **ec2.yaml**: Creates EC2 instances in public and private subnets
- **main.yaml**: Main template that orchestrates the deployment of all components

## Deployment Instructions

### Prerequisites

1. AWS CLI installed and configured with appropriate credentials
2. An existing EC2 Key Pair for SSH access

### Deployment Steps

1. Upload all template files to an S3 bucket (or use local files if deploying from AWS Console)

2. Deploy the stack using AWS CLI:

```bash
aws cloudformation create-stack \
  --stack-name my-vpc-stack \
  --template-body file://main.yaml \
  --parameters \
    ParameterKey=VpcCIDR,ParameterValue=10.0.0.0/16 \
    ParameterKey=PublicSubnetCIDR,ParameterValue=10.0.1.0/24 \
    ParameterKey=PrivateSubnetCIDR,ParameterValue=10.0.2.0/24 \
    ParameterKey=AvailabilityZone,ParameterValue=us-east-1a \
    ParameterKey=AllowedSSHIP,ParameterValue=YOUR_IP_ADDRESS/32 \
    ParameterKey=KeyName,ParameterValue=YOUR_KEY_PAIR_NAME \
    ParameterKey=InstanceType,ParameterValue=t2.micro \
  --capabilities CAPABILITY_IAM
```

Replace `YOUR_IP_ADDRESS/32` with your IP address in CIDR notation and `YOUR_KEY_PAIR_NAME` with the name of your EC2 Key Pair.

### Accessing the Instances

1. **Public Instance**: You can SSH directly to the public instance using its public IP:
   ```bash
   ssh -i your-key.pem ec2-user@PUBLIC_IP
   ```

2. **Private Instance**: You need to SSH to the public instance first, then SSH to the private instance:
   ```bash
   # From your local machine
   ssh -i your-key.pem ec2-user@PUBLIC_IP
   
   # From the public instance
   ssh -i your-key.pem ec2-user@PRIVATE_IP
   ```

## Security Considerations

- The public EC2 instance is only accessible via SSH from the IP specified in the `AllowedSSHIP` parameter
- The private EC2 instance is only accessible from the public EC2 instance
- All resources are tagged for better management
- The NAT Gateway allows private instances to access the internet while remaining secure

## Testing with TaskCat

This project includes TaskCat configuration for testing CloudFormation templates. TaskCat is an AWS tool that tests CloudFormation templates across multiple AWS regions.

### Test Structure

- `.taskcat.yml` - Main configuration file that defines test scenarios for each template
- `ci/taskcat_inputs.json` - Input parameters for the tests
- `ci/vpc_test.py`, `ci/security_test.py`, `ci/ec2_test.py`, `ci/main_test.py` - Python unit tests for each template
- `run-tests.sh` - Script to install TaskCat and run the tests

### Running Tests

To run the tests, execute the following command:

```bash
./run-tests.sh
```

This will:
1. Install TaskCat if not already installed
2. Run the TaskCat tests defined in `.taskcat.yml`
3. Generate a report of the test results

### Test Coverage

The tests verify:
- VPC creation with public and private subnets
- Internet Gateway and NAT Gateway setup
- Route table configurations
- Security group rules for public and private instances
- EC2 instance placement and connectivity
- End-to-end infrastructure validation

### Prerequisites for Testing

- AWS CLI installed and configured with appropriate credentials
- Python 3.6+ with boto3 installed
- Permissions to create and delete CloudFormation stacks in your AWS account
