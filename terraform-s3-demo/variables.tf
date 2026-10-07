variable "region" {
  type    = string
  default = "ap-south-1"
}
variable "bucket_prefix" {
  type    = string
  default = "suhani-24bcs10260-devops"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,39}$", var.bucket_prefix))
    error_message = "Use a DNS-compatible lowercase prefix of 3–40 characters."
  }
}
variable "force_destroy" {
  type    = bool
  default = false
}
