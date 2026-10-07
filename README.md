# DevOps Coursework

**Suhani Awasthi · 24BCS10260**

Course exercises from Linux fundamentals through the final DevOps project. Missing implementations and documentation have been prepared. Screenshots and live cluster/cloud/pipeline evidence will be collected in the final practical session; local validation is recorded separately.

Start with [assignment coverage](ASSIGNMENT-STATUS.md), [validation](VALIDATION.md), and [evidence checklist](EVIDENCE-CHECKLIST.md).

| Module | Work |
|---|---|
| Linux fundamentals | [Notes and practice script](linuxFundamentals/README.md) |
| Shell scripting | [System information script](ShellScripting/README.md) |
| Git | [Commit and cherry-pick exercises](Git/README.md) |
| Networking | [Command explanations and existing screenshots](Networking/README.md) |
| Docker applications | [Six Hello World applications](Docker-Homework.md) |
| Multi-stage Docker | [Build exercise](docker-multistage/Docker-Multistage-Homework.md) |
| Docker networking/storage | [Networks, host networking and bind mounts](Docker-Networking-Volumes/README.md) |
| Kubernetes Fundamentals | [Setup, objects and tutorial](Kubernetes%20Fundamentals/README.md) |
| Session 10 | [Workloads](Kubernetes%20Workloads/README.md), [strategies](Kubernetes%20Workloads/strategies/README.md), [lifecycle](Kubernetes%20Workloads/lifecycle/README.md) |
| Session 11 | [Services](Kubernetes%20Services/README.md), [comparisons](Kubernetes%20Services/comparisons/README.md), [FQDN](fqdn/README.md), [CoreDNS](coredns/README.md) |
| Session 12 | [Ingress, ConfigMaps and Secrets](Kubernetes%20Ingress%20and%20Config/README.md) |
| Session 13 | [Volumes](01-kubernetes-volumes/README.md), [HPA, probes and mini-project](kubernetes-hpa-probes/README.md) |
| Session 14 | [Troubleshooting and mini-project](kubernetes-troubleshooting/README.md) |
| Session 15 | [Helm and Notes chart](Helm/README.md) |
| Session 16 | [Calculator CI/CD](session16-cicd-github-actions/README.md) |
| Session 17 | [DevSecOps pipeline](session17-devsecops-pipeline/README.md) |
| Session 18 | [Terraform S3 and AWS research](session18-terraform-iac/README.md) |
| Session 19 | [Cloud infrastructure](session19-cloud-terraform-in-action/README.md) |
| Session 20 | [Monitoring, observability and GitOps](session20-monitoring-observability-gitops/README.md) |
| Session 21 | [Final Notes project](final-devops-project/README.md) |

## Kubernetes setup

Use macOS, Docker Desktop and a single-node Minikube profile. Run from this repository's root unless a guide says otherwise:
```bash
docker version
kubectl version --client
minikube version
minikube start --driver=docker
minikube status
kubectl --context minikube cluster-info
kubectl --context minikube get nodes -o wide
```
Run modules sequentially, capture observations, then clean up their dedicated namespaces. The Notes application deliberately uses SQLite on one node; it is not a multi-node production database. See the final README for resource/architecture limits and the cloud K3s alternative.

## Local code validation

Use Python 3.13+, Helm and Terraform. Install application/dev dependencies in a virtual environment and PyYAML for the repository checker. Then follow [VALIDATION.md](VALIDATION.md). `scripts/validate.py` performs offline parsing, chart rendering and consistency checks without creating resources. `scripts/local-demo.sh` is explicitly for the later live Minikube run and creates lab resources.

## Sources and authorship

Requirements: the provided assignment Google Doc. Reference organization/examples: https://github.com/Kavya100206/devops . Official Kubernetes, Helm, AWS, Terraform, Prometheus and Argo documentation is linked in the relevant guides. New mini-project code and documentation are original implementations; all runtime proof must come from the student's own environment.
