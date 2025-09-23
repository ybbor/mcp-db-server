# GitHub Secrets Setup Guide

This guide explains how to set up the required GitHub Secrets for the CI/CD pipeline.

## 🔐 Required Secrets

Your GitHub Actions workflow requires these secrets to function properly:

### Docker Hub Secrets
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

## 📋 Step-by-Step Setup

### Step 1: Go to Repository Settings
1. Open your repository: https://github.com/Souhar-dya/mcp-db-server
2. Click on the **Settings** tab (top right of the repository page)
3. In the left sidebar, scroll down and click **Secrets and variables** → **Actions**

### Step 2: Add Docker Hub Secrets

#### Add DOCKER_USERNAME
1. Click **"New repository secret"**
2. **Name:** `DOCKER_USERNAME`
3. **Secret:** `souhardyak` (your Docker Hub username)
4. Click **"Add secret"**

#### Add DOCKER_PASSWORD
1. Click **"New repository secret"** again
2. **Name:** `DOCKER_PASSWORD`
3. **Secret:** Your Docker Hub password OR access token (recommended)
4. Click **"Add secret"**

### Step 3: Get Docker Hub Access Token (Recommended)

For better security, use an access token instead of your password:

1. Go to https://hub.docker.com/settings/security
2. Click **"New Access Token"**
3. **Access Token Description:** `GitHub Actions - MCP DB Server`
4. **Access permissions:** `Read, Write, Delete`
5. Click **"Generate"**
6. **Copy the token** (you won't see it again!)
7. Use this token as your `DOCKER_PASSWORD` secret

## 🎯 What Each Secret Does

| Secret | Purpose | Example Value |
|--------|---------|---------------|
| `DOCKER_USERNAME` | Docker Hub login username | `souhardyak` |
| `DOCKER_PASSWORD` | Docker Hub login credential | `dckr_pat_ABC123...` (access token) |

## ✅ Verification

After adding secrets, you should see them listed in your repository's Actions secrets:

```
Repository secrets
├── DOCKER_USERNAME ✅
└── DOCKER_PASSWORD ✅
```

## 🚀 What Happens After Setup

Once secrets are configured, your GitHub Actions will:

1. **✅ Run comprehensive tests** (PostgreSQL, MySQL, SQLite)
2. **✅ Build Docker image** for multiple architectures (AMD64, ARM64)  
3. **✅ Push to Docker Hub** as `souhardyak/mcp-db-server:latest`
4. **✅ Run security scans** with Trivy
5. **✅ Test the built Docker image** 

## 🔧 Troubleshooting

### "Username and password required" error
- Check that `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set
- Verify the secret names are exactly: `DOCKER_USERNAME` and `DOCKER_PASSWORD`
- Make sure the Docker Hub credentials are correct

### "Authentication failed" error  
- Verify your Docker Hub username/password are correct
- Try using an access token instead of password
- Check if your Docker Hub account is active

### Secrets not appearing
- Make sure you're in the correct repository
- Refresh the page after adding secrets
- Check you have admin access to the repository

## 📚 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Hub Access Tokens](https://docs.docker.com/docker-hub/access-tokens/)
- [GitHub Actions Docker Login](https://github.com/docker/login-action)

---

## 🎉 Ready to Go!

After setting up these secrets, push any changes to trigger the CI/CD pipeline:

```bash
git add .
git commit -m "Add comprehensive CI/CD pipeline"
git push
```

Your workflow will automatically:
- Test all database types (PostgreSQL, MySQL, SQLite)
- Build and publish Docker images
- Run security scans
- Validate the final Docker image works correctly