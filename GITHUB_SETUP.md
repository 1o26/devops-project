# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `devops-project`
3. Set to Public (for resume visibility)
4. Click "Create repository"
5. Copy the repository URL (HTTPS or SSH)

## Step 2: Push Your Project

Run these commands:

```bash
cd "c:\Users\User\Desktop\Projects\DevOps project"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/devops-project.git

# Rename branch to main (optional)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Webhook for Jenkins

1. Go to your repository settings: Settings → Webhooks
2. Click "Add webhook"
3. Payload URL: `http://YOUR_JENKINS_URL/github-webhook/`
4. Content type: `application/json`
5. Events: Select "Just the push event"
6. Check "Active"
7. Click "Add webhook"

## Your Repository URL

After pushing, your project will be available at:
```
https://github.com/YOUR_USERNAME/devops-project
```

Add this link to your resume!
