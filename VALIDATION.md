# Local validation results

Validated on 7 October 2026. These are actual local checks of the authored implementation. They are not substitutes for the later assignment screenshots, Kubernetes practical session, GitHub Actions run or AWS execution.

| Check | Actual result |
|---|---|
| Notes application tests | 11 passed |
| Session 16 calculator tests | 10 passed |
| Bandit SAST on Notes application | Passed; no issues reported |
| pip-audit on pinned Notes runtime dependencies | No known vulnerabilities found at validation time |
| Notes multi-stage Docker build | Passed on local arm64 Docker Desktop |
| Notes container smoke test | Passed: HTTP/readiness, API-key enforcement, non-root UID 10001, read-only root filesystem, metrics and note persistence after container recreation |
| Repository checker | 79 YAML files parsed, 8 shell scripts syntax-checked, 113 local documentation links checked; chart/snapshot/monitoring consistency passed |
| Helm chart | Lint passed; default, production-demo and external-secret/ephemeral-storage render variants passed |
| Kubernetes/Argo JSON schemas | 113 resources valid; 0 invalid, 0 errors, 0 skipped against Kubernetes 1.34 and Argo schemas |
| Actionlint | All three active GitHub Actions workflows passed |
| Terraform formatting | Passed |
| Terraform validate | Passed for S3, cloud-lab module, Session 19 and final-project roots |
| Terraform mocked tests | S3: 1 passed; cloud module: 2 passed; no AWS resources created |
| Prometheus promtool | Configuration and all 3 alert rules passed |
| Git whitespace check | Passed |

Tools used: Python 3.13, Helm 4.3.0, Terraform 1.13.5, AWS provider 6.67.0, random provider 3.9.1, Actionlint 1.7.12, Kubeconform 0.8.0, Prometheus/promtool 3.15.0. Provider lock files are included. Downloaded validators and the Python environment were kept under /tmp rather than installed globally during this work.

## Reproduce the checks

From repository root, install the Notes dev requirements and PyYAML into an activated Python 3.13 environment. Install Helm and the named validation tools through their official distributions.

```bash
python -m pytest -q final-devops-project/application
(cd session16-cicd-github-actions && python -m pytest -q tests)
python scripts/validate.py
bandit -r final-devops-project/application -x final-devops-project/application/test_app.py -c final-devops-project/security/bandit.yaml
pip-audit -r final-devops-project/application/requirements.txt
helm lint final-devops-project/helm
actionlint
terraform fmt -check -recursive
```

For each Terraform root/module, run `terraform init -backend=false`, then `terraform validate`; run `terraform test` in terraform-s3-demo and modules/cloud-lab. Their tests explicitly mock AWS/random providers and do not require an AWS account.

```bash
docker build -f final-devops-project/docker/Dockerfile -t coursework-notes:local final-devops-project
python scripts/container-smoke.py coursework-notes:local
docker run --rm --entrypoint /bin/promtool -v "$PWD/final-devops-project/monitoring:/etc/prometheus:ro" prom/prometheus:v3.15.0 check config /etc/prometheus/prometheus.yml
```

The smoke script creates uniquely named disposable containers/volume and removes only its own resources. No screenshots were generated, no cluster was started, no GitHub workflow was triggered, no image was published and no AWS infrastructure was applied. Full-history Gitleaks and Trivy image scans are wired into the pipeline but have not been executed as part of these local checks. All later run evidence remains listed in EVIDENCE-CHECKLIST.md.
