# Final troubleshooting challenge

Use the directly managed devops-final release. Do not inject these faults into the GitOps release, where reconciliation can immediately undo them. Run scripts from repository root.

Introduce `image`, `readiness` and `service` faults with `bash final-devops-project/troubleshooting/faults.sh <case>`. They may be introduced together for the final challenge. Investigate each independently before recovery.

| Symptom to investigate | Root cause introduced | Evidence | Repair |
|---|---|---|---|
| New rollout stalls; old Pods may still serve | Invalid image tag | Pod Events, image name, rollout status | Restore local/published known-good tag |
| New Pod runs but remains unready | Readiness path returns 404 | describe probe failures, endpoint readiness, application logs | Restore /readyz |
| Service requests fail while Pod checks succeed | targetPort 9999 has no listener | Service YAML, EndpointSlice port, direct Pod HTTP | Restore named http target |

```bash
kubectl --context minikube -n devops-final get pods -o wide
kubectl --context minikube -n devops-final describe pods
kubectl --context minikube -n devops-final get events --sort-by=.metadata.creationTimestamp
kubectl --context minikube -n devops-final logs deploy/notes --tail=30
kubectl --context minikube -n devops-final get svc notes -o yaml
kubectl --context minikube -n devops-final get endpointslices
bash final-devops-project/troubleshooting/faults.sh recover
```
Recovery reapplies the correct Helm template and runs an HTTP test. Finish by reopening the app, checking a saved note, Prometheus target health, and actual version/configuration. Keep a table of observed symptoms, hypotheses, confirming commands, fixes and before/after outputs. No successful recovery is claimed before the practical run.
