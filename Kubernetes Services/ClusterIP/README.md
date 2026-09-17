# ClusterIP

**Status: execution and screenshots pending.** Complete the [shared setup](../README.md) first.
Run from the repository root.

ClusterIP provides a stable in-cluster address. The selector matches the Pod's labels;
`port: 9090` is the Service port, and `targetPort: http` resolves to the Pod's named port 80.

```bash
kubectl --context minikube apply -f "Kubernetes Services/ClusterIP/webapp-clusterip.yaml"
kubectl --context minikube -n devops-services get svc webapp-clusterip -o wide
kubectl --context minikube -n devops-services get endpointslices -l kubernetes.io/service-name=webapp-clusterip
kubectl --context minikube -n devops-services exec client -- curl -fsS --max-time 10 http://webapp-clusterip:9090
kubectl --context minikube -n devops-services exec client -- curl -fsS --max-time 10 http://webapp-clusterip.devops-services.svc.cluster.local:9090
kubectl --context minikube -n devops-services exec dns -- nslookup webapp-clusterip.devops-services.svc.cluster.local
```

Expected: HTTP serves the lab page, DNS returns the Service address, and the EndpointSlice
identifies the webapp Pod on port 80. Save `screenshots/clusterip.png` in the Services module.

## Deliberately broken selector

```bash
kubectl --context minikube apply -f "Kubernetes Services/ClusterIP/webapp-clusterip-typo.yaml"
kubectl --context minikube -n devops-services describe svc webapp-typo
kubectl --context minikube -n devops-services get endpointslices -l kubernetes.io/service-name=webapp-typo
kubectl --context minikube -n devops-services exec client -- curl -v --max-time 5 http://webapp-typo:9090
```

Expected: `app: webap` matches no Pod and the HTTP check fails. The exact failure can depend
on the dataplane; use selectors and EndpointSlices to diagnose it instead of assuming one curl
exit code. Capture `screenshots/no-endpoints.png`, then remove the intentionally broken Service:

```bash
kubectl --context minikube delete -f "Kubernetes Services/ClusterIP/webapp-clusterip-typo.yaml"
```

## Actual results

Pending the practical session.
