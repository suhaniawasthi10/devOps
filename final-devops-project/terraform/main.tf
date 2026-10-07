module "cloud" {
  source               = "../../modules/cloud-lab"
  project_name         = "suhani-final-devops"
  region               = var.region
  admin_cidr           = var.admin_cidr
  key_name             = var.key_name
  enable_k3s           = true
  instance_type        = var.instance_type
  force_destroy_bucket = var.force_destroy_bucket
}
