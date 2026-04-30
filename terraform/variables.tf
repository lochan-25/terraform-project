variable "region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-west-2"
}

variable "instance_type" {
  description = "The EC2 instance type to use."
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
  default     = "ami-0c55b159cbfafe1f0" # Example AMI ID, replace with your own.
}