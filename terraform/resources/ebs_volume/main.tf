resource "aws_ebs_volume" "example" {
  availability_zone = var.availability_zone
  size              = 10

  tags = {
    Name = "terraform-example"
  }
}