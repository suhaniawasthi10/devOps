# Practical-session evidence checklist

Code/configuration preparation is separate from proof of execution. Screenshots and account-dependent runs are deferred at the user's request. Save actual outputs using `bash scripts/capture.sh evidence/<name>.txt <command...>`; never insert sample results as if observed.

| Module | Later evidence required |
|---|---|
| Linux | inode/link behavior; test-user creation and verification on Ubuntu; service journal; command practice |
| Shell | complete system_info.sh run and created processes.txt |
| Docker networks | exact two-network backend; successful Apache host-network HTTP on port 80 |
| Kubernetes basics | cluster status, objects, namespaces and tutorial commands; existing Kubernetes checklist |
| Session 10 | four strategy transitions; old/new Pods; canary request counts; lifecycle phases/details |
| Session 11 | each Service connectivity result; DNS/FQDN/CoreDNS configuration and lookups |
| Session 12 | ConfigMap/Secret injection, controller and routing, troubleshooting before/after |
| Session 13 | emptyDir/hostPath/PV/PVC/StorageClass observations; persistence after Pod deletion; baseline/load/cooldown HPA; probes |
| Session 14 | each fault's symptom, investigation, root cause, fix and successful verification; combined mini-project |
| Session 15 | Helm commands; install → two upgrades → rollback; broken upgrade recovery; Notes persistence |
| Session 16 | GitHub Actions passing run URL, tests/artifact/container; deliberate test failure and recovery |
| Session 17 | security gates, registry image tag/digest, candidate cluster test and published-image deployment |
| Session 18 | AWS S3 plan/apply/show/output/verification/destroy with real account credentials |
| Session 19 | cloud architecture/resources, Nginx HTTP, scoped S3 access and teardown |
| Session 20 | metrics/logs, healthy targets, alert firing/resolution, Argo sync and manual drift correction |
| Session 21 | integrated app/persistence/ingress/HPA, published image deployment, cloud infrastructure, monitoring/GitOps and final troubleshooting |

## Inputs needed at execution time

- AWS profile/account, region, allowed spend and operator public /32; no access keys in Git or chat.
- GitHub push/run authorization and GHCR visibility or pull credentials.
- A Linux systemd environment for user/journal tasks; macOS cannot substitute for those commands.
- Any exact instructor Session 13/14 mini-project brief if the original implementations here must match a prescribed project.
- Choose local Minikube versus AWS K3s and image architecture before image promotion.

The original [Kubernetes checklist](Kubernetes-Checklist.md) remains useful for the first four Kubernetes modules. This table adds the later sessions. Mark a row complete only after checking actual evidence.
