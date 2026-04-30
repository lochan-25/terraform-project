provider "aws" {
  region = var.region
}

module "ec2_instance" {
  source        = "./resources/ec2_instance"
  ami_id        = var.ami_id
  instance_type = var.instance_type
}

module "ebs_volume" {
  source            = "./resources/ebs_volume"
  availability_zone = "${var.region}a"
}

module "elastic_ip" {
  source = "./resources/elastic_ip"
}

module "snapshot" {
  source    = "./snapshot"
  volume_id = module.ebs_volume.volume_id
}