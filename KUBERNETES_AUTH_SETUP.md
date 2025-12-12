# Kubernetes Setup - Authentication Required

Your kubectl is trying to connect but needs authentication. Here's how to fix it.

---

## Check Your kubeconfig

First, let's see what kubeconfig file you have:

```powershell
# Check if kubeconfig exists
Test-Path $env:USERPROFILE\.kube\config

# View current kubeconfig
kubectl config view

# Show kubeconfig location
$env:KUBECONFIG
```

---

## Fix Authentication - Option 1: Docker Desktop (Easiest)

If you have **Docker Desktop**, it includes Kubernetes:

1. Open **Docker Desktop**
2. Settings → Kubernetes
3. Check **Enable Kubernetes**
4. Wait for it to start (shows green light)

Then verify:
```powershell
kubectl cluster-info
kubectl get nodes
```

---

## Fix Authentication - Option 2: Minikube

If you want a local Kubernetes cluster:

1. Install Minikube: https://minikube.sigs.k8s.io/docs/start/
2. Start cluster:
   ```powershell
   minikube start
   ```
3. Verify:
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

---

## Fix Authentication - Option 3: Existing Cluster

If you have access to a remote cluster (cloud or on-prem):

1. **Get kubeconfig from admin**
   - They should give you a `.kubeconfig` or `config` file
   - Or provide credentials to download it

2. **Place kubeconfig file:**
   ```powershell
   # Create .kube directory if it doesn't exist
   mkdir $env:USERPROFILE\.kube -Force
   
   # Copy kubeconfig file there
   Copy-Item -Path "C:\path\to\config" -Destination "$env:USERPROFILE\.kube\config"
   ```

3. **Verify access:**
   ```powershell
   kubectl cluster-info
   kubectl get nodes
   ```

---

## Troubleshooting

### Problem: "Authentication required"
**Solution:**
- Get valid kubeconfig from cluster admin
- Make sure kubeconfig has correct permissions
- Check kubeconfig file isn't corrupted

### Problem: "Connection refused"
**Solution:**
- Make sure Kubernetes cluster is running
- Check cluster IP in kubeconfig is correct
- Make sure firewall allows connection

### Problem: Can't find kubeconfig
**Solution:**
```powershell
# Standard location
$env:USERPROFILE\.kube\config

# Docker Desktop
$env:USERPROFILE\.kube\docker-desktop\kubeconfig.yml

# Minikube
$env:USERPROFILE\.minikube\profiles\minikube\kubeconfig.yaml
```

---

## For Jenkins Pipeline

Once you have working kubectl:

1. Get kubeconfig content:
   ```powershell
   Get-Content $env:USERPROFILE\.kube\config
   ```

2. In Jenkins:
   - Create credential: **KUBE_CONFIG**
   - Type: **Secret file**
   - Upload the kubeconfig file
   - ID: `KUBE_CONFIG` (exact!)

---

## What You Need to Deploy

For the Jenkins pipeline to work:
- ✅ Working kubectl access (can run `kubectl get nodes`)
- ✅ Valid kubeconfig file
- ✅ Credentials to access Kubernetes cluster

---

## Recommended for Testing

For resume purposes, use **Docker Desktop with Kubernetes enabled**:
- No extra setup needed
- Easy to manage
- Perfect for testing pipeline
- Can show working Kubernetes deployment

---

## Next Steps

1. **Set up Kubernetes access** (Docker Desktop or Minikube)
2. **Verify:** `kubectl get nodes` works
3. **Get kubeconfig file** path
4. **Then:** Create KUBE_CONFIG credential in Jenkins

Once `kubectl get nodes` works without errors, you're ready for Jenkins setup!

---

## Status Check

Run these to verify setup:

```powershell
# 1. Check Docker
docker --version

# 2. Check kubectl
kubectl version --client

# 3. Check cluster access (this should work)
kubectl cluster-info

# 4. Check nodes (this should show nodes)
kubectl get nodes

# 5. Check kubeconfig location
$env:KUBECONFIG
ls $env:USERPROFILE\.kube\
```

If all 5 show output without errors, you're ready! ✅
