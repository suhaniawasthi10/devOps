# Pod lifecycle

```bash
kubectl --context minikube create namespace devops-lifecycle
kubectl --context minikube -n devops-lifecycle apply -f "Kubernetes Workloads/lifecycle"
kubectl --context minikube -n devops-lifecycle get pods -o wide
kubectl --context minikube -n devops-lifecycle describe pods
kubectl --context minikube -n devops-lifecycle logs lifecycle-succeeded
kubectl --context minikube -n devops-lifecycle logs lifecycle-failed
kubectl --context minikube -n devops-lifecycle delete pod lifecycle-running --wait=false
kubectl --context minikube -n devops-lifecycle get pods
```

Pending: unmatched node selector prevents scheduling. Running: the sleeping process starts. Succeeded: exit 0 with restartPolicy Never. Failed: exit 1 with restartPolicy Never. Unknown means the Pod's state cannot be obtained; deliberately breaking the node is unnecessary. Terminating and CrashLoopBackOff are displayed statuses, not additional phases. Containers have Waiting, Running and Terminated states. Capture status, describe, Events and observations for each file during the practical session.

Cleanup: `kubectl --context minikube delete namespace devops-lifecycle`.
Reference: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
