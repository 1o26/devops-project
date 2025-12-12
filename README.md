# DevOps CI/CD Pipeline Project

A production-ready DevOps CI/CD pipeline demonstration project showcasing best practices for containerization, orchestration, and automated deployment.

## 📋 Project Overview

This project implements a complete software delivery pipeline that automates the entire process from source code to production deployment. It demonstrates modern DevOps practices using industry-standard tools.

**Key Technologies:**
- **Language:** Python 3.11
- **Web Framework:** Flask
- **Container Platform:** Docker
- **Orchestration:** Kubernetes
- **CI/CD:** Jenkins
- **Notifications:** Slack
- **Testing:** pytest with coverage
- **Code Quality:** flake8

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Developer                             │
│                   (Push to GitHub)                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│              (Source Code Management)                        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Jenkins Master/Agent                       │
│                  (CI/CD Orchestration)                       │
│                                                               │
│  ┌──────┬────────┬──────┬─────────┬──────────┬─────────┐    │
│  │Check │  Lint  │ Test │  Build  │   Push   │ Deploy  │    │
│  │ out  │        │      │ Docker  │ Registry │   to K8s│    │
│  └──────┴────────┴──────┴─────────┴──────────┴─────────┘    │
└──────────────┬────────────────────────────────┬──────────────┘
               │                                │
               ▼                                ▼
        ┌────────────────┐           ┌────────────────────┐
        │  Docker Hub    │           │ Kubernetes Cluster │
        │   Registry     │           │    (Production)    │
        │                │           │                    │
        │ my-devops-app  │           │  ┌──────────────┐  │
        │   :latest      │           │  │  Deployment  │  │
        │   :BUILD_NUM   │           │  │  (2 replicas)│  │
        └────────────────┘           │  │              │  │
                                     │  │  Service &   │  │
                                     │  │  Ingress     │  │
                                     └────────────────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │  Slack Channel     │
                    │ (#devops)          │
                    │ Notifications      │
                    └────────────────────┘
```

## 📁 Project Structure

```
DevOps project/
├── app/                          # Flask Application
│   ├── app.py                    # Main application with routes
│   ├── requirements.txt           # Python dependencies
│   └── healthcheck.sh             # Health check script
├── tests/                         # Unit Tests
│   └── test_app.py               # pytest test suite
├── docker/                       # Docker Configuration
│   ├── Dockerfile                # Multi-stage build image
│   └── .dockerignore             # Docker build exclusions
├── k8s/                          # Kubernetes Manifests
│   ├── deployment.yaml           # Pod deployment spec
│   ├── service.yaml              # Service definition
│   └── ingress.yaml              # Ingress configuration (optional)
├── Jenkinsfile                   # CI/CD Pipeline definition
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

## 🚀 Pipeline Stages

The Jenkins declarative pipeline includes the following automated stages:

### 1. **Checkout**
- Clones repository from GitHub
- Prepares clean workspace
- Sets up build environment

### 2. **Lint** (Code Quality)
- Runs flake8 Python linter
- Checks for PEP8 compliance
- Reports code style issues
- Non-blocking (warnings only)

### 3. **Unit Tests**
- Executes pytest test suite
- Generates code coverage report
- Produces JUnit XML results
- Publishes HTML coverage report
- **Failure blocks pipeline**

### 4. **Docker Build**
- Builds multi-stage Docker image
- Optimizes image size
- Tags with BUILD_NUMBER and latest
- Applies build metadata labels

### 5. **Docker Push**
- Authenticates to Docker Hub (DOCKERHUB_CREDS)
- Pushes image with BUILD_NUMBER tag
- Pushes latest tag
- Secure credentials handling

### 6. **Kubernetes Deploy**
- Uses KUBE_CONFIG credentials
- Applies service manifest
- Applies deployment manifest
- Updates image to latest version
- Applies optional ingress
- Waits for rollout completion
- Verifies pod status

### 7. **Slack Notifications** (Post actions)
- **Success:** Green notification with build details
- **Failure:** Red alert notification
- **Unstable:** Yellow warning notification
- Includes build number, commit, branch, image tag

## 🔧 Application Features

### Routes

#### `GET /`
Returns application information and status.

```json
{
  "message": "Welcome to DevOps CI/CD Application",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-12-12T10:30:45.123456",
  "status": "running"
}
```

#### `GET /health`
Health check endpoint for Kubernetes probes.

```json
{
  "status": "healthy",
  "timestamp": "2024-12-12T10:30:45.123456",
  "version": "1.0.0"
}
```

#### `GET /api/info`
Detailed application information including pod details.

```json
{
  "application": "DevOps CI/CD Pipeline Demo",
  "version": "1.0.0",
  "environment": "production",
  "hostname": "pod-hostname",
  "pod_name": "devops-app-xyz789",
  "timestamp": "2024-12-12T10:30:45.123456"
}
```

#### `GET /api/metrics`
Placeholder metrics endpoint for monitoring systems.

```json
{
  "uptime_seconds": "3600",
  "requests_processed": "N/A",
  "timestamp": "2024-12-12T10:30:45.123456"
}
```

### Health Checks

- **Readiness Probe:** Checks `/health` every 10 seconds (initial delay: 10s)
- **Liveness Probe:** Checks `/health` every 30 seconds (initial delay: 30s)
- Both probes allow 3 failures before restarting pod

## 🐳 Docker Configuration

### Multi-Stage Build
The Dockerfile uses multi-stage building to:
- Minimize final image size
- Separate build and runtime dependencies
- Improve security and performance

### Image Details
- **Base Image:** python:3.11-slim
- **Non-root User:** Runs as appuser (UID: 100)
- **Port:** 5000
- **HEALTHCHECK:** Integrated health check
- **Process Manager:** gunicorn with 4 workers

### Building Locally
```bash
docker build -t my-devops-app:latest -f docker/Dockerfile .
```

### Running Locally
```bash
docker run -p 5000:5000 \
  -e ENVIRONMENT=development \
  my-devops-app:latest
```

## ☸️ Kubernetes Deployment

### Deployment Configuration
- **Replicas:** 2 for high availability
- **Strategy:** RollingUpdate (1 surge, 0 unavailable)
- **Resource Limits:** 
  - Memory: 256Mi limit, 128Mi request
  - CPU: 500m limit, 100m request
- **Pod Anti-Affinity:** Spreads pods across nodes
- **Security Context:** Non-root user, read-only filesystems

### Service Configuration
- **Type:** ClusterIP (internal only)
- **Port:** 80 → 5000
- **Session Affinity:** None (stateless)

### Ingress Configuration (Optional)
- Supports NGINX ingress controller
- TLS support ready (cert-manager)
- Rate limiting enabled
- Host: devops-app.example.com

### Deploying to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -l app=devops-app
kubectl logs -l app=devops-app

# Port forward for testing
kubectl port-forward svc/devops-app-service 8080:80

# Clean up
kubectl delete -f k8s/
```

## 🧪 Testing

### Unit Tests
Comprehensive test suite with 20+ test cases covering:
- Endpoint response codes
- JSON response validation
- Required fields presence
- Error handling
- Content types

### Running Tests Locally

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run tests
pytest tests/test_app.py -v

# Run with coverage
pytest tests/test_app.py --cov=app --cov-report=html

# Run specific test class
pytest tests/test_app.py::TestHealthEndpoint -v
```

### Test Results
Tests generate:
- JUnit XML report (`test-results.xml`)
- HTML coverage report (`htmlcov/index.html`)
- Terminal output with detailed results

## 🔐 Jenkins Credentials

The pipeline requires the following Jenkins credentials:

### DOCKERHUB_CREDS (Username with password)
- **Username:** Your Docker Hub username
- **Password:** Your Docker Hub access token
- Used to authenticate and push images

### KUBE_CONFIG (Secret file)
- **Content:** Your kubeconfig file contents
- **Location:** ~/.kube/config
- Used to authenticate with Kubernetes cluster

### SLACK_WEBHOOK_URL (Secret text)
- **Content:** Your Slack incoming webhook URL
- **Format:** https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
- Used for pipeline notifications

## ⚙️ Environment Variables

### Application Variables
- `ENVIRONMENT`: deployment environment (development/production)
- `PORT`: application port (default: 5000)
- `POD_NAME`: Kubernetes pod name
- `POD_NAMESPACE`: Kubernetes namespace
- `POD_IP`: Pod IP address

### Jenkins Pipeline Variables
- `IMAGE`: Docker Hub image name (mydockerhubuser/my-devops-app)
- `TAG`: Build number for tagging
- `KUBE_NAMESPACE`: Kubernetes target namespace

## 📝 Jenkins Pipeline Configuration

### Prerequisites
1. Jenkins with Blue Ocean plugin installed
2. Docker installed on Jenkins agents
3. kubectl installed on Jenkins agents
4. Git plugin configured
5. JUnit and HTML Publisher plugins

### Creating the Pipeline Job

1. Go to Jenkins Dashboard → New Item
2. Select "Pipeline"
3. Name: `devops-app-pipeline`
4. Check "GitHub hook trigger for GITScm polling"
5. Under "Pipeline" → Definition: Select "Pipeline script from SCM"
6. SCM: Git
   - Repository URL: Your GitHub repo URL
   - Branch: */main
   - Script Path: Jenkinsfile
7. Save and trigger build

### GitHub Integration

1. Add Jenkins webhook to GitHub repository
2. Go to Settings → Webhooks
3. Add webhook:
   - Payload URL: `http://jenkins-server/github-webhook/`
   - Content type: application/json
   - Events: Push events
   - Active: Yes

## 🔄 CI/CD Workflow

### Developer Workflow

```bash
# 1. Clone repository
git clone <repository-url>
cd DevOps\ project

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes
# ... edit code ...

# 4. Test locally
pytest tests/test_app.py -v

# 5. Build Docker image
docker build -t my-devops-app:test -f docker/Dockerfile .

# 6. Test Docker image
docker run -p 5000:5000 my-devops-app:test

# 7. Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# 8. Create Pull Request on GitHub
# ... wait for Jenkins to run tests ...

# 9. Merge after approval
```

### Automated Workflow (Jenkins)

1. GitHub webhook triggers Jenkins
2. Pipeline executes all stages
3. Tests fail → Pipeline stops (notification sent)
4. Tests pass → Docker image built
5. Image pushed to Docker Hub
6. Deployment updated in Kubernetes
7. Success notification sent to Slack

## 📊 Monitoring and Logging

### Pod Logs
```bash
kubectl logs -l app=devops-app --tail=100 -f
```

### Pod Metrics
```bash
kubectl top pods -l app=devops-app
```

### Events
```bash
kubectl get events --sort-by='.lastTimestamp'
```

### Describe Pod
```bash
kubectl describe pod <pod-name>
```

## 🛡️ Security Best Practices Implemented

1. **Non-root User:** Application runs as non-root user
2. **Multi-stage Build:** Reduces final image size and attack surface
3. **Minimal Base Image:** Uses slim Python image
4. **Resource Limits:** Prevents resource exhaustion
5. **Health Checks:** Automatic pod recovery
6. **RBAC Ready:** Includes service account
7. **Network Policies Ready:** Can be added to k8s manifests
8. **Secrets Management:** Credentials handled via Jenkins
9. **Image Scanning:** Docker images can be scanned by registries
10. **Secure Credentials:** No hardcoded secrets in code

## 📈 Scalability Features

- **Horizontal Scaling:** Easy to increase replicas
- **Pod Auto-scaling:** Can add HPA manifest
- **Load Balancing:** Service distributes traffic
- **Rolling Updates:** Zero-downtime deployments
- **Stateless Design:** Easy to scale horizontally

## 🚨 Troubleshooting

### Pipeline Fails at Docker Push
- Verify DOCKERHUB_CREDS are correctly configured
- Check Docker Hub username and access token
- Ensure Jenkins agent has Docker installed

### Kubernetes Deployment Fails
- Verify KUBE_CONFIG credentials exist
- Check kubeconfig file syntax: `kubectl config view`
- Verify user has permissions: `kubectl auth can-i create deployments`
- Check pod logs: `kubectl logs devops-app-xxx`

### Pod CrashLoopBackOff
- Check pod logs: `kubectl logs <pod-name>`
- Verify image exists: `docker pull image:tag`
- Check resource limits aren't too low
- Review liveness probe settings

### Health Check Failing
- Verify application is running
- Check port 5000 is listening
- Test endpoint manually: `curl http://localhost:5000/health`
- Review application logs

## 🔗 Resources and References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Docker Hub Registry](https://hub.docker.com/)

## 📄 License

This project is provided as-is for educational and resume demonstration purposes.

## 👤 Author

Your Name - DevOps Engineer

---

**Last Updated:** December 12, 2024

**Version:** 1.0.0
