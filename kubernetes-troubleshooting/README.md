# Session 14 — Troubleshooting workbook

Each case has an intentionally broken `before.yaml` and a corrected `after.yaml`. These are diagnostic fixtures, not production manifests. Run one case at a time in its dedicated namespace. Do not bulk-apply before and after files together. Actual observations and screenshots are deferred.

```bash
bash kubernetes-troubleshooting/lab.sh image-pull introduce
kubectl --context minikube -n devops-trouble-image-pull get pods -o wide
kubectl --context minikube -n devops-trouble-image-pull describe pods
kubectl --context minikube -n devops-trouble-image-pull events
bash kubernetes-troubleshooting/lab.sh image-pull fix
```

| Case argument | Problem / root cause | Investigation | Fix |
|---|---|---|---|
| `crash-loop` | Container repeatedly exits with code 1. | kubectl logs --previous and describe show repeated termination. | Replace the failing command with the normal Nginx startup. |
| `image-pull` | The image tag does not exist. | describe Events show ErrImagePull then ImagePullBackOff; logs may not exist. | Restore the valid image tag and wait for rollout. |
| `pending` | CPU request exceeds node capacity. | describe shows FailedScheduling / insufficient cpu. | Reduce requests to fit allocatable node resources. |
| `container-creating` | Required Secret volume is absent. | describe Events show FailedMount while container is Waiting. | Create the required Secret and allow kubelet to retry. |
| `configuration` | An envFrom ConfigMap is absent. | describe shows CreateContainerConfigError. | Create the ConfigMap with the expected name and keys. |
| `service` | Service selector does not match backend labels. | Compare labels/selectors and inspect EndpointSlices. | Restore the matching selector; verify HTTP through the Service. |
| `dns` | Explicit unreachable DNS nameserver | `/etc/resolv.conf`, nslookup and CoreDNS health | Recreate Pod with ClusterFirst defaults |
| `network` | NetworkPolicy denies inbound connections | DNS can succeed while HTTP times out; inspect policy and endpoints | Allow namespace clients on TCP 80 |

## Investigation commands

Substitute the case namespace and actual Pod name:
```bash
kubectl --context minikube -n devops-trouble-crash-loop get pods -o wide
kubectl --context minikube -n devops-trouble-crash-loop describe pods
kubectl --context minikube -n devops-trouble-crash-loop logs deploy/trouble-crash-loop
kubectl --context minikube -n devops-trouble-crash-loop logs deploy/trouble-crash-loop --previous
kubectl --context minikube -n devops-trouble-crash-loop events
kubectl --context minikube explain pod.spec.containers.resources
kubectl --context minikube -n devops-trouble-crash-loop top pods
# Run after fixing the container so exec is possible:
kubectl --context minikube -n devops-trouble-crash-loop exec deploy/trouble-crash-loop -- nginx -v
```
`top` requires metrics-server and cannot report a container that never started. `--previous` requires an earlier terminated container instance. Image pull errors need Events rather than application logs. ContainerCreating is a Waiting reason; inspect mount/image/CNI events rather than assuming one root cause.

## Service, DNS and networking checks

For the Service case, run a temporary client in devops-trouble-service and request `http://trouble-service`. Before the fix, EndpointSlices have no selected backends; afterward HTTP should work.
```bash
kubectl --context minikube -n devops-trouble-service get endpointslices
kubectl --context minikube -n devops-trouble-service run client --image=busybox:1.37 --restart=Never --command -- sleep 3600
kubectl --context minikube -n devops-trouble-service wait --for=condition=Ready pod/client --timeout=120s
kubectl --context minikube -n devops-trouble-service exec client -- wget -T 5 -qO- http://trouble-service
```
DNS: after introducing/fixing the case, wait for dns-client readiness and run `nslookup kubernetes.default.svc.cluster.local` inside it. Before fixing, inspect `/etc/resolv.conf`; afterward record the resolved address.

Network: use a cluster with policy enforcement (for example Minikube started with `--cni=calico`). Do not claim the denial worked on a non-enforcing CNI. Wait for network-client and trouble-network, then execute `wget -T 5 -qO- http://trouble-network` inside network-client before and after the policy fix. Leave the main cluster unchanged if it lacks policy support; use a separate lab profile later.

## Mini-project: diagnose three faults

An original mini-project based on Session 14's requirements; no exact instructor brief was supplied. See [mini-project](mini-project/README.md). It combines a bad image, missing configuration and wrong Service port; fix and verify them separately.

For each case record: command → observed symptom → hypothesis → confirming evidence → root cause → change → successful verification. Expected failures above are not recorded results.

Cleanup after capture: delete only the `devops-trouble-<case>` namespace you created. These namespaces contain disposable lab resources.
Reference: https://kubernetes.io/docs/tasks/debug/debug-application/

### Separate NetworkPolicy cluster option

If the existing Minikube profile lacks policy enforcement, create a dedicated profile during the practical session:
```bash
minikube start -p devops-policy --driver=docker --cni=calico --cpus=2 --memory=2048
KUBE_CONTEXT=devops-policy bash kubernetes-troubleshooting/lab.sh network introduce
# Use --context devops-policy for the client checks described above.
KUBE_CONTEXT=devops-policy bash kubernetes-troubleshooting/lab.sh network fix
```
Stop the main profile first if memory is limited. Cleanup only this profile after capturing evidence.
