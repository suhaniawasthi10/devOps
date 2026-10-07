# Final-project infrastructure

This root configuration reuses [cloud-lab](../../modules/cloud-lab), enabling a pinned K3s server on an encrypted t3.small instance. VPC, subnet, routing, IAM, security groups and S3 are managed by Terraform. Pod/service CIDRs are separate from the VPC CIDR. K3s provides local-path storage, metrics-server and Traefik; use ingress.className=traefik for the cloud deployment. The Minikube chart profile uses nginx instead.

Follow the [Session 19 workflow](../../session19-cloud-terraform-in-action/README.md), with AWS_PROFILE, actual admin_cidr and spending approval supplied later. Inspect cloud-init and `sudo k3s kubectl get nodes` through Session Manager. Kubeconfig remains on the instance at /etc/rancher/k3s/k3s.yaml, mode restricted by K3s; Terraform does not output it. For external access securely obtain it, change its server to the output endpoint and keep it outside Git. The certificate includes the instance public IP.

The final chart's SQLite/RWO storage suits this single-node classroom architecture. There is no HA database or multi-node scheduling guarantee. Data survives Pod recreation but not instance/volume destruction unless backed up. S3 is available for backups via the scoped instance role; no automatic backup is claimed.

After publishing an image, deploy the chart from the machine or use Argo CD with the cloud values override. Restrict API reachability to the configured /32. A GitHub-hosted runner normally will not match that IP; use a reachable controlled runner or pull-based GitOps instead of opening 6443 globally. Cloud execution and evidence are deferred.
