#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Run intentionally during the practical session; this creates local lab resources.
minikube -p minikube status
kubectl --context minikube get nodes
docker build -f final-devops-project/docker/Dockerfile -t coursework-notes:local final-devops-project
minikube -p minikube image load coursework-notes:local
minikube -p minikube addons enable metrics-server
minikube -p minikube addons enable ingress
helm upgrade --install notes final-devops-project/helm --kube-context minikube -n devops-final --create-namespace -f final-devops-project/helm/values-prod.yaml --wait --timeout 240s
helm test notes --kube-context minikube -n devops-final --logs
kubectl --context minikube apply -f final-devops-project/monitoring/stack.yaml
kubectl --context minikube -n devops-observe rollout status deployment/prometheus --timeout=180s
kubectl --context minikube -n devops-observe rollout status deployment/alertmanager --timeout=180s
kubectl --context minikube -n devops-final get deploy,pods,svc,ingress,hpa,pvc
