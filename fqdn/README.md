# Fully qualified domain names

An FQDN specifies a complete DNS name; a final dot explicitly denotes the DNS root. Kubernetes Services normally follow `<service>.<namespace>.svc.<cluster-domain>`. `cluster.local` is conventional, not mandatory.

For this lab: `webapp-clusterip.devops-services.svc.cluster.local.`. Within devops-services, use `webapp-clusterip`; from another namespace use `webapp-clusterip.devops-services` or the full name. The Pod resolver's search domains expand short names. A ClusterIP name resolves to a virtual Service IP; traffic then uses the Service port. Headless Services resolve ready endpoint IPs; ExternalName returns a CNAME.

After the Services lab setup:
```bash
kubectl --context minikube -n devops-services exec dns -- cat /etc/resolv.conf
kubectl --context minikube -n devops-services exec dns -- nslookup webapp-clusterip
kubectl --context minikube -n devops-services exec dns -- nslookup webapp-clusterip.devops-services.svc.cluster.local
kubectl --context minikube -n devops-services exec client -- curl -fsS http://webapp-clusterip.devops-services.svc.cluster.local:9090
```
Namespace-qualified names prevent resolving a same-named Service in the wrong namespace. Record actual lookup and HTTP results later.
Reference: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
