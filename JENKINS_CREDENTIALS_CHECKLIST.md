# Jenkins Credentials Checklist

Use this checklist to track your credential creation:

## [ ] Credential 1: Docker Hub (DOCKERHUB_CREDS)

- [ ] Go to Jenkins Dashboard
- [ ] Click: Manage Jenkins → Manage Credentials → System → Global credentials
- [ ] Click: Add Credentials
- [ ] Kind: Username with password
- [ ] Username: _________________________ (your Docker Hub username)
- [ ] Password: _________________________ (your access token)
- [ ] ID: DOCKERHUB_CREDS
- [ ] Description: Docker Hub credentials for image push
- [ ] Click: Create
- [ ] Verify: See DOCKERHUB_CREDS in credentials list

**How to get Docker Hub Access Token:**
1. Go to https://hub.docker.com
2. Account Settings → Security
3. Click "New Access Token"
4. Name: jenkins-devops
5. Permissions: Read, Write, Delete
6. Generate and COPY the token

**Test locally:**
```bash
docker login
# Username: YOUR_USERNAME
# Password: YOUR_TOKEN (paste it)
```

---

## [ ] Credential 2: Kubernetes Config (KUBE_CONFIG)

- [ ] Go to: Jenkins Dashboard → Manage Credentials → System → Global credentials
- [ ] Click: Add Credentials
- [ ] Kind: Secret file
- [ ] File: Upload kubeconfig file
  - Location: `~/.kube/config` on Linux/Mac
  - Location: `C:\Users\YOUR_USERNAME\.kube\config` on Windows
- [ ] ID: KUBE_CONFIG
- [ ] Description: Kubernetes config for cluster access
- [ ] Click: Create
- [ ] Verify: See KUBE_CONFIG in credentials list

**How to find your kubeconfig:**
```bash
# Linux/Mac
cat ~/.kube/config

# Windows PowerShell
Get-Content $env:USERPROFILE\.kube\config

# Or if using Docker Desktop:
# File location varies, check Docker Desktop settings
```

**If you don't have kubeconfig:**
- Ask your Kubernetes cluster admin for it
- Or set up Kubernetes locally: https://kubernetes.io/docs/setup/learning-environment/minikube/

**Test locally:**
```bash
kubectl config view
kubectl get nodes
```

---

## [ ] Credential 3: Slack Webhook (SLACK_WEBHOOK_URL)

- [ ] Go to: Jenkins Dashboard → Manage Credentials → System → Global credentials
- [ ] Click: Add Credentials
- [ ] Kind: Secret text
- [ ] Secret: _________________________ (paste webhook URL)
- [ ] ID: SLACK_WEBHOOK_URL
- [ ] Description: Slack webhook for pipeline notifications
- [ ] Click: Create
- [ ] Verify: See SLACK_WEBHOOK_URL in credentials list

**How to create Slack Webhook:**
1. Go to your Slack workspace
2. Click workspace name (top left)
3. Select "Settings & administration" → "Manage apps"
4. Search "Incoming Webhooks"
5. Click "Create New"
6. Choose a channel (e.g., #devops, #jenkins)
7. Click "Create Incoming Webhook"
8. COPY the webhook URL

**Example webhook URL:**
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
```

**Test locally:**
```bash
$webhook = "YOUR_WEBHOOK_URL"
$body = @{
    text = "Test message from Jenkins"
} | ConvertTo-Json

Invoke-WebRequest -Uri $webhook -Method Post -Body $body -ContentType "application/json"
```

---

## Summary Checklist

Once all credentials are created, you should see:

```
Global credentials (unrestricted)

✅ DOCKERHUB_CREDS (Username with password)
✅ KUBE_CONFIG (Secret file)
✅ SLACK_WEBHOOK_URL (Secret text)
```

If you see all three ✅, you're ready to create the Jenkins Pipeline job!

---

## Important Notes

⚠️ **DO NOT** hardcode credentials in Jenkinsfile
⚠️ **DO NOT** share webhook URLs or tokens
⚠️ **DO** use the exact credential IDs (case-sensitive):
   - `DOCKERHUB_CREDS` (not `dockerhub`, `docker_creds`, etc.)
   - `KUBE_CONFIG` (not `kubeconfig`, `k8s_config`, etc.)
   - `SLACK_WEBHOOK_URL` (not `slack`, `slack_webhook`, etc.)

---

## Next Step

Once all 3 credentials are created, go to: **JENKINS_SETUP_VISUAL.md**
And follow **PART 2: Create Pipeline Job**
