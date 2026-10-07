terraform {
  required_version = ">= 1.7, < 2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}
provider "aws" {
  region = var.region
  default_tags {
    tags = { Owner = "Suhani Awasthi", Enrollment = "24BCS10260", Purpose = "DevOps coursework" }
  }
}
