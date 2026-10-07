# Session 15 — Helm and Notes mini-project

**Suhani Awasthi · 24BCS10260**

The complete custom chart is shared at [final-devops-project/helm](../final-devops-project/helm) so later assignments deploy the same application. It contains Chart.yaml, values.yaml, values-prod.yaml, ConfigMap, Secret, Deployment, Service, PVC, HPA, Ingress and an HTTP test hook. The mini-project packages a functioning persistent Notes API and browser interface, not a renamed Nginx page.

All commands below run from the repository root. Build and load the image using the final-project README first.

## Core commands
```bash
helm version
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm repo list
helm search repo prometheus
# Starter example only; the authored chart is in final-devops-project/helm.
helm create /tmp/coursework-sample-chart
helm lint final-devops-project/helm
helm template notes final-devops-project/helm
helm install notes final-devops-project/helm --kube-context minikube -n devops-helm --create-namespace --wait --timeout 180s
helm list --kube-context minikube -n devops-helm
helm status notes --kube-context minikube -n devops-helm
helm get values notes --kube-context minikube -n devops-helm
helm get manifest notes --kube-context minikube -n devops-helm
helm test notes --kube-context minikube -n devops-helm --logs
```
A chart is a reusable package; a release is one installation; each upgrade/rollback creates a new release revision. Values parameterize templates. `lint` checks the chart and `template` renders it locally; neither proves cluster behavior.

## Install → upgrade → upgrade → rollback

```bash
helm upgrade notes final-devops-project/helm --kube-context minikube -n devops-helm --set app.version=v2 --wait
kubectl --context minikube -n devops-helm get pods
helm test notes --kube-context minikube -n devops-helm --logs
helm upgrade notes final-devops-project/helm --kube-context minikube -n devops-helm --set app.version=v3 --wait
helm history notes --kube-context minikube -n devops-helm
helm rollback notes 2 --kube-context minikube -n devops-helm --wait
helm history notes --kube-context minikube -n devops-helm
kubectl --context minikube -n devops-helm port-forward svc/notes 8080:80
# In another terminal verify the actual version:
curl -fsS http://localhost:8080/api/config
```
The config checksum changes the Pod template when version/configuration changes. On a fresh release revision 2 is v2; inspect history if you have already repeated the exercise. Rollback restores prior manifests, not database contents.

## Mini-project fault recovery and environment overrides

Upgrade using `-f final-devops-project/helm/values-prod.yaml` after enabling metrics-server and ingress. This is a classroom production profile, still restricted to a single-node SQLite design. Save a note, delete a Pod, and verify persistence. Introduce an invalid image using `--set image.tag=no-such-tag-coursework`, inspect Events, then rollback to the last known healthy revision and verify `/readyz` plus the saved note. Capture the unhealthy and recovered states later.

After evidence: `helm uninstall notes --kube-context minikube -n devops-helm`. The PVC is deliberately retained by the chart. Delete `pvc/notes-data` only when you no longer need those lab notes; then delete the namespace.

Original mini-project implementation based on the assignment topic and reference repo's chart structure. Reference: https://helm.sh/docs/ and https://github.com/Kavya100206/devops/tree/main/Helm
