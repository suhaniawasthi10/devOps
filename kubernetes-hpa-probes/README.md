# Session 13 — HPA, probes and Notes mini-project

Enable the metrics-server addon; CPU utilization is measured against CPU requests, so the application specifies requests. Load the base workload first, then create load separately:
```bash
minikube -p minikube addons enable metrics-server
kubectl --context minikube create namespace devops-hpa
kubectl --context minikube -n devops-hpa apply -f kubernetes-hpa-probes/manifests
kubectl --context minikube -n devops-hpa rollout status deployment/cpu-demo --timeout=180s
kubectl --context minikube -n devops-hpa get hpa
kubectl --context minikube -n devops-hpa top pods
kubectl --context minikube -n devops-hpa apply -f kubernetes-hpa-probes/load-generator.yaml
kubectl --context minikube -n devops-hpa get hpa,pods -w
# After utilization and replica count rise:
kubectl --context minikube -n devops-hpa describe hpa cpu-demo
kubectl --context minikube -n devops-hpa top pods
kubectl --context minikube -n devops-hpa delete pod load-generator
kubectl --context minikube -n devops-hpa get hpa,pods -w
```
Allow time for metric collection and stabilization before concluding scaling failed. Approximately desiredReplicas = ceil(currentReplicas × currentUtilization / targetUtilization), subject to readiness rules, tolerance and bounds. Record baseline, peak and cooldown, not an invented replica count.

Startup probes allow slow initialization; liveness restarts an unhealthy container; readiness removes an unready Pod from Service endpoints without restarting it. The Notes chart implements all three. If readiness fails because storage is unavailable, the process can remain live while traffic is withheld.

## Mini-project: persistent Notes with autoscaling

This is an original implementation based on the assignment topic; the instructor's exact Session 13 mini-project brief was not supplied.

From the root, build `coursework-notes:local` with the final project's Dockerfile and load it using `minikube image load coursework-notes:local`. Install the shared chart:
```bash
helm upgrade --install notes final-devops-project/helm --kube-context minikube --namespace devops-notes --create-namespace --set autoscaling.enabled=true --wait
kubectl --context minikube -n devops-notes port-forward svc/notes 8080:80
```
Open localhost:8080, save a note using the dummy key `coursework-demo-only`, delete one Notes Pod, wait for replacement and confirm the note remains. Inspect PVCs, probes and HPA. Generate load against `/work` to exercise scaling. This SQLite/RWO design targets a single-node cluster; it is not a multi-node database design.

After evidence, remove load; uninstall notes and explicitly delete its retained PVC only if the lab data is no longer needed. Delete devops-hpa after capturing cooldown.
Reference: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
