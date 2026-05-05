output "ec2_public_ip" {
  value = aws_instance.ec2.public_ip
}

output "s3_bucket" {
  value = aws_s3_bucket.bucket.id
}