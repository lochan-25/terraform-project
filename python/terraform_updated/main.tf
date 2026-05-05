# 🔥 Get latest AMI (fixes your previous error)
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# ✅ EC2
resource "aws_instance" "ec2" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  tags = {
    Name = "jenkins-ec2"
  }
}

# ✅ EBS Volume
resource "aws_ebs_volume" "ebs" {
  availability_zone = aws_instance.ec2.availability_zone
  size              = 8

  tags = {
    Name = "jenkins-ebs"
  }
}

# Attach EBS
resource "aws_volume_attachment" "attach" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.ebs.id
  instance_id = aws_instance.ec2.id
}

# ✅ S3 Bucket
resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name

  tags = {
    Name = "jenkins-s3"
  }
}