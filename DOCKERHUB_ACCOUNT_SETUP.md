# Docker Hub Account Setup - EASY STEPS

## Step 1: Create Docker Hub Account

1. Go to: https://hub.docker.com
2. Click "Sign Up"
3. Fill in:
   - Email: your_email@example.com
   - Username: **YOUR_DOCKER_HUB_USERNAME** (remember this!)
   - Password: Strong password
4. Verify email
5. Login to Docker Hub

---

## Step 2: Generate Access Token

This is what Jenkins will use to push images.

**Steps:**
1. Login to https://hub.docker.com
2. Click your username (top right) → Account Settings
3. Click **Security** (left sidebar)
4. Click **New Access Token**
5. Token name: `jenkins-devops`
6. Permissions: Select "Read, Write, Delete"
7. Click **Generate**

**IMPORTANT:** Copy the token and save it somewhere safe!
You won't see it again if you close the page.

**Example token:**
```
dckr_pat_XXXXXXXXXXXXXXXXXXXXXXXX
```

---

## Step 3: Update Jenkinsfile with Your Username

Edit your local file: `Jenkinsfile`

Find line 11:
```groovy
IMAGE = "mydockerhubuser/my-devops-app"
```

Replace `mydockerhubuser` with your Docker Hub username:
```groovy
IMAGE = "YOUR_DOCKER_HUB_USERNAME/my-devops-app"
```

**Example:**
```groovy
IMAGE = "john-smith/my-devops-app"
```

---

## Step 4: Test Docker Login (Optional)

If you have Docker running locally, test your credentials:

```powershell
docker login
```

When prompted:
- Username: `YOUR_DOCKER_HUB_USERNAME`
- Password: `YOUR_ACCESS_TOKEN` (paste the full token)

If successful, you'll see:
```
Login Succeeded
```

---

## Step 5: Create Jenkins Credential

In Jenkins:

1. Go to **Manage Jenkins** → **Manage Credentials** → **System** → **Global credentials**
2. Click **Add Credentials**
3. Fill in:
   - Kind: `Username with password`
   - Username: `YOUR_DOCKER_HUB_USERNAME`
   - Password: `YOUR_ACCESS_TOKEN` (the long token you generated)
   - ID: `DOCKERHUB_CREDS` (exactly this!)
   - Description: `Docker Hub credentials for image push`
4. Click **Create**

---

## What Happens in Jenkins Pipeline

When you run the pipeline:

1. Jenkins uses `DOCKERHUB_CREDS` to login to Docker Hub
2. Builds image: `YOUR_USERNAME/my-devops-app:BUILD_NUMBER`
3. Pushes to: `https://hub.docker.com/r/YOUR_USERNAME/my-devops-app`

**Example:**
```
Build #1: john-smith/my-devops-app:1
Build #2: john-smith/my-devops-app:2
Latest: john-smith/my-devops-app:latest
```

---

## View Your Images on Docker Hub

After Jenkins pipeline runs:

1. Go to: https://hub.docker.com/r/YOUR_USERNAME/my-devops-app
2. You should see:
   - Tags: latest, 1, 2, 3, etc.
   - Image details
   - Pull command

**Pull and run locally:**
```bash
docker pull YOUR_USERNAME/my-devops-app:latest
docker run -p 5000:5000 YOUR_USERNAME/my-devops-app:latest
```

---

## Summary

| Item | Your Value |
|------|---|
| Docker Hub Username | _________________________ |
| Docker Hub Email | _________________________ |
| Access Token | dckr_pat_XXXXXXXXXXXXXXX... |
| Jenkins Image Name | YOUR_USERNAME/my-devops-app |
| Jenkins Credential ID | DOCKERHUB_CREDS |

---

## Quick Checklist

- [ ] Created Docker Hub account
- [ ] Generated access token
- [ ] Saved access token somewhere safe
- [ ] Updated Jenkinsfile with username
- [ ] Created Jenkins credential DOCKERHUB_CREDS
- [ ] Verified credential in Jenkins

Once done, you're ready for the full Jenkins setup!
