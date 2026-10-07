# Deployment strategies — Session 10

Run from the repository root. RollingUpdate is already implemented by the v1/v2 manifests in the parent module: maxSurge 1, maxUnavailable 0, readiness checks and rollback. Watch `get pods -w` in a second terminal during that update to capture overlap between old and new Pods.

```bash
kubectl --context minikube create namespace devops-strategies
kubectl --context minikube -n devops-strategies apply -f "Kubernetes Workloads/strategies"
kubectl --context minikube -n devops-strategies wait --for=condition=Available deployment --all --timeout=180s
kubectl --context minikube -n devops-strategies run client --image=busybox:1.37 --restart=Never --command -- sleep 3600
kubectl --context minikube -n devops-strategies wait --for=condition=Ready pod/client --timeout=180s
kubectl --context minikube -n devops-strategies exec client -- wget -qO- http://blue-green
kubectl --context minikube -n devops-strategies patch svc blue-green -p '{"spec":{"selector":{"track":"green"}}}'
kubectl --context minikube -n devops-strategies exec client -- wget -qO- http://blue-green
kubectl --context minikube -n devops-strategies exec client -- sh -c 'for i in $(seq 1 100); do wget -qO- http://canary; done' | sort | uniq -c
# Terminal 2: watch old Pods disappear before new Pods start.
kubectl --context minikube -n devops-strategies get pods -w
# Terminal 1:
kubectl --context minikube -n devops-strategies apply -f "Kubernetes Workloads/strategies/updates/recreate-v2.yaml"
kubectl --context minikube -n devops-strategies rollout status deployment/recreate
kubectl --context minikube -n devops-strategies exec deploy/recreate -- wget -qO- http://localhost
```

| Strategy | Mechanism | Tradeoff / rollback |
|---|---|---|
| Rolling | Gradually replace replicas after readiness | Overlapping versions; rollout undo |
| Blue-green | Both releases ready; switch Service selector | Double capacity; switch selector back to blue |
| Canary | 3 stable and 1 canary backend share a Service | Approximately 25% of new connections, not guaranteed per-request weighting; scale canary to zero to withdraw |
| Recreate | Stop old replicas before replacement | Downtime; suitable when overlap is undesirable |

The canary test counts independent connections. Keep-alive, connection affinity and small samples can skew the ratio. A traffic-management controller is needed for exact weighted routing.

Expected outcomes are described above; observations/screenshots remain pending. Cleanup: `kubectl --context minikube delete namespace devops-strategies`.
Reference: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
