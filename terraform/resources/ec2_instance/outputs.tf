output "instance_public_ip" {
  value       = aws_instance.example.public_ip
  description = "Public IP of the created EC2 instance."
}
