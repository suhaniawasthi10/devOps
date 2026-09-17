# NodePort

**Status: execution and screenshots pending.** Complete the [shared setup](../README.md) first.
Run from the repository root.

This example uses Service port 9090, target port `http` (80), and node port 30090.
The node port is in Kubernetes' default NodePort range, 30000–32767.

```bash
kubectl --context minikube apply -f "Kubernetes Services/NodePort/webapp-nodeport.yaml"
kubectl --context minikube -n devops-services get svc webapp-nodeport -o wide
kubectl --context minikube -n devops-services exec client -- curl -fsS --max-time 10 http://webapp-nodeport:9090
minikube -p minikube ssh -- 'curl -fsS --max-time 10 http://127.0.0.1:30090'
minikube -p minikube service webapp-nodeport -n devops-services --url
```

On macOS with the Docker driver, use the URL printed by the final command in a browser.
Keep that terminal open while accessing it; do not hard-code a node IP or a tunnel port from
someone else's run. The in-node curl check also depends on the node's NodePort address rules;
record and investigate any failure rather than treating the expected output as observed.

## Actual results and screenshot

Pending. Capture the mapping and page as `Kubernetes Services/screenshots/nodeport.png`.
Stop the URL tunnel with Ctrl+C after capturing evidence.
