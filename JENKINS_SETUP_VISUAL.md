# Jenkins Setup - Step by Step Visual Guide

## Prerequisites Check

Before starting, verify you have:

```powershell
# Check Jenkins is running
# Go to http://localhost:8080 (or your Jenkins URL)

# Check Docker is installed
docker --version

# Check kubectl is installed
kubectl version --client
```

---

## PART 1: Create Jenkins Credentials (3 Required)

### Credential 1: Docker Hub (DOCKERHUB_CREDS)

**Steps:**
1. Open Jenkins Dashboard: `http://localhost:8080`
2. Click **Manage Jenkins** (left sidebar)
3. Click **Manage Credentials**
4. Click **System** (left sidebar)
5. Click **Global credentials (unrestricted)** (right side)
6. Click **Add Credentials** (top left)

**Fill in:**
- Kind: `Username with password`
- Username: `YOUR_DOCKER_HUB_USERNAME`
- Password: `YOUR_DOCKER_HUB_ACCESS_TOKEN`
  - Get token from: Docker Hub → Account Settings → Security → New Access Token
- ID: `DOCKERHUB_CREDS` ← **MUST BE EXACT**
- Description: `Docker Hub credentials for image push`
- Click **Create**

**Expected Result:**
You should see `DOCKERHUB_CREDS` in the credentials list.

---

### Credential 2: Kubernetes Config (KUBE_CONFIG)

**Steps:**
1. Go back to **Global credentials** (same page as above)
2. Click **Add Credentials** (top left)

**Fill in:**
- Kind: `Secret file`
- File: **Upload your kubeconfig file**
  - Location: `~/.kube/config` (or `C:\Users\YOUR_USERNAME\.kube\config`)
  - If you don't have it, get it from your Kubernetes cluster admin
- ID: `KUBE_CONFIG` ← **MUST BE EXACT**
- Description: `Kubernetes config for cluster access`
- Click **Create**

**Expected Result:**
You should see `KUBE_CONFIG` in the credentials list.

---

### Credential 3: Slack Webhook (SLACK_WEBHOOK_URL)

**Steps:**
1. Go back to **Global credentials**
2. Click **Add Credentials** (top left)

