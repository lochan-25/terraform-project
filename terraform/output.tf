output "instance_public_ip" {
  value       = module.ec2_instance.instance_public_ip
  description = "Public IP of the created EC2 instance."
}

output "ebs_volume_id" {
  value       = module.ebs_volume.volume_id
  description = "ID of the created EBS volume."
}

output "elastic_ip" {
  value       = module.elastic_ip.public_ip
  description = "Elastic IP address allocated to the EC2 instance."
}

output "snapshot_id" {
  value       = module.snapshot.snapshot_id
  description = "Snapshot ID created from the EBS volume."
}