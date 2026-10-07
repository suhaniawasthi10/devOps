# GitOps with Argo CD

Git records desired configuration. Argo CD pulls the repository, renders the Notes chart and reconciles the cluster. Self-heal corrects manual drift; prune removes resources deleted from desired state, except the deliberately retained Notes PVC. Deployment replicas are ignored when HPA manages scaling.

Prerequisites: push these files to main, have a working local cluster, load coursework-notes:local, and enable ingress/metrics-server. An Application pointing to files that have not been pushed cannot sync.

```bash
kubectl --context minikube create namespace argocd
kubectl --context minikube apply --server-side -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/install.yaml
kubectl --context minikube -n argocd rollout status deploy/argocd-server --timeout=300s
kubectl --context minikube apply -f final-devops-project/gitops/project.yaml
kubectl --context minikube apply -f final-devops-project/gitops/application.yaml
kubectl --context minikube -n argocd get application coursework-notes -w
kubectl --context minikube -n devops-gitops get deploy,pods,svc,hpa,pvc
```

The AppProject limits source repository and destination namespace/resource kinds. Monitor Healthy/Synced status; inspect Application conditions and controller logs for repository, image or permission errors. The local image starts the demonstration without registry credentials. On a different node, publish and promote an appropriate image first.

## Demonstrate reconciliation

```bash
kubectl --context minikube -n devops-gitops set env deployment/notes ENVIRONMENT=manual-drift
kubectl --context minikube -n devops-gitops get deployment notes -w
kubectl --context minikube -n argocd get application coursework-notes
```
Argo should remove the extra explicit environment override and restore Git's configuration. Record drift and recovery; do not count ordinary ReplicaSet replacement as proof of GitOps reconciliation.

## Promote and roll back an image

After the DevSecOps workflow publishes a successful image, run `python3 scripts/promote-image.py <full-commit-sha>` from root, review the diff, then commit/push the values change. Argo pulls that desired tag. Revert the promotion commit to roll back through Git. Use a published image matching the node architecture: the hosted CI image is amd64; Apple Silicon local builds are arm64.

GHCR packages must be readable from the cluster. Set the classroom package public or configure an imagePullSecret and chart imagePullSecrets. On the Terraform K3s cluster, add `../gitops/values-cloud.yaml` after values.yaml in Application valueFiles for Traefik, and use the published image. Do not let direct Helm commands and Argo manage the same release/namespace.

Cleanup after evidence: delete the Application (no cascading finalizer is installed here), then explicitly delete disposable devops-gitops resources/namespace after deciding what to do with notes data. Remove the AppProject and Argo installation only if no other applications use them. Cloud instance teardown requires separate Terraform cleanup.
Reference: https://argo-cd.readthedocs.io/en/stable/getting_started/
