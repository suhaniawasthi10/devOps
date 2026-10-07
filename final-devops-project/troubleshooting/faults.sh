#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
case "${1:-}" in
  image)
    kubectl --context minikube -n devops-final set image deployment/notes notes=coursework-notes:no-such-tag-coursework
    ;;
  readiness)
    kubectl --context minikube -n devops-final patch deployment notes --type=json -p='[{"op":"replace","path":"/spec/template/spec/containers/0/readinessProbe/httpGet/path","value":"/does-not-exist"}]'
    ;;
  service)
    kubectl --context minikube -n devops-final patch svc notes --type=json -p='[{"op":"replace","path":"/spec/ports/0/targetPort","value":9999}]'
    ;;
  recover)
    # Restore only the dedicated local lab release. Do not use on a GitOps-managed namespace.
    helm upgrade notes final-devops-project/helm --kube-context minikube -n devops-final -f final-devops-project/helm/values-prod.yaml --wait --timeout 240s
    helm test notes --kube-context minikube -n devops-final --logs
    ;;
  *) echo 'Usage: faults.sh image|readiness|service|recover' >&2; exit 2 ;;
esac
kubectl --context minikube -n devops-final get pods,svc,endpointslices
