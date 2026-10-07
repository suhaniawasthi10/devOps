# Kubernetes setup and screenshot checklist

Prepared on 17 September 2026 for a planned run on 18 September 2026.
All live verification and screenshots remain pending. No cluster resources were created
while preparing these files.

## Setup

The guides target macOS, Docker Desktop and a local Minikube cluster using the Docker driver.
`kubectl` was found while preparing the files; `minikube` was not on PATH. Installation and
cluster startup are left for the practical session.

1. Start Docker Desktop and wait for its engine to be ready.
2. Install Minikube if needed using the [official setup instructions](https://minikube.sigs.k8s.io/docs/start/).
3. From the repository root, run:

```bash
docker version
kubectl version --client
minikube version
minikube start --driver=docker
minikube status
kubectl --context minikube cluster-info
kubectl --context minikube get nodes -o wide
```

Record the versions and actual output during the run. Do not substitute version numbers,
Pod names or IP addresses from the reference repository.

All lab commands explicitly select the `minikube` context. Resources use dedicated namespaces:
`devops-fundamentals`, `devops-staging`, `devops-workloads`, `devops-services`, and `devops-config`.
Run the command blocks in each guide in order, from the repository root. Keep port-forward
or `minikube service --url` processes open in a separate terminal while testing their URLs.

## Capture checklist

Save images in each module's `screenshots/` directory. Filenames below are planned files;
there are no screenshot image links until the images exist.

### Fundamentals

- [ ] `Kubernetes Fundamentals/screenshots/cluster-info.png` — versions, cluster info, nodes and namespaces.
- [ ] `Kubernetes Fundamentals/screenshots/kube-system-pods.png` — system Pods and their placement.
- [ ] `Kubernetes Fundamentals/screenshots/node-capacity.png` — node capacity, allocatable resources and API resources.
- [ ] `Kubernetes Fundamentals/screenshots/first-pod.png` — Pod readiness, details, exec and logs.
- [ ] `Kubernetes Fundamentals/screenshots/namespaces.png` — same Pod name in two namespaces, dry-run and explain.

### Workloads

- [ ] `Kubernetes Workloads/screenshots/pod.png` — bare Pod creation and deletion.
- [ ] `Kubernetes Workloads/screenshots/replicaset.png` — replacement Pod and scaling to five replicas.
- [ ] `Kubernetes Workloads/screenshots/deployment-v1.png` — Deployment, ReplicaSet and Pods, plus v1 HTTP response.
- [ ] `Kubernetes Workloads/screenshots/rolling-update-rollback.png` — v2 rollout and rollback to v1.
- [ ] `Kubernetes Workloads/screenshots/broken-image.png` — image pull failure and recovery.
- [ ] `Kubernetes Workloads/screenshots/daemonset.png` — DaemonSet and eligible-node placement.

### Services

- [ ] `Kubernetes Services/screenshots/webapp-pod.png` — Nginx Pod and helper Pods ready.
- [ ] `Kubernetes Services/screenshots/clusterip.png` — HTTP response, DNS and EndpointSlice.
- [ ] `Kubernetes Services/screenshots/no-endpoints.png` — typo selector, missing backend endpoints and failed request.
- [ ] `Kubernetes Services/screenshots/nodeport.png` — Service port mapping and browser through Minikube URL.
- [ ] `Kubernetes Services/screenshots/loadbalancer.png` — actual external-IP state and internal HTTP response; record how browser access was obtained.
- [ ] `Kubernetes Services/screenshots/headless.png` — Pod IP versus DNS answer and direct HTTP response.
- [ ] `Kubernetes Services/screenshots/externalname.png` — CNAME lookup and external HTTP check.
- [ ] `Kubernetes Services/screenshots/final-state.png` — Services, EndpointSlices and Pods before cleanup.

### Ingress and configuration

- [ ] `Kubernetes Ingress and Config/screenshots/controller.png` — ready controller and IngressClass.
- [ ] `Kubernetes Ingress and Config/screenshots/configmap.png` — declarative ConfigMap and CLI-created ConfigMap.
- [ ] `Kubernetes Ingress and Config/screenshots/secret.png` — dummy Secret metadata and lab username encode/decode.
- [ ] `Kubernetes Ingress and Config/screenshots/apps-env.png` — Deployments/Services and selected non-password environment values.
- [ ] `Kubernetes Ingress and Config/screenshots/ingress-routing.png` — frontend, `/api/`, and unmatched-host request.

## Finish the submission

- [ ] Add actual observations below each module's pending-results section.
- [ ] Add Markdown image links only after saving the matching screenshots.
- [ ] Record failed checks and their fixes; leave incomplete checks marked pending.
- [ ] Run the module cleanup commands after capturing evidence.
- [ ] Stop temporary tunnels with Ctrl+C and optionally run `minikube stop`.
- [ ] Review `git diff` and `git status` before committing.