**Fill in:**
- Kind: `Secret text`
- Secret: `https://hooks.slack.com/services/YOUR_WEBHOOK_URL`
  - **Get webhook URL:**
    1. Go to your Slack workspace
    2. Click your workspace name (top left)
    3. Select "Settings & administration" → "Manage apps"
    4. Search "Incoming Webhooks"
    5. Click "Create New"
    6. Choose a channel (e.g., #devops)
    7. Click "Create Incoming Webhook"
    8. Copy the webhook URL
- ID: `SLACK_WEBHOOK_URL` ← **MUST BE EXACT**
- Description: `Slack webhook for pipeline notifications`
- Click **Create**

**Expected Result:**
You should see `SLACK_WEBHOOK_URL` in the credentials list.

---

## PART 2: Create Pipeline Job

### Create New Job

**Steps:**
1. Go to Jenkins Dashboard: `http://localhost:8080`
2. Click **New Item** (left sidebar)

**Fill in:**
- Item name: `devops-app-pipeline`
- Type: Select **Pipeline** (the one that looks like a flow diagram)
- Click **OK**

---

### Configure Job - General Tab

You're now in the job configuration page.

**General Section:**
- Check box: **GitHub project**
- Project url: `https://github.com/1o26/devops-project`

**Build Triggers Section:**
- Check box: **GitHub hook trigger for GITScm polling**
  - This enables automatic builds when you push to GitHub

---

### Configure Job - Pipeline Tab

Scroll down to **Pipeline** section:

**Definition:** 
- Select: **Pipeline script from SCM** (not "Pipeline script")

**SCM:**
- Select: **Git**
- Repository URL: `https://github.com/1o26/devops-project.git`
- Credentials: (leave blank for public repo, or select if private)
- Branch: `*/main`
- Script Path: `Jenkinsfile`

**Click Save**

---

## PART 3: Test First Build

### Run First Build

**Steps:**
1. Go to job: `devops-app-pipeline`
2. Click **Build Now** (left sidebar)

**Monitor the build:**
- Click the build number (e.g., `#1`) that appears
- Click **Console Output** to see logs

**Expected stages (in order):**
```
✅ Checkout - Clone repository
✅ Lint - Code quality checks
✅ Unit Tests - pytest execution
✅ Docker Build - Build image
✅ Docker Push - Push to Docker Hub
✅ Kubernetes Deploy - Deploy to cluster
✅ Slack Notifications - Send notification
```

---

## PART 4: Enable GitHub Webhook

### In GitHub Repository

**Steps:**
1. Go to: `https://github.com/1o26/devops-project`
2. Click **Settings** (top right)
3. Click **Webhooks** (left sidebar)
4. Click **Add webhook**

**Fill in:**
- Payload URL: `http://YOUR_JENKINS_URL/github-webhook/`
  - If Jenkins is local: `http://localhost:8080/github-webhook/`
  - If Jenkins is remote: `http://your-jenkins-server.com/github-webhook/`
- Content type: `application/json`
- Events: Select **Just the push event**
- Check: **Active**
- Click **Add webhook**

**Expected Result:**
Green checkmark appears next to the webhook.

---

## PART 5: Test Automatic Trigger

### Push a Change

**Steps:**
1. Make a small change to a file:
   ```bash
   cd "c:\Users\User\Desktop\Projects\DevOps project"
   echo "# Test" >> README.md
   ```

2. Commit and push:
   ```bash
   git add README.md
   git commit -m "Test webhook trigger"
   git push origin main
   ```

3. Watch Jenkins:
   - Go to `http://localhost:8080/job/devops-app-pipeline`
   - A new build should start automatically in ~5 seconds

**Expected Result:**
Build triggers without clicking "Build Now"

---

## Troubleshooting

### Problem: Build Fails at "Docker Build"
**Solution:**
- Ensure Docker is running: `docker ps`
- Check Jenkins agent has Docker access: `docker info`
- Run: `docker login` on the Jenkins agent

### Problem: Build Fails at "Kubernetes Deploy"
**Solution:**
- Verify kubeconfig is valid: `kubectl config view`
- Check cluster access: `kubectl get nodes`
- Ensure user has permissions: `kubectl auth can-i create deployments`

### Problem: Slack Notifications Not Working
**Solution:**
- Verify webhook URL is correct
- Check Slack channel exists and is active
- Test webhook manually:
  ```bash
  curl -X POST YOUR_WEBHOOK_URL -H 'Content-Type: application/json' -d '{"text":"Test"}'
  ```

### Problem: GitHub Webhook Not Triggering
**Solution:**
- Verify webhook is active (green checkmark)
- Check "Recent Deliveries" in webhook settings
- Ensure Jenkins webhook URL is accessible
- Verify branch is "main"

---

## Quick Reference

### All 3 Credentials Needed

| Credential ID | Type | Value | Where to Get |
|---|---|---|---|
| `DOCKERHUB_CREDS` | Username + Password | Docker Hub username + access token | Docker Hub Account Settings → Security |
| `KUBE_CONFIG` | Secret file | kubeconfig file | `~/.kube/config` |
| `SLACK_WEBHOOK_URL` | Secret text | Slack webhook URL | Slack workspace → Manage apps → Incoming Webhooks |

### Job Configuration Summary

| Field | Value |
|---|---|
| Job Name | `devops-app-pipeline` |
| Type | Pipeline |
| GitHub Project | `https://github.com/1o26/devops-project` |
| Git Repository | `https://github.com/1o26/devops-project.git` |
| Branch | `*/main` |
| Script Path | `Jenkinsfile` |
| Build Trigger | GitHub hook trigger for GITScm polling |

---

## What Happens When You Build

1. **Checkout** - Clones your repository
2. **Lint** - Runs flake8 code checks
3. **Unit Tests** - Runs 23 pytest tests
4. **Docker Build** - Builds image: `YOUR_USERNAME/my-devops-app:BUILD_NUMBER`
5. **Docker Push** - Pushes to Docker Hub
6. **Kubernetes Deploy** - Updates K8s deployment
7. **Slack** - Sends notification to Slack

Total time: ~3-5 minutes

---

## Success Indicators

✅ All 3 credentials created and visible in Jenkins
✅ Job created and shows in Jenkins dashboard
✅ First build completes all 7 stages
✅ Docker image appears in Docker Hub
✅ Kubernetes pods updated with new image
✅ Slack notification received
✅ Pushing to GitHub triggers new builds automatically

---

Once you complete these steps, your CI/CD pipeline is fully operational! 🚀
