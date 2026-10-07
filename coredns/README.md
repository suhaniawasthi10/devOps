# CoreDNS

CoreDNS is a DNS server extended by plugins. Kubernetes uses the kubernetes plugin to watch Service/endpoint data and answer cluster names. Pod → cluster DNS Service → CoreDNS → local cluster answer or upstream resolver for external names. Responses are cached according to TTLs.

The kube-system coredns ConfigMap holds a Corefile. Common directives: `kubernetes cluster.local` for cluster records; `forward . /etc/resolv.conf` for upstream requests; `cache` for caching; `errors`, `health`, `ready`, `loop`, `reload` and `loadbalance` for operations. Read the actual configuration rather than replacing it with an assumed default.

```bash
kubectl --context minikube -n kube-system get deploy,pods,svc -l k8s-app=kube-dns
kubectl --context minikube -n kube-system get configmap coredns -o yaml
kubectl --context minikube -n kube-system logs -l k8s-app=kube-dns --tail=40
kubectl --context minikube -n devops-services exec dns -- nslookup kubernetes.default.svc.cluster.local
kubectl --context minikube -n devops-services exec dns -- nslookup example.org
```

Troubleshoot in order: spelling/namespace → Pod resolv.conf and dnsPolicy → kube-dns Service and EndpointSlices → CoreDNS readiness/logs/Corefile → NetworkPolicy allowing UDP/TCP 53 → upstream DNS. NXDOMAIN differs from timeout. If only external names fail, investigate forwarding. If DNS resolves but HTTP fails, inspect Service selectors and ports.
References: https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/ and https://coredns.io/plugins/kubernetes/
