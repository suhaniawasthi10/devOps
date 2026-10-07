# Monitoring: metrics, logs, alerts and application health

Deploy Notes into devops-final first, then run from the root:
```bash
kubectl --context minikube apply -f final-devops-project/monitoring/stack.yaml
kubectl --context minikube -n devops-observe rollout status deploy/prometheus --timeout=180s
kubectl --context minikube -n devops-observe rollout status deploy/alertmanager --timeout=180s
kubectl --context minikube -n devops-observe port-forward svc/prometheus 9090:9090
# Another terminal:
kubectl --context minikube -n devops-observe port-forward svc/alertmanager 9093:9093
```
Open localhost:9090/targets, localhost:9090/alerts and localhost:9093. Prometheus discovers each annotated Notes Pod in devops-final/devops-gitops using namespace-scoped read-only RBAC. It scrapes actual `/metrics` endpoints and loads alert rules from a separate file. Alertmanager groups visible alerts; no email/Slack receiver is configured, so nothing is sent externally.

| Query | Meaning |
|---|---|
| `sum(rate(notes_requests_total[2m]))` | Request rate per second |
| `rate(process_cpu_seconds_total{job="notes-pods"}[2m]) * 100` | CPU percentage of one core per process |
| `process_resident_memory_bytes{job="notes-pods"}` | Process RSS memory |
| `histogram_quantile(0.95, sum by (le) (rate(notes_request_seconds_bucket[5m])))` | Approximate p95 latency |
| `up{job="notes-pods"}` | Successful scrape (not a complete end-to-end health test) |

Generate requests to `/` and `/work`; view changing metrics, `kubectl top pods -n devops-final` (metrics-server required), and `kubectl logs -n devops-final deploy/notes`. Application logs include route, response status and request ID, without request bodies/API keys. Readiness queries SQLite while liveness checks process responsiveness.

For a controlled unavailable alert on the direct Helm release, first disable HPA with a Helm upgrade; scale notes to zero in the disposable lab namespace, wait for NotesUnavailable to fire, then restore one replica and verify resolution. Do this before enabling GitOps self-heal, which would restore replicas. Record the actual firing/resolved states later.

`stack.yaml` embeds the three source configuration files. `scripts/validate.py` checks they stay synchronized. The Prometheus/Alertmanager storage uses emptyDir and is intentionally ephemeral with a six-hour metric retention setting. This is a lightweight lab, not a durable production monitoring service. Cleanup: delete only devops-observe after evidence; namespace-scoped discovery Roles/Bindings can be removed with their application namespaces later.

References: https://prometheus.io/docs/prometheus/latest/configuration/configuration/ and https://prometheus.io/docs/alerting/latest/overview/
