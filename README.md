# AWS Infrastructure with Terraform

## Introduction / Giới thiệu

This repository uses **Terraform** to deploy AWS infrastructure including: VPC, subnets, security groups, and EC2 instances (public/private).

Repository này sử dụng **Terraform** để triển khai hạ tầng AWS bao gồm: VPC, các subnet, security group, và EC2 instance (public/private).

## Requirements / Yêu cầu

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0.0
- AWS account with permissions to create VPC, EC2, Security Groups, etc.
- Tài khoản AWS với quyền tạo VPC, EC2, Security Group, v.v.

## Usage / Hướng dẫn sử dụng

### 1. Clone repository

```bash
git clone <repo-url>
cd devops_assignment
```

### 2. Configure AWS credentials and input variables

Create a `terraform.tfvars` file (or modify the existing one) with the following example content:

```hcl
aws_region     = "us-east-1"
my_ip_cidr     = "YOUR_IP_ADDRESS/32"  # e.g., "1.2.3.4/32"
key_pair_name  = "your-keypair"
```

Other variables have default values defined in the modules.

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Review the configuration

```bash
terraform plan
```

### 5. Deploy the infrastructure

```bash
terraform apply
```

Enter `yes` when prompted for confirmation.

### 6. Output

After completion, Terraform will display outputs including:
- VPC, subnet, and security group IDs
- Public and private EC2 instance IDs

## Module Structure / Cấu trúc module

- `modules/vpc`: Creates VPC, subnets, NAT gateway, route tables, and default security group.
- `modules/security`: Creates security groups for public and private EC2 instances.
- `modules/ec2`: Creates public and private EC2 instances.

## Configuration Details / Chi tiết cấu hình

### Default Values / Giá trị mặc định

- Region: `us-east-1`
- Availability Zones: `us-east-1a`, `us-east-1b`
- VPC CIDR: `10.0.0.0/16`
- Public Subnets: `10.0.1.0/24`, `10.0.2.0/24`
- Private Subnets: `10.0.4.0/24`, `10.0.5.0/24`
- Instance Type: `t2.micro`
- AMI ID: `ami-0f88e80871fd81e91` (Amazon Linux 2)

## Notes / Lưu ý

- Ensure you have created an AWS key pair and specified its name in the `key_pair_name` variable.
- Do not commit sensitive information (access keys, secret keys) to the repository.
- Đảm bảo bạn đã tạo sẵn key pair trên AWS và điền đúng tên vào biến `key_pair_name`.
- Không commit thông tin nhạy cảm (access key, secret key) lên repository.