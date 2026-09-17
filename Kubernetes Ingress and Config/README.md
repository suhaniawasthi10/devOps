# Kubernetes Ingress, ConfigMaps and Secrets

**Name:** Suhani Awasthi

**Enrollment Number:** 24BCS10260

**Status:** Prepared; cluster execution, observed results, and screenshots are pending.

## Goal and layout

Serve a frontend at `/` and a backend at `/api/` for the host `devops.local`, with configuration
supplied through ConfigMaps and dummy credentials supplied through a Secret.
Complete [cluster setup](../README.md#kubernetes-setup) first. Run commands from the repository root.

```text
Host: devops.local → Ingress controller
                    ├── /       → frontend Service → Nginx Pods + HTML ConfigMap
                    └── /api/   → backend Service  → Python Pods + ConfigMap + Secret
```

The backend reports non-sensitive configuration. It does not connect to a database; the Secret
exercise demonstrates injection only. The checked-in password is dummy lab data.

## 1. Controller and namespace

```bash
minikube -p minikube addons enable ingress
kubectl --context minikube -n ingress-nginx rollout status deployment/ingress-nginx-controller --timeout=300s
kubectl --context minikube -n ingress-nginx get pods
kubectl --context minikube get ingressclass
kubectl --context minikube create namespace devops-config
```

An Ingress resource needs a controller to implement it. These manifests use the Minikube
NGINX addon for this local coursework exercise. Verify that the `nginx` IngressClass exists.

## 2. ConfigMaps

```bash
kubectl --context minikube apply -f "Kubernetes Ingress and Config/manifests/configmap.yaml"
kubectl --context minikube -n devops-config get configmap devops-app-config
kubectl --context minikube -n devops-config describe configmap devops-app-config
kubectl --context minikube -n devops-config create configmap cli-demo-config --from-literal=FEATURE_ATTENDANCE=true --from-literal=REGION=ap-south-1
kubectl --context minikube -n devops-config get configmap cli-demo-config -o yaml
```

ConfigMaps hold non-sensitive settings outside the image. The frontend also mounts a ConfigMap
as HTML files. Environment-variable changes require replacement/restarted Pods; normal ConfigMap
volume updates propagate asynchronously, and the application must read the updated file.

## 3. Dummy Secret

```bash
kubectl --context minikube apply -f "Kubernetes Ingress and Config/manifests/secret.yaml"
kubectl --context minikube -n devops-config get secret devops-db-secret
kubectl --context minikube -n devops-config describe secret devops-db-secret
kubectl --context minikube -n devops-config get secret devops-db-secret -o jsonpath='{.data.POSTGRES_USER}'
printf '\n'
kubectl --context minikube -n devops-config get secret devops-db-secret -o jsonpath='{.data.POSTGRES_USER}' | base64 --decode
printf '\n'
printf %s lab_user | base64
```

The file uses `stringData` for readability; Kubernetes exposes stored values under base64-encoded
`data`. Encoding is not encryption. Use only these dummy values in screenshots and the committed
exercise. Access control and encryption are separate concerns.

## 4. Applications and injected values

```bash
kubectl --context minikube apply -f "Kubernetes Ingress and Config/manifests/frontend.yaml" -f "Kubernetes Ingress and Config/manifests/backend.yaml"
kubectl --context minikube -n devops-config rollout status deployment/devops-frontend --timeout=300s
kubectl --context minikube -n devops-config rollout status deployment/devops-backend --timeout=300s
kubectl --context minikube -n devops-config get deploy,pods,svc
kubectl --context minikube -n devops-config exec deploy/devops-backend -- printenv ENVIRONMENT DEFAULT_CAMPUS POSTGRES_USER
```

Expected: two Ready replicas per Deployment, two ClusterIP Services and injected values from
both the ConfigMap and Secret. `envFrom.configMapRef` imports configuration keys;
`env.valueFrom.secretKeyRef` selects individual Secret keys.

## 5. Host and path routing

```bash
kubectl --context minikube apply -f "Kubernetes Ingress and Config/manifests/ingress.yaml"
kubectl --context minikube -n devops-config get ingress
kubectl --context minikube -n devops-config describe ingress
```

In a separate terminal, keep this running:

```bash
kubectl --context minikube -n ingress-nginx port-forward svc/ingress-nginx-controller 8086:80
```

Then test in the first terminal:

```bash
curl -fsS --max-time 10 -H 'Host: devops.local' http://localhost:8086/
curl -fsS --max-time 10 -H 'Host: devops.local' http://localhost:8086/api/
curl -sS --max-time 10 -o /dev/null -w 'HTTP %{http_code}\n' -H 'Host: nowhere.local' http://localhost:8086/
```

Expected: frontend HTML, backend configuration output and an unmatched-host response (normally
404 with the default controller backend). Two Ingress resources share the host: only the API
resource has a rewrite annotation, stripping `/api` before forwarding. The frontend preserves
its request paths. Both use the same controller entry point.

The Host header avoids changing `/etc/hosts`. A plain browser request to `localhost:8086`
does not send `Host: devops.local`, so use the curl commands for routing evidence. This lab
uses HTTP only; TLS configuration is outside its scope.

## Results and screenshots — pending

Capture `controller.png`, `configmap.png`, `secret.png`, `apps-env.png` and `ingress-routing.png`
inside `screenshots/`. Record actual outputs after the run and then add image links.

## Cleanup

Stop the port-forward with Ctrl+C. Delete the exercise namespace:

```bash
kubectl --context minikube delete namespace devops-config
```

The cluster-wide Ingress addon remains enabled for later exercises.
