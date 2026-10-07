# Kubernetes Fundamentals

**Name:** Suhani Awasthi

**Enrollment Number:** 24BCS10260

**Status:** Prepared; cluster execution, observed results, and screenshots are pending.

## Goal and concepts

Inspect a local cluster, run a Pod and use namespaces. Complete the
[setup instructions](../README.md#kubernetes-setup) first. Run these commands from the repository root.

| Component | Responsibility |
|---|---|
| API server | Entry point for Kubernetes API requests |
| etcd | Stores cluster state |
| Scheduler | Assigns unscheduled Pods to nodes |
| Controller manager | Runs controllers that reconcile desired and observed state |
| kubelet | Manages containers for Pods assigned to its node |
| Container runtime | Runs containers, for example containerd |
| kube-proxy or an alternative dataplane | Implements Service traffic forwarding |
| CoreDNS | Provides cluster DNS |

In Minikube, several control-plane components appear as static Pods. The kubelet and
container runtime run as node processes; not every component appears in `get pods`.

## 1. Cluster and system components

```bash
kubectl --context minikube cluster-info
kubectl --context minikube get nodes -o wide
kubectl --context minikube get namespaces
kubectl --context minikube get pods -n kube-system -o wide
kubectl --context minikube describe node minikube
kubectl --context minikube api-resources
```

Compare `Capacity` with `Allocatable`: the latter is the resource budget available for Pods
after system reservations. Record the components actually present in this cluster.

## 2. First Pod

```bash
kubectl --context minikube create namespace devops-fundamentals
kubectl --context minikube -n devops-fundamentals run hello-web --image=nginx:1.27-alpine --port=80
kubectl --context minikube -n devops-fundamentals wait --for=condition=Ready pod/hello-web --timeout=180s
kubectl --context minikube -n devops-fundamentals get pods -o wide
kubectl --context minikube -n devops-fundamentals describe pod hello-web
kubectl --context minikube -n devops-fundamentals exec hello-web -- nginx -v
kubectl --context minikube -n devops-fundamentals logs hello-web
```

Expected: a Ready Pod, scheduling/container events, the Nginx version and startup logs.
Record the actual Pod IP rather than assuming a fixed address.

## 3. Namespaces, dry-run and field help

```bash
kubectl --context minikube create namespace devops-staging
kubectl --context minikube -n devops-staging run hello-web --image=nginx:1.27-alpine
kubectl --context minikube -n devops-staging wait --for=condition=Ready pod/hello-web --timeout=180s
kubectl --context minikube get pods -A | grep -E 'NAMESPACE|hello-web'
kubectl --context minikube -n devops-fundamentals run preview --image=nginx:1.27-alpine --dry-run=client -o yaml
kubectl --context minikube explain pod.spec.containers.image
```

Expected: two Pods with the same name in different namespaces. Dry-run prints a manifest
without creating a Pod. Namespaces scope names; network isolation needs separate policies.

## Results and screenshots — pending

Capture `cluster-info.png`, `kube-system-pods.png`, `node-capacity.png`, `first-pod.png`
and `namespaces.png` inside `screenshots/`. Add actual observations and image links after the run.

## Cleanup

After capturing evidence, delete only these exercise namespaces:

```bash
kubectl --context minikube delete namespace devops-fundamentals devops-staging
```

## Kubernetes Basics tutorial continuation

The earlier sections explore the cluster and a Pod. To cover deploy/expose/scale/update, run this before cleaning up devops-fundamentals:
```bash
kubectl --context minikube -n devops-fundamentals create deployment tutorial-web --image=nginx:1.27-alpine
kubectl --context minikube -n devops-fundamentals expose deployment tutorial-web --port=80 --type=ClusterIP
kubectl --context minikube -n devops-fundamentals rollout status deployment/tutorial-web
kubectl --context minikube -n devops-fundamentals scale deployment tutorial-web --replicas=3
kubectl --context minikube -n devops-fundamentals get deploy,rs,pods,svc
kubectl --context minikube -n devops-fundamentals set image deployment/tutorial-web nginx=nginx:1.29-alpine
kubectl --context minikube -n devops-fundamentals rollout status deployment/tutorial-web
kubectl --context minikube -n devops-fundamentals rollout undo deployment/tutorial-web
kubectl --context minikube -n devops-fundamentals port-forward svc/tutorial-web 8087:80
```
Check localhost:8087 in another terminal/browser, then stop port-forward and clean up the namespace. This follows the deploy/explore/expose/scale/update learning sequence; record actual outputs later.
Reference: https://kubernetes.io/docs/tutorials/kubernetes-basics/
