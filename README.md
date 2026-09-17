# DevOps Coursework

**Suhani Awasthi · 24BCS10260**

Code and notes for the DevOps exercises. The Kubernetes modules are prepared for a future
local run; their results and screenshots have not been captured yet.

| Topic | Files | Status |
|---|---|---|
| Linux fundamentals | [Notes](linuxFundamentals/README.md) | Notes present; practical evidence can be expanded |
| Shell scripting | [Script and notes](ShellScripting/README.md) | Script present; README output placeholders remain |
| Git | [Exercises](Git/README.md) | Commit and cherry-pick exercises documented |
| Networking | [Commands](Networking/README.md) | Commands and screenshots present |
| Docker fundamentals | [Six applications](Docker-Homework.md) | Dockerfiles, code and screenshots present |
| Docker multi-stage builds | [Exercise](docker-multistage/Docker-Multistage-Homework.md) | Code and screenshots present |
| Docker networks and mounts | [Exercises](Docker-Networking-Volumes/README.md) | Documented; host-network HTTP verification pending |
| Kubernetes fundamentals | [Guide](Kubernetes%20Fundamentals/README.md) | Prepared; execution/screenshots pending |
| Kubernetes workloads | [Guide](Kubernetes%20Workloads/README.md) | Prepared; execution/screenshots pending |
| Kubernetes Services | [Guide](Kubernetes%20Services/README.md) | Prepared; execution/screenshots pending |
| Kubernetes Ingress and configuration | [Guide](Kubernetes%20Ingress%20and%20Config/README.md) | Prepared; execution/screenshots pending |

## Kubernetes setup

These exercises use macOS, Docker Desktop and Minikube with the Docker driver.
Start Docker Desktop, and install `kubectl` and Minikube if needed using the
[Minikube setup instructions](https://minikube.sigs.k8s.io/docs/start/).

```bash
docker version
kubectl version --client
minikube version
minikube start --driver=docker
minikube status
kubectl --context minikube cluster-info
kubectl --context minikube get nodes -o wide
```

Run the modules in order: Fundamentals → Workloads → Services → Ingress and Config.
All command blocks run from the repository root and explicitly select the `minikube` context.
Each guide includes expected behavior, screenshot filenames and cleanup instructions.
Record actual results and screenshots during the practical session; live verification is pending.
