mock_provider "aws" {}
mock_provider "random" {}
run "private_versioned_bucket" {
  command = plan
  assert {
    condition     = aws_s3_bucket_public_access_block.demo.block_public_policy && aws_s3_bucket_public_access_block.demo.block_public_acls
    error_message = "Public access must remain blocked."
  }
  assert {
    condition     = aws_s3_bucket_versioning.demo.versioning_configuration[0].status == "Enabled"
    error_message = "Bucket versioning must be enabled."
  }
  assert {
    condition     = !aws_s3_bucket.demo.force_destroy
    error_message = "Deleting object versions must be opt-in."
  }
}
