# LoadBalancer

**Status: execution and screenshots pending.** Complete the [shared setup](../README.md) first.
Run from the repository root.

A LoadBalancer Service requests an external load balancer from the cluster's implementation.
It commonly also has a ClusterIP and NodePort; an external address needs a supporting controller
or a local mechanism such as `minikube tunnel`.

```bash
kubectl --context minikube apply -f "Kubernetes Services/LoadBalancer/webapp-loadbalancer.yaml"
kubectl --context minikube -n devops-services get svc webapp-loadbalancer -o wide
kubectl --context minikube -n devops-services exec client -- curl -fsS --max-time 10 http://webapp-loadbalancer:9090
minikube -p minikube service webapp-loadbalancer -n devops-services --url
```

Use the printed URL in the browser and keep the process running while checking. This tests
the NodePort access path; it does not prove that an external load balancer was provisioned.
Record whether `EXTERNAL-IP` is pending or assigned in the actual run.

## Optional external-IP demonstration

After stopping the URL helper, run this in a separate terminal:

```bash
minikube -p minikube tunnel
```

It may request administrator access to configure routes. In the first terminal:

```bash
kubectl --context minikube -n devops-services get svc webapp-loadbalancer -o wide
```

Use the assigned address and Service port 9090 to test access from a reachable client. Record
whether it worked on this machine, and stop the tunnel afterward. If skipped, keep external-IP
verification explicitly pending.

## Actual results and screenshot

Pending. Save `Kubernetes Services/screenshots/loadbalancer.png` and state which access method was tested.
