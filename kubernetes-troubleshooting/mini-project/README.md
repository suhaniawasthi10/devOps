# Broken portal mini-project

```bash
kubectl --context minikube create namespace devops-trouble-project
kubectl --context minikube -n devops-trouble-project apply -f kubernetes-troubleshooting/mini-project/broken.yaml
kubectl --context minikube -n devops-trouble-project describe pods
kubectl --context minikube -n devops-trouble-project set image deployment/broken-portal web=nginx:alpine
kubectl --context minikube -n devops-trouble-project describe pods
kubectl --context minikube -n devops-trouble-project create configmap portal-config --from-literal=ENVIRONMENT=lab
kubectl --context minikube -n devops-trouble-project rollout status deployment/broken-portal --timeout=180s
kubectl --context minikube -n devops-trouble-project describe svc portal
kubectl --context minikube -n devops-trouble-project get endpointslices
kubectl --context minikube -n devops-trouble-project patch svc portal -p '{"spec":{"ports":[{"port":80,"targetPort":80}]}}'
kubectl --context minikube -n devops-trouble-project apply -f kubernetes-troubleshooting/mini-project/fixed.yaml
kubectl --context minikube -n devops-trouble-project run client --image=busybox:1.37 --restart=Never --command -- sleep 3600
kubectl --context minikube -n devops-trouble-project wait --for=condition=Ready pod/client --timeout=120s
kubectl --context minikube -n devops-trouble-project exec client -- wget -qO- http://portal
```
The first two faults prevent startup; the third leaves a healthy Pod unreachable through the Service. Event order may vary. Explain each observed symptom rather than claiming a predetermined order. The final declarative apply also restores repeatability after imperative diagnosis.
Capture each before/after transition, then delete devops-trouble-project.
