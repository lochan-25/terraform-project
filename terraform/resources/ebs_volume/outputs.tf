output "volume_id" {
  value       = aws_ebs_volume.example.id
  description = "ID of the created EBS volume."
}
