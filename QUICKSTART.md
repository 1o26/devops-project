# Quick Start Guide

Get your DevOps project up and running in minutes!

## Prerequisites

- Python 3.11+
- Docker
- kubectl (for Kubernetes deployment)
- Git
- Jenkins (for CI/CD)

## 5-Minute Local Setup

### 1. Install Python Dependencies
```powershell
cd "DevOps project"
pip install -r app/requirements.txt
```

### 2. Run the Application Locally
```powershell
python app/app.py
```

Visit: http://localhost:5000/health

### 3. Run Unit Tests
```powershell
pytest tests/test_app.py -v
```

### 4. Build Docker Image
```powershell
docker build -t my-devops-app:latest -f docker/Dockerfile .
```

### 5. Run in Docker
```powershell
docker run -p 5000:5000 my-devops-app:latest
```

## Testing Endpoints

```bash
# Root endpoint
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# API info
curl http://localhost:5000/api/info

# Metrics
curl http://localhost:5000/api/metrics

# Test 404 error
curl http://localhost:5000/invalid
```

## Push to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag my-devops-app:latest mydockerhubuser/my-devops-app:latest
docker tag my-devops-app:latest mydockerhubuser/my-devops-app:1

# Push
docker push mydockerhubuser/my-devops-app:latest
docker push mydockerhubuser/my-devops-app:1
```

## Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml

# Check status
kubectl get pods -l app=devops-app
kubectl get svc devops-app-service

# Port forward for testing
kubectl port-forward svc/devops-app-service 8080:80

# View logs
kubectl logs -l app=devops-app -f
```

## Jenkins Integration

1. Create Pipeline job in Jenkins
2. Point to Jenkinsfile in repository
3. Add GitHub webhook
4. Configure these credentials:
   - DOCKERHUB_CREDS (username/password)
   - KUBE_CONFIG (secret file)
   - SLACK_WEBHOOK_URL (secret text)
5. Trigger build

## Troubleshooting

**Docker build fails:**
```bash
docker build --no-cache -t my-devops-app -f docker/Dockerfile .
```

**Port already in use:**
```bash
docker run -p 8080:5000 my-devops-app
curl http://localhost:8080/health
```

**Kubernetes pods not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Tests failing locally:**
```bash
pytest tests/test_app.py -v --tb=long
```

## Key Files to Customize

1. **Jenkinsfile** (line 11): Change `IMAGE = "mydockerhubuser/my-devops-app"`
2. **k8s/deployment.yaml** (line 54): Update image URL
3. **README.md** (bottom): Add your name
4. **Jenkinsfile** (line 278): Update SLACK_WEBHOOK_URL

## Performance Tuning

### Docker
- Adjust gunicorn workers (line 38 of Dockerfile): `--workers 4`
- Increase Python timeout if needed: `--timeout 30`

### Kubernetes
- Increase replicas: Edit deployment.yaml line 18 `replicas: 2`
- Adjust resource limits: Edit deployment.yaml lines 88-93
- Enable HPA (auto-scaling) with: `kubectl autoscale deployment devops-app --min=2 --max=10`

### Application
- Set environment variables in deployment.yaml
- Adjust probe timeouts in deployment.yaml
- Increase worker processes for high traffic

## Monitoring

```bash
# Pod metrics
kubectl top pods -l app=devops-app

# Pod resources
kubectl describe node

# Recent events
kubectl get events --sort-by='.lastTimestamp'

# Application logs
kubectl logs -l app=devops-app --tail=100 -f

# Access application
kubectl port-forward svc/devops-app-service 5000:80
curl http://localhost:5000/health
```

## Common Commands Cheat Sheet

```bash
# Git
git init
git add .
git commit -m "Initial commit"
git push origin main

# Docker
docker build -t my-app .
docker run -p 5000:5000 my-app
docker push my-registry/my-app

# Python/Testing
pip install -r requirements.txt
pytest tests/ -v
flake8 app/

# Kubernetes
kubectl apply -f k8s/
kubectl delete -f k8s/
kubectl get pods -w
kubectl logs -f pod/name
kubectl exec -it pod/name -- bash

# Jenkins
# Use Pipeline job with Jenkinsfile
# Build triggers: GitHub push
# Post actions: Email, Slack notifications
```

## Need Help?

- Check **README.md** for detailed documentation
- Review **PROJECT_STRUCTURE.md** for file descriptions
- See troubleshooting section in README.md
- Jenkins logs at: Jenkins Dashboard → Build → Console Output

## Success Indicators

✅ Flask app runs on http://localhost:5000/health
✅ Tests pass: `pytest tests/test_app.py` shows all green
✅ Docker image builds and runs successfully
✅ Kubernetes deployment shows 2 running pods
✅ Pipeline completes all 6 stages
✅ Slack notifications received

---

**You're ready to go!** 🚀
