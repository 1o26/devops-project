# Jenkins Setup Instructions

## Prerequisites
- Jenkins installed and running
- Docker installed on Jenkins agents
- kubectl installed on Jenkins agents
- Git plugin configured

## Step 1: Create Jenkins Credentials

Go to **Jenkins Dashboard → Manage Credentials → System → Global credentials**

### 1.1 Docker Hub Credentials (DOCKERHUB_CREDS)
1. Click "Add Credentials"
2. Kind: **Username with password**
3. Username: Your Docker Hub username
4. Password: Your Docker Hub access token (generate from Docker Hub settings)
5. ID: `DOCKERHUB_CREDS`
6. Click "Create"

### 1.2 Kubernetes Config (KUBE_CONFIG)
1. Click "Add Credentials"
2. Kind: **Secret file**
3. File: Upload your `~/.kube/config` file
4. ID: `KUBE_CONFIG`
5. Click "Create"

### 1.3 Slack Webhook (SLACK_WEBHOOK_URL)
1. Click "Add Credentials"
2. Kind: **Secret text**
3. Secret: Your Slack incoming webhook URL
   - Go to Slack workspace → Apps → Create New App → Incoming Webhooks
   - Copy the webhook URL
4. ID: `SLACK_WEBHOOK_URL`
5. Click "Create"

## Step 2: Create Pipeline Job

1. Go to Jenkins Dashboard
2. Click "New Item"
3. Job name: `devops-app-pipeline`
4. Type: **Pipeline**
5. Click "OK"

## Step 3: Configure Pipeline Job

### General Tab
- Check "GitHub project"
- Project url: `https://github.com/YOUR_USERNAME/devops-project`
- Check "GitHub hook trigger for GITScm polling"

### Build Triggers
- Check "GitHub hook trigger for GITScm polling"

### Pipeline Tab
- Definition: **Pipeline script from SCM**
- SCM: **Git**
  - Repository URL: `https://github.com/YOUR_USERNAME/devops-project.git`
  - Branch: `*/main`
  - Script Path: `Jenkinsfile`

## Step 4: Run First Build

1. Click "Build Now" to trigger pipeline
2. Monitor build progress in "Build History"
3. Check "Console Output" for logs

## Expected Pipeline Output

```
✅ Checkout - Clone repository
✅ Lint - Code quality checks
✅ Unit Tests - pytest execution
✅ Docker Build - Image creation
✅ Docker Push - Upload to Docker Hub
✅ Kubernetes Deploy - Update cluster
✅ Slack Notifications - Send status
```

## Troubleshooting

### Build Fails at Docker Build
- Ensure Docker is installed: `docker --version`
- Check Jenkins agent has Docker access

### Build Fails at Kubernetes Deploy
- Verify kubeconfig is valid: `kubectl config view`
- Ensure user has cluster permissions

### Slack Notifications Not Sent
- Verify SLACK_WEBHOOK_URL credential is correct
- Check Slack workspace allows webhooks

### GitHub Webhook Not Triggering
- Verify webhook is active in repository settings
- Check Jenkins webhook URL is accessible
- Look at recent deliveries in GitHub Webhooks settings

## Pipeline Environment Variables

The Jenkinsfile uses these variables (defined in pipeline):
- `IMAGE`: Docker Hub image name
- `TAG`: Build number
- `KUBE_NAMESPACE`: Kubernetes namespace (default: default)

To modify, edit the `environment` section in Jenkinsfile.

## Next Steps

After successful first build:
1. Push code changes to GitHub
2. GitHub webhook automatically triggers Jenkins
3. Monitor build in Jenkins dashboard
4. Check Slack for notifications
5. Verify pods running in Kubernetes: `kubectl get pods -l app=devops-app`
