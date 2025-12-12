# JENKINS SETUP - WHAT YOU NEED

Here's exactly what you need to do to get Jenkins working with your project.

---

## ✅ What You Already Have

- [x] Docker installed (v28.5.1)
- [x] kubectl installed (v1.34.1)
- [x] Project on GitHub (https://github.com/1o26/devops-project)
- [x] All code ready (25 files, 3000+ lines)
- [x] Tests passing (23/23)

---

## 🔴 What You Still Need

### 1. Docker Hub Account
**Status:** Not set up yet

**To do:**
1. Go to: https://hub.docker.com
2. Create account
3. Generate access token
4. **See:** `DOCKERHUB_ACCOUNT_SETUP.md`

**Why needed:** Jenkins needs to authenticate and push Docker images

---

### 2. Kubernetes Cluster Access
**Status:** kubectl installed, but need cluster configured

**To do:**
1. Make sure you have access to a Kubernetes cluster:
   - Minikube (local)
   - Docker Desktop with K8s enabled
   - Kind cluster
   - Cloud cluster (GKE, EKS, AKS)
2. Verify connection: `kubectl get nodes`
3. Get kubeconfig file location: Usually `~/.kube/config`

**Why needed:** Jenkins needs kubeconfig to deploy to your cluster

---

### 3. Jenkins Installation
**Status:** Unknown if installed

**To do:**
1. Verify Jenkins is installed and running
2. Go to: `http://localhost:8080` (or your Jenkins URL)
3. If not installed:
   - Windows: https://www.jenkins.io/download/ (Windows Installer)
   - Or use Docker: `docker run -p 8080:8080 jenkins/jenkins:latest`

**Why needed:** Jenkins is the CI/CD orchestrator

---

### 4. Slack Workspace (Optional but Recommended)
**Status:** Unknown

**To do:**
1. If you have a Slack workspace, create incoming webhook
2. If not, skip this (notifications won't work but pipeline will)

**Why needed:** Get notifications when builds succeed/fail

---

## 📋 COMPLETE SETUP CHECKLIST

Print this checklist and mark off each item:

### Phase 1: Prerequisites
- [ ] Docker Hub account created
- [ ] Docker Hub access token generated and saved
- [ ] Kubernetes cluster configured and accessible
- [ ] kubeconfig file exists at `~/.kube/config`
- [ ] Verified: `kubectl get nodes` shows cluster nodes
- [ ] Slack workspace ready (optional)

### Phase 2: Update Configuration Files
- [ ] Updated Jenkinsfile line 11 with your Docker Hub username
- [ ] Example: `IMAGE = "your-username/my-devops-app"`

### Phase 3: Create Jenkins Credentials
- [ ] DOCKERHUB_CREDS credential created in Jenkins
  - Type: Username with password
  - Username: Your Docker Hub username
  - Password: Your access token
- [ ] KUBE_CONFIG credential created in Jenkins
  - Type: Secret file
  - File: Your ~/.kube/config file
- [ ] SLACK_WEBHOOK_URL credential created in Jenkins (optional)
  - Type: Secret text
  - Value: Your Slack webhook URL

### Phase 4: Create Jenkins Pipeline Job
- [ ] Job name: `devops-app-pipeline`
- [ ] Type: Pipeline
- [ ] GitHub project URL configured
- [ ] Git repository configured
- [ ] Jenkinsfile path configured
- [ ] GitHub webhook trigger enabled

### Phase 5: Test Pipeline
- [ ] Run "Build Now" in Jenkins
- [ ] All 7 stages pass:
  - [ ] Checkout
  - [ ] Lint
  - [ ] Unit Tests
  - [ ] Docker Build
  - [ ] Docker Push
  - [ ] Kubernetes Deploy
  - [ ] Slack Notifications

---

## 🎯 YOUR NEXT STEP

**You need to:**

1. **Create Docker Hub account** (5 minutes)
   - Follow: `DOCKERHUB_ACCOUNT_SETUP.md`

2. **Verify Kubernetes cluster** (5 minutes)
   ```bash
   kubectl get nodes
   kubectl config view  # check location of kubeconfig
   ```

3. **Once Docker Hub is ready**, move to Jenkins setup:
   - Follow: `JENKINS_CREDENTIALS_CHECKLIST.md`
   - Follow: `JENKINS_SETUP_VISUAL.md`

---

## ⏱️ TIME ESTIMATE

- Docker Hub setup: **5-10 minutes**
- Kubernetes verification: **5 minutes**
- Jenkins setup: **15-20 minutes**
- First pipeline run: **5-10 minutes**

**Total: ~40-50 minutes to fully functional CI/CD pipeline**

---

## 🆘 IF YOU GET STUCK

1. **Docker Hub issue?** → See `DOCKERHUB_ACCOUNT_SETUP.md`
2. **Jenkins credential issue?** → See `JENKINS_CREDENTIALS_CHECKLIST.md`
3. **Kubernetes issue?** → See `KUBERNETES_SETUP.md`
4. **Jenkins job issue?** → See `JENKINS_SETUP_VISUAL.md`

---

## 📞 QUICK REFERENCE

### Commands to Verify Setup

```bash
# Check Docker
docker --version

# Check kubectl
kubectl version --client

# Check Kubernetes cluster
kubectl get nodes

# Check kubeconfig location
# Windows: cat $env:USERPROFILE\.kube\config
# Linux/Mac: cat ~/.kube/config

# Test Docker Hub login
docker login
# Username: YOUR_USERNAME
# Password: YOUR_TOKEN
```

---

## Ready?

Once you have Docker Hub set up, let me know and I'll guide you through the Jenkins setup! 🚀

---

**Current Status:** Waiting for Docker Hub account + Kubernetes verification
**Next Action:** Follow `DOCKERHUB_ACCOUNT_SETUP.md`
