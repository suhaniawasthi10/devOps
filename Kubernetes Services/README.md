# Kubernetes Services

**Name:** Suhani Awasthi

**Enrollment Number:** 24BCS10260

**Status:** Prepared; cluster execution, observed results, and screenshots are pending.

## Goal

Expose the same Nginx Pod through four Service types and a headless configuration.
Headless is a Service configuration (`clusterIP: None`), not a fifth `spec.type` value.
See the [Kubernetes Service documentation](https://kubernetes.io/docs/concepts/services-networking/service/).

Complete [cluster setup](../README.md#kubernetes-setup) first. Run all commands from the repository root.

| Exercise | What to observe |
|---|---|
| [ClusterIP](ClusterIP/README.md) | In-cluster HTTP, DNS, EndpointSlices, and a broken selector |
| [NodePort](NodePort/README.md) | Service port, target port, node port, and access from macOS |
| [LoadBalancer](LoadBalancer/README.md) | Actual external-IP state and the difference between NodePort access and a load balancer |
| [Headless](Headless/README.md) | DNS resolves Pod IPs instead of a Service virtual IP |
| [ExternalName](ExternalName/README.md) | DNS alias to an external hostname |

## 1. Create the common Pod and clients

```bash
kubectl --context minikube create namespace devops-services
kubectl --context minikube apply -f "Kubernetes Services/webapp-pod.yaml"
kubectl --context minikube -n devops-services wait --for=condition=Ready pod/webapp --timeout=180s
kubectl --context minikube -n devops-services run client --image=curlimages/curl:8.11.1 --restart=Never --command -- sleep 86400
kubectl --context minikube -n devops-services run dns --image=busybox:1.37 --restart=Never --command -- sleep 86400
kubectl --context minikube -n devops-services wait --for=condition=Ready pod/client pod/dns --timeout=180s
kubectl --context minikube -n devops-services get pods -o wide --show-labels
```

The manifest includes a ConfigMap containing the page and a Pod mounting it into Nginx.
The Pod label is `app: webapp` and its named port `http` maps to container port 80.
Run the five linked exercises in table order so that later comparisons can use earlier Services.

## 2. Final inspection

After the exercises, capture the combined state:

```bash
kubectl --context minikube -n devops-services get svc
kubectl --context minikube -n devops-services get endpointslices
kubectl --context minikube -n devops-services get pods -o wide
```

## Results and screenshots — pending

All Service exercises share this module's `screenshots/` directory. Capture `webapp-pod.png`,
`clusterip.png`, `no-endpoints.png`, `nodeport.png`, `loadbalancer.png`, `headless.png`,
`externalname.png` and `final-state.png`. Add observations and image links only after the run.

## Cleanup

Stop any `minikube service --url` or `minikube tunnel` process with Ctrl+C first.

```bash
kubectl --context minikube delete namespace devops-services
```
