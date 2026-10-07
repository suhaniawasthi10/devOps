#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
context=${KUBE_CONTEXT:-minikube}
case_name=${1:?Usage: lab.sh CASE introduce|fix}
action=${2:?Usage: lab.sh CASE introduce|fix}
case "$case_name" in crash-loop|image-pull|pending|container-creating|configuration|service|dns|network) ;; *) echo 'Unknown case' >&2; exit 2;; esac
case "$action" in introduce) file=before;; fix) file=after;; *) echo 'Use introduce or fix' >&2; exit 2;; esac
ns="devops-trouble-$case_name"
kubectl --context "$context" create namespace "$ns" --dry-run=client -o yaml | kubectl --context "$context" apply -f -
if [ "$case_name" = dns ] && [ "$action" = fix ]; then
  kubectl --context "$context" -n "$ns" delete pod dns-client --ignore-not-found
fi
kubectl --context "$context" -n "$ns" apply -f "kubernetes-troubleshooting/cases/$case_name/$file.yaml"
kubectl --context "$context" -n "$ns" get pods,svc -o wide
kubectl --context "$context" -n "$ns" get events --sort-by=.metadata.creationTimestamp
if [ "$action" = fix ] && [ "$case_name" != dns ]; then
  kubectl --context "$context" -n "$ns" rollout status "deployment/trouble-$case_name" --timeout=180s
fi
printf 'Inspect and capture: kubectl --context %s -n %s describe pods\n' "$context" "$ns"
