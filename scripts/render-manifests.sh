#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
helm template notes final-devops-project/helm --namespace devops-final -f final-devops-project/helm/values-prod.yaml --skip-tests > final-devops-project/kubernetes/resources.yaml
