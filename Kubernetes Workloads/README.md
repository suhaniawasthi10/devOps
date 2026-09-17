# Kubernetes Workloads

**Name:** Suhani Awasthi

**Enrollment Number:** 24BCS10260

**Status:** Prepared; cluster execution, observed results, and screenshots are pending.

## Goal

Practice Pods, ReplicaSets, Deployments, rolling updates, rollback and DaemonSets.
Complete [cluster setup](../README.md#kubernetes-setup) first. Run from the repository root.

A standalone Pod is not recreated after deletion. Its containers can still restart according
to the restart policy. A ReplicaSet maintains a replica count; a Deployment manages ReplicaSets
for updates. A DaemonSet places a Pod on each eligible node.

```bash
kubectl --context minikube create namespace devops-workloads
```

## 1. Standalone Pod

```bash
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/demo-pod.yaml"
kubectl --context minikube -n devops-workloads wait --for=condition=Ready pod/devops-demo-pod --timeout=180s
kubectl --context minikube -n devops-workloads get pods -o wide --show-labels
kubectl --context minikube -n devops-workloads delete pod devops-demo-pod
kubectl --context minikube -n devops-workloads get pods
```

Expected: deleting the bare Pod does not create a replacement.

## 2. ReplicaSet: self-healing and scaling

```bash
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/backend-rs.yaml"
kubectl --context minikube -n devops-workloads wait --for=condition=Ready pod -l app=devops-backend-rs --timeout=240s
kubectl --context minikube -n devops-workloads get rs,pods -l app=devops-backend-rs
lab_pod=$(kubectl --context minikube -n devops-workloads get pods -l app=devops-backend-rs -o jsonpath='{.items[0].metadata.name}')
kubectl --context minikube -n devops-workloads delete pod "$lab_pod"
kubectl --context minikube -n devops-workloads get pods -l app=devops-backend-rs
kubectl --context minikube -n devops-workloads scale rs devops-backend-rs --replicas=5
kubectl --context minikube -n devops-workloads get rs,pods -l app=devops-backend-rs
kubectl --context minikube -n devops-workloads describe rs devops-backend-rs
```

Expected: a replacement Pod with a different name and eventually five Ready replicas.
Re-run `get` until the controller has converged. Capture the result, then remove this exercise
before starting the Deployment:

```bash
kubectl --context minikube delete -f "Kubernetes Workloads/manifests/backend-rs.yaml"
```

## 3. Deployment: v1, v2 and rollback

```bash
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/deployment-v1.yaml"
kubectl --context minikube -n devops-workloads rollout status deployment/devops-backend --timeout=300s
kubectl --context minikube -n devops-workloads annotate deployment/devops-backend kubernetes.io/change-cause='Initial v1' --overwrite
kubectl --context minikube -n devops-workloads get deploy,rs,pods -l app=devops-backend
kubectl --context minikube -n devops-workloads exec deploy/devops-backend -- python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000').read().decode())"
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/deployment-v2.yaml"
kubectl --context minikube -n devops-workloads annotate deployment/devops-backend kubernetes.io/change-cause='Update to v2' --overwrite
kubectl --context minikube -n devops-workloads rollout status deployment/devops-backend --timeout=300s
kubectl --context minikube -n devops-workloads get pods -l app=devops-backend -L version
kubectl --context minikube -n devops-workloads exec deploy/devops-backend -- python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000').read().decode())"
kubectl --context minikube -n devops-workloads rollout history deployment/devops-backend
kubectl --context minikube -n devops-workloads rollout undo deployment/devops-backend
kubectl --context minikube -n devops-workloads rollout status deployment/devops-backend --timeout=300s
kubectl --context minikube -n devops-workloads get pods -l app=devops-backend -L version
kubectl --context minikube -n devops-workloads exec deploy/devops-backend -- python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000').read().decode())"
```

Expected: the HTTP response changes from v1 to v2 and returns to v1. Old ReplicaSets remain
available for rollback. `maxSurge: 1`, `maxUnavailable: 0` and an HTTP readiness probe control
replacement. This exercise does not measure uninterrupted traffic during the rollout.

## 4. Diagnose a bad image

```bash
kubectl --context minikube -n devops-workloads set image deployment/devops-backend backend=python:no-such-tag-devops-lab
kubectl --context minikube -n devops-workloads get pods -l app=devops-backend
kubectl --context minikube -n devops-workloads describe pods -l app=devops-backend
```

Wait for pull attempts and capture `ErrImagePull` or `ImagePullBackOff` with the actual Events.
The existing Ready replicas should remain while the new Pod cannot become Ready. Recover with:

```bash
kubectl --context minikube -n devops-workloads rollout undo deployment/devops-backend
kubectl --context minikube -n devops-workloads rollout status deployment/devops-backend --timeout=300s
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/deployment-v1.yaml"
kubectl --context minikube -n devops-workloads rollout status deployment/devops-backend --timeout=300s
```

The final apply makes the intended declarative version explicit after the rollback exercise.
For a crashing container, inspect `kubectl logs --previous`; image-pull failures instead need Events.

## 5. DaemonSet and resource settings

```bash
kubectl --context minikube apply -f "Kubernetes Workloads/manifests/node-agent-ds.yaml"
kubectl --context minikube -n devops-workloads rollout status ds/node-metrics-agent --timeout=240s
kubectl --context minikube -n devops-workloads get ds,pods -l app=node-metrics-agent -o wide
kubectl --context minikube -n devops-workloads logs -l app=node-metrics-agent --tail=5
kubectl --context minikube describe node minikube
```

Expected: one DaemonSet Pod on the single eligible node. This is a logging demonstration,
not a real metrics collector. Inspect the manifests' CPU/memory requests and limits; requests
are used in scheduling, while limits constrain usage. Taints and selectors can change node eligibility.

## Results and screenshots — pending

Capture `pod.png`, `replicaset.png`, `deployment-v1.png`, `rolling-update-rollback.png`,
`broken-image.png` and `daemonset.png` inside `screenshots/`. Record actual results after running.

## Cleanup

```bash
kubectl --context minikube delete namespace devops-workloads
```

Apply v1 and v2 individually as above; do not bulk-apply the manifests folder, which contains
two versions of the same Deployment.
