output "public_ip" {
  value       = aws_eip.example.public_ip
  description = "Public IP of the Elastic IP."
}
