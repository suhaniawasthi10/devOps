# Headless Service

**Status: execution and screenshots pending.** Complete the [shared setup](../README.md) and
ClusterIP exercise first. Run from the repository root.

`clusterIP: None` removes the virtual Service IP. With a selector, DNS can return the ready
backing Pods' addresses directly. Clients connect to the actual container port, 80 here.

```bash
kubectl --context minikube apply -f "Kubernetes Services/Headless/webapp-headless.yaml"
kubectl --context minikube -n devops-services get svc webapp-headless
kubectl --context minikube -n devops-services get endpointslices -l kubernetes.io/service-name=webapp-headless
kubectl --context minikube -n devops-services get pod webapp -o wide
kubectl --context minikube -n devops-services exec dns -- nslookup -type=a webapp-headless.devops-services.svc.cluster.local
kubectl --context minikube -n devops-services exec dns -- nslookup -type=a webapp-clusterip.devops-services.svc.cluster.local
kubectl --context minikube -n devops-services exec client -- curl -fsS --max-time 10 http://webapp-headless:80
```

Expected: headless DNS returns the webapp Pod IP; ClusterIP DNS returns its Service IP.
A headless Service does not proxy port 9090 to port 80 for ordinary A-record connections.

## Actual results and screenshot

Pending. Save `Kubernetes Services/screenshots/headless.png`.
