# Docker Hub Setup Instructions

## Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com
2. Sign up (or log in if you have an account)
3. Verify your email

## Step 2: Create Access Token

1. Go to Account Settings → Security
2. Click "New Access Token"
3. Token name: `jenkins-devops`
4. Permissions: Select "Read, Write, Delete"
5. Click "Generate"
6. **COPY THE TOKEN** (you won't see it again!)

## Step 3: Update Jenkinsfile Image Name

Edit `Jenkinsfile` in your project and change:

```groovy
IMAGE = "YOUR_DOCKER_HUB_USERNAME/my-devops-app"
```

Replace `YOUR_DOCKER_HUB_USERNAME` with your actual Docker Hub username.

## Step 4: Test Login Locally

```bash
docker login
# Username: your_docker_hub_username
# Password: your_access_token
```

If successful, you can push images to Docker Hub.

## Step 5: Create Jenkins Credentials

In Jenkins:
1. Manage Credentials → Global
2. Add Credentials
3. Kind: Username with password
4. Username: `YOUR_DOCKER_HUB_USERNAME`
5. Password: `YOUR_ACCESS_TOKEN`
6. ID: `DOCKERHUB_CREDS`

## Expected Pipeline Push

When pipeline runs "Docker Push" stage:
1. Authenticate to Docker Hub
2. Push image: `YOUR_USERNAME/my-devops-app:BUILD_NUMBER`
3. Push latest tag: `YOUR_USERNAME/my-devops-app:latest`

## Verify in Docker Hub

After first successful build:
1. Go to https://hub.docker.com/r/YOUR_USERNAME/my-devops-app
2. You should see:
   - Tags: `latest`, `1`, `2`, etc.
   - Image details and layers
   - Pull commands

## Pull and Run Image

Once pushed:

```bash
docker pull YOUR_USERNAME/my-devops-app:latest
docker run -p 5000:5000 YOUR_USERNAME/my-devops-app:latest
```

## Cleanup Old Images (Optional)

Keep your Docker Hub registry clean:
1. Go to repository → Tags
2. Delete old tags to save space
3. Docker Hub free tier allows 1 private repo
