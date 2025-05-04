# devops_assignment

## Giới thiệu

Repository này sử dụng **Terraform** để triển khai hạ tầng AWS bao gồm: VPC, các subnet, security group, và EC2 instance (public/private).

## Yêu cầu

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0.0
- Tài khoản AWS với quyền tạo VPC, EC2, Security Group, v.v.

## Hướng dẫn sử dụng

### 1. Clone repository

```bash
git clone <repo-url>
cd devops_assignment
```

### 2. Cấu hình thông tin AWS và biến đầu vào

Tạo file `terraform.tfvars` (hoặc chỉnh sửa file có sẵn) với nội dung ví dụ:

```hcl
aws_region     = "us-west-2"
aws_access_key = "YOUR_ACCESS_KEY"
aws_secret_key = "YOUR_SECRET_KEY"
my_ip_cidr     = "1.2.3.4/32"
ami_id         = "ami-0abcdef1234567890"
instance_type  = "t2.micro"
key_pair_name  = "your-keypair"
```

Các biến khác đã có giá trị mặc định hoặc được định nghĩa trong module.

### 3. Khởi tạo Terraform

```bash
terraform init
```

### 4. Kiểm tra cấu hình

```bash
terraform plan
```

### 5. Triển khai hạ tầng

```bash
terraform apply
```

Nhập `yes` để xác nhận khi được hỏi.

### 6. Kết quả đầu ra

Sau khi chạy xong, Terraform sẽ hiển thị các output như:
- ID của VPC, subnet, security group
- ID của các EC2 instance public/private

## Cấu trúc module

- `modules/vpc`: Tạo VPC, subnet, NAT gateway, route table, default security group.
- `modules/security`: Tạo security group cho EC2 public/private.
- `modules/ec2`: Tạo EC2 instance public và private.

## Lưu ý

- Đảm bảo bạn đã tạo sẵn key pair trên AWS và điền đúng tên vào biến `key_pair_name`.
- Không commit thông tin nhạy cảm (access key, secret key) lên repository.