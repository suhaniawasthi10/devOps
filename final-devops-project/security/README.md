# Security configuration and gates

Bandit scans application sources (tests excluded). pip-audit checks the pinned runtime dependencies. Gitleaks scans Git history with default rules and redacted output. Trivy rejects HIGH/CRITICAL image vulnerabilities. The workflow's dependent stages run only if all preceding gates succeed.

Local commands from root:
```bash
bandit -r final-devops-project/application -x final-devops-project/application/test_app.py -c final-devops-project/security/bandit.yaml
pip-audit -r final-devops-project/application/requirements.txt
docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:v8.30.1 git /repo --redact --config /repo/final-devops-project/security/gitleaks.toml
trivy image --config final-devops-project/security/trivy.yaml coursework-notes:local
```
Only public dummy keys are committed. A real Secret should be created externally and selected through secret.existingName. API mutations use constant-time key comparison and parameterized SQL; the UI displays note text using textContent. The app uses a non-root UID, dropped capabilities and a read-only root filesystem with explicit writable data/tmp volumes.

Limitations: lab HTTP has no TLS, reads are public, SQLite targets one node, and the CPU exercise endpoint is intentionally accessible for load generation. Use local port-forward access for coursework. Before broader deployment add TLS, user authentication, rate limiting and a multi-node database.

## Optional manual-deployment identity

`deployer-rbac.yaml` defines a ServiceAccount and namespace-scoped Role for devops-release. It does not grant cluster-admin. Apply it during deployment setup, obtain a short-lived token with `kubectl -n devops-release create token coursework-deployer --duration=1h`, and use it with the cluster endpoint/CA in an external kubeconfig. Store the base64 file as the coursework environment's KUBE_CONFIG_B64 secret; refresh it when it expires. Keep the kubeconfig out of the repository. Validate with `kubectl auth can-i` using that identity. GitOps does not require this external deployment credential.
