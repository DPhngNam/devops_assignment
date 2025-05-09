resource "aws_security_group" "public_ec2_sg" {
    name        = "public_ec2_sg"
    description = "Security group for public EC2 instances"
    vpc_id      = var.vpc_id
    
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [var.my_ip_cidr]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "Public EC2 Security Group"
    }
}

resource "aws_security_group" "private_ec2_sg" {
    name        = "private_ec2_sg"
    description = "Security group for private EC2 instances"
    vpc_id      = var.vpc_id
    
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        security_groups = [aws_security_group.public_ec2_sg.id]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "Private EC2 Security Group"
    }
}