# Session 13 — Volumes

| Volume/object | Lifetime and purpose | Example |
|---|---|---|
| emptyDir | Shared by containers in one Pod; survives container restart but disappears with the Pod | writer/reader scratch space |
| hostPath | Node filesystem directory; node-specific and can expose host data | dedicated /tmp coursework path |
| PersistentVolume | Cluster-scoped storage resource | static hostPath PV in this single-node lab |
| PersistentVolumeClaim | Namespaced request that binds to a compatible PV | static-data or dynamic-data |
| StorageClass | Provisioner and policy for creating storage | Minikube hostpath provisioner |
| Dynamic provisioning | Creates a PV in response to a PVC | dynamic-data claim |

Run from repository root on Minikube:
```bash
kubectl --context minikube create namespace devops-storage
kubectl --context minikube -n devops-storage apply -f 01-kubernetes-volumes/manifests
kubectl --context minikube -n devops-storage get pods,pvc
kubectl --context minikube get pv,storageclass
kubectl --context minikube -n devops-storage logs shared-emptydir -c reader
kubectl --context minikube -n devops-storage exec static-writer -- cat /data/proof.txt
kubectl --context minikube -n devops-storage delete pod static-writer
kubectl --context minikube -n devops-storage apply -f 01-kubernetes-volumes/manifests/static-writer.yaml
kubectl --context minikube -n devops-storage wait --for=condition=Ready pod/static-writer --timeout=120s
kubectl --context minikube -n devops-storage exec static-writer -- cat /data/proof.txt
```
Two appended lines after recreation demonstrate persistence. Repeat with dynamic-writer. emptyDir data disappears with its Pod. ReadWriteOnce means writable from a single node, not necessarily a single Pod. Retain preserves backing data after claim deletion; Delete asks the provisioner to delete storage.

Cleanup after evidence: delete the devops-storage namespace, then only `pv/devops-static-pv` and `storageclass/devops-dynamic`. The retained static hostPath data remains on the Minikube node until deliberately removed. Never mount host root for this exercise.

Reference: https://kubernetes.io/docs/concepts/storage/volumes/ and https://kubernetes.io/docs/concepts/storage/persistent-volumes/
