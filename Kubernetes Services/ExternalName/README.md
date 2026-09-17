# ExternalName

**Status: execution and screenshots pending.** Complete the [shared setup](../README.md) first.
Run from the repository root.

ExternalName provides a DNS CNAME alias. It has no Pod selector and does not proxy traffic.
This example aliases an in-cluster name to `example.org`.

```bash
kubectl --context minikube apply -f "Kubernetes Services/ExternalName/webapp-externalname.yaml"
kubectl --context minikube -n devops-services get svc webapp-externalname -o wide
kubectl --context minikube -n devops-services get endpointslices -l kubernetes.io/service-name=webapp-externalname
kubectl --context minikube -n devops-services exec dns -- nslookup webapp-externalname.devops-services.svc.cluster.local
kubectl --context minikube -n devops-services exec client -- curl -sS -D - --max-time 15 -H 'Host: example.org' http://webapp-externalname/
```

Expected: DNS shows a CNAME to `example.org` and there are no Service-managed EndpointSlices.
The HTTP check also depends on external access and the site's response; record the actual status.
DNS aliasing does not rewrite HTTP Host headers or TLS certificate names, which is why this
HTTP example supplies the real hostname explicitly.

## Actual results and screenshot

Pending. Save `Kubernetes Services/screenshots/externalname.png`.
