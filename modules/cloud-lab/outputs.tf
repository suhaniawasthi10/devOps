output "instance_id" { value = aws_instance.web.id }
output "public_ip" { value = aws_instance.web.public_ip }
output "web_url" { value = "http://${aws_instance.web.public_ip}" }
output "vpc_id" { value = aws_vpc.lab.id }
output "bucket_name" { value = aws_s3_bucket.assets.bucket }
output "kubernetes_endpoint" { value = var.enable_k3s ? "https://${aws_instance.web.public_ip}:6443" : null }
