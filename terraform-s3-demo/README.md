# Session 18 — Terraform S3 demo

**Suhani Awasthi · 24BCS10260**

The project provisions a uniquely suffixed S3 bucket, blocked public access, versioning, AES256 server-side encryption and BucketOwnerEnforced ownership. provider.tf declares AWS/random providers; variables.tf exposes region/prefix/cleanup policy; terraform.tfvars holds non-secret classroom defaults; main.tf defines resources; outputs.tf returns bucket identifiers. Tests use mocked providers and cannot create AWS resources.

```bash
cd terraform-s3-demo
terraform init
terraform test
```

## Execution workflow — for the later cloud session

Configure AWS credentials locally through an AWS profile/SSO; never put access keys in tfvars or Git. Set `AWS_PROFILE` and review `aws sts get-caller-identity` before provisioning.

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan -out=lab.tfplan
terraform show lab.tfplan
terraform apply lab.tfplan
terraform show
terraform output
# After verification and evidence capture:
terraform plan -destroy -out=destroy.tfplan
terraform apply destroy.tfplan
```

`init` resolves providers and state backend; `fmt` formats HCL; `validate` checks consistency; `plan` previews changes; `apply` changes AWS; `show` inspects state/plan; `output` extracts declared values; a destroy plan tears down managed resources. `terraform destroy` is the interactive shortcut for the final two commands.

Local state may contain sensitive metadata. State, saved plans, provider caches and local.auto.tfvars are ignored; commit provider lock files. Never copy someone else's state or run destroy against unrelated infrastructure. Bucket deletion fails while versioned objects remain unless you explicitly empty all versions or opt into force_destroy for disposable lab data. Cloud charges and credentials require the user's later input. No AWS apply/destroy has been run for this submission preparation.

After apply, verify bucket encryption, public-access block and versioning in the console or AWS CLI. Capture those checks plus plan/apply/output/destroy results later.
References: https://developer.hashicorp.com/terraform/language and https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
