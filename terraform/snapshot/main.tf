resource "aws_ebs_snapshot" "example" {
  volume_id = var.volume_id

  tags = {
    Name = "terraform-example"
  }
}