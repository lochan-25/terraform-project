output "snapshot_id" {
  value       = aws_ebs_snapshot.example.id
  description = "ID of the created EBS snapshot."
}
