mock_provider "aws" {
  mock_data "aws_availability_zones" {
    defaults = { names = ["ap-south-1a"] }
  }
  mock_data "aws_ami" {
    defaults = { id = "ami-0123456789abcdef0" }
  }
}
mock_provider "random" {}
run "restricted_web_lab" {
  command = plan
  assert {
    condition     = length(aws_vpc_security_group_ingress_rule.ssh) == 0 && length(aws_vpc_security_group_ingress_rule.kubernetes) == 0
    error_message = "SSH and Kubernetes ports should not open in the default web lab."
  }
  assert {
    condition     = aws_instance.web.metadata_options[0].http_tokens == "required" && aws_instance.web.root_block_device[0].encrypted
    error_message = "Require IMDSv2 and encrypted root storage."
  }
}
run "kubernetes_lab" {
  command = plan
  variables {
    enable_k3s = true
  }
  assert {
    condition     = length(aws_vpc_security_group_ingress_rule.kubernetes) == 1 && aws_vpc_security_group_ingress_rule.kubernetes[0].cidr_ipv4 == "127.0.0.1/32"
    error_message = "Kubernetes API access must stay scoped to the configured operator IP."
  }
}
