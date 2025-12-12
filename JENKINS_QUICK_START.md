# JENKINS SETUP - SIMPLIFIED FOR YOU

Since you're setting up for the first time, here's the simplest path:

---

## ✅ WHAT YOU HAVE READY

1. ✅ Code on GitHub: https://github.com/1o26/devops-project
2. ✅ Tests passing (23/23)
3. ✅ Docker installed
4. ✅ kubectl installed

---

## 🔴 WHAT'S NEEDED

### 1. Docker Hub Account (Required)
- [ ] Create account at https://hub.docker.com
- [ ] Generate access token
- [ ] Update Jenkinsfile with your username
  - Line 31: `IMAGE = "YOUR_USERNAME/my-devops-app"`

**See:** `DOCKERHUB_ACCOUNT_SETUP.md`

---

### 2. Kubernetes Cluster (Can Be Tested Later)
- [ ] Set up Docker Desktop Kubernetes OR Minikube
- [ ] OR get kubeconfig from admin
- [ ] Test: `kubectl get nodes` (should work)

**See:** `KUBERNETES_AUTH_SETUP.md`

---

### 3. Jenkins Installation (If Not Running)
- [ ] Make sure Jenkins is running at http://localhost:8080
- [ ] If not installed: Download from https://www.jenkins.io/download/

---

## 📝 SIMPLE SETUP STEPS

### Step 1: Docker Hub (5 min)
1. Go to https://hub.docker.com → Sign up
2. Generate token: Account → Security → New Access Token
3. Update Jenkinsfile line 31:
   ```groovy
   IMAGE = "YOUR_USERNAME/my-devops-app"
   ```

### Step 2: Jenkins - Create Credential (2 min)
1. Go to http://localhost:8080
2. Manage Jenkins → Manage Credentials → System → Global credentials
3. Add Credentials:
   - Kind: Username with password
   - Username: YOUR_DOCKER_HUB_USERNAME
   - Password: YOUR_ACCESS_TOKEN
   - ID: `DOCKERHUB_CREDS`

### Step 3: Jenkins - Create Pipeline Job (3 min)
1. New Item
2. Name: `devops-app-pipeline`
3. Type: Pipeline
4. General:
   - GitHub project: https://github.com/1o26/devops-project
5. Pipeline:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository: https://github.com/1o26/devops-project.git
   - Branch: */main
   - Script Path: Jenkinsfile
6. Save

### Step 4: Run First Build (5 min)
1. Click Build Now
2. Watch Console Output
3. Should see: Checkout → Lint → Tests → Docker Build → Docker Push

---

## 📌 IMPORTANT NOTE

**For Kubernetes Deploy Stage:**

The pipeline will try to deploy to Kubernetes.

**If Kubernetes is not ready:**
- First 4 stages (Checkout, Lint, Tests, Docker Build, Docker Push) will pass ✅
- Kubernetes Deploy stage may fail ❌
- But that's OK for now - you can fix later

**To fix Kubernetes issues:**
1. Set up Docker Desktop Kubernetes OR Minikube
2. Get kubeconfig working: `kubectl get nodes`
3. Create KUBE_CONFIG credential in Jenkins
4. Re-run pipeline

---

## 🚀 RECOMMENDED ORDER

1. **TODAY:** Docker Hub + Jenkins + First Pipeline Run
   - Docker/Slack stages should work
   - K8s stage may fail (that's ok)

2. **LATER:** Fix Kubernetes
   - Set up K8s cluster
   - Get kubeconfig
   - Create KUBE_CONFIG credential
   - Re-run pipeline

---

## QUICK CHECKLIST

### Before First Build
- [ ] Docker Hub account created
- [ ] Access token generated and saved
- [ ] Jenkinsfile updated with YOUR username (line 31)
- [ ] DOCKERHUB_CREDS credential created in Jenkins
- [ ] devops-app-pipeline job created in Jenkins

### First Build Expectations
- [x] Checkout - will pass
- [x] Lint - will pass
- [x] Unit Tests - will pass ✅ 23/23
- [x] Docker Build - will pass (if Docker running)
- [x] Docker Push - will pass (if creds correct)
- [?] Kubernetes Deploy - depends on K8s setup
- [?] Slack Notifications - depends on webhook

---

## 📞 NEXT STEP

**Go create Docker Hub account** and let me know when you're done! 

Then we'll set up Jenkins and run your first pipeline! 🎯
