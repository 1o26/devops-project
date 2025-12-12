# Kubernetes Deployment Instructions

## Prerequisites

- kubectl installed: `kubectl version --client`
- Kubernetes cluster running (minikube, kind, or cloud cluster)
- kubeconfig file configured: `kubectl config view`
- Docker image built and available

## Step 1: Verify Cluster Connection

```bash
# Check cluster connection
kubectl cluster-info

# List nodes
kubectl get nodes

# List namespaces
kubectl get namespaces
```

## Step 2: Create Kubernetes Manifests

The project includes three manifests in `k8s/` directory:

- `service.yaml` - ClusterIP service on port 80 → 5000
- `deployment.yaml` - 2 replicas with health probes
- `ingress.yaml` - Optional NGINX ingress (requires ingress controller)

## Step 3: Update Image in Manifest

Edit `k8s/deployment.yaml` and update line 54:

```yaml
image: YOUR_DOCKER_HUB_USERNAME/my-devops-app:latest
```

Or use kubectl to update directly:

```bash
kubectl set image deployment/devops-app \
  devops-app=YOUR_USERNAME/my-devops-app:latest \
  -n default
```

## Step 4: Deploy to Kubernetes

```bash
# Apply service
kubectl apply -f k8s/service.yaml

# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Apply ingress (optional, requires ingress controller)
kubectl apply -f k8s/ingress.yaml
```

## Step 5: Verify Deployment

```bash
# Check deployment
kubectl get deployment devops-app

# Check pods
kubectl get pods -l app=devops-app

# Check service
kubectl get svc devops-app-service

# Describe deployment
kubectl describe deployment devops-app
```

## Step 6: Test Application

### Option 1: Port Forward
```bash
kubectl port-forward svc/devops-app-service 8080:80

# Test in another terminal
curl http://localhost:8080/health
```

### Option 2: Port Forward to Pod
```bash
kubectl port-forward pod/PODNAME 5000:5000

curl http://localhost:5000/health
```

### Option 3: Exec into Pod
```bash
kubectl exec -it PODNAME -- bash
curl http://localhost:5000/health
```

## Step 7: Monitor Application

```bash
# View logs
kubectl logs -l app=devops-app --tail=100 -f

# View logs from specific pod
kubectl logs PODNAME -f

# Describe pod for events
kubectl describe pod PODNAME

# Get pod metrics
kubectl top pods -l app=devops-app

# Watch pod status
kubectl get pods -l app=devops-app -w
```

## Step 8: Scale Application

```bash
# Scale to 3 replicas
kubectl scale deployment devops-app --replicas=3

# Verify
kubectl get pods -l app=devops-app
```

## Step 9: Update Deployment

### Push new image:
```bash
docker build -t YOUR_USERNAME/my-devops-app:2 -f docker/Dockerfile .
docker push YOUR_USERNAME/my-devops-app:2
```

### Update deployment:
```bash
kubectl set image deployment/devops-app \
  devops-app=YOUR_USERNAME/my-devops-app:2
```

### Monitor rollout:
```bash
kubectl rollout status deployment/devops-app

# Rollback if needed:
kubectl rollout undo deployment/devops-app
```

## Ingress Setup (Optional)

If you want external access via ingress:

### 1. Install NGINX Ingress Controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml
```

### 2. Update Ingress Host
Edit `k8s/ingress.yaml` and change:
```yaml
- host: YOUR_DOMAIN.com
```

### 3. Apply Ingress
```bash
kubectl apply -f k8s/ingress.yaml
```

### 4. Get Ingress IP
```bash
kubectl get ingress devops-app-ingress
```

## Troubleshooting

### Pods Stuck in Pending
```bash
kubectl describe pod PODNAME
# Check node resources, PVC availability, etc.
```

### Pod CrashLoopBackOff
```bash
kubectl logs PODNAME
# Check for errors in application startup
```

### Health Check Failing
```bash
kubectl exec PODNAME -- curl http://localhost:5000/health
# Verify app is running and health endpoint works
```

### Image Pull Error
```bash
# Verify image exists in Docker Hub
docker pull YOUR_USERNAME/my-devops-app:latest

# Check image pull policy in deployment.yaml
```

## Cleanup

```bash
# Delete deployment
kubectl delete deployment devops-app

# Delete service
kubectl delete svc devops-app-service

# Delete ingress
kubectl delete ingress devops-app-ingress

# Or delete all at once
kubectl delete -f k8s/
```

## Next Steps

1. Monitor application in Kubernetes
2. Check logs and metrics
3. Scale up/down as needed
4. Set up monitoring (Prometheus, Grafana)
5. Configure persistent storage if needed
6. Implement network policies
7. Set up RBAC policies
