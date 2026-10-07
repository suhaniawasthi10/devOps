variable "region" {
  type    = string
  default = "ap-south-1"
}
variable "admin_cidr" {
  type    = string
  default = "127.0.0.1/32"
}
variable "key_name" {
  type    = string
  default = null
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}
variable "force_destroy_bucket" {
  type    = bool
  default = false
}
