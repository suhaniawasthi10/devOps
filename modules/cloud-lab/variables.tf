variable "project_name" {
  type    = string
  default = "suhani-devops-lab"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.project_name))
    error_message = "Use 3–30 lowercase letters, digits and hyphens, beginning with a letter."
  }
}
variable "region" {
  type    = string
  default = "ap-south-1"
}
variable "admin_cidr" {
  type        = string
  default     = "127.0.0.1/32"
  description = "Replace with your public IPv4 /32 before apply. Never defaults to world access."
  validation {
    condition     = can(cidrhost(var.admin_cidr, 0)) && can(regex("/32$", var.admin_cidr))
    error_message = "admin_cidr must be a valid single-address IPv4 /32."
  }
}
variable "instance_type" {
  type    = string
  default = "t3.micro"
}
variable "key_name" {
  type        = string
  default     = null
  description = "Optional existing EC2 key pair. Without it, use Session Manager; SSH ingress stays closed."
}
variable "enable_k3s" {
  type    = bool
  default = false
}
variable "k3s_version" {
  type    = string
  default = "v1.34.1+k3s1"
}
variable "force_destroy_bucket" {
  type        = bool
  default     = false
  description = "Keep false unless intentionally deleting all versions of disposable lab objects."
}
