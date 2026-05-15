# GitHub Actions CI/CD Configuration

This workflow automates testing, building, and deploying the Churn Prediction API.

## Workflow Stages

### 1. **Test Stage** (Runs on every push and PR)
   - Sets up Python 3.12 environment
   - Installs dependencies using `uv`
   - Runs code linting with Ruff
   - Runs pytest with coverage reports
   - Uploads coverage to Codecov

### 2. **Build & Push Stage** (Runs only on main/develop branch pushes)
   - Builds Docker image
   - Pushes to Docker Hub (primary)
   - Optionally pushes to AWS ECR (if configured)

### 3. **Deploy Stage** (Runs only on main branch)
   - Connects to EC2 instance via SSH
   - Pulls latest Docker image
   - Stops old container and starts new one
   - Verifies deployment with health checks

## Required GitHub Secrets

Configure these secrets in your repository settings (Settings → Secrets and variables → Actions):

### Docker Hub Credentials
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub access token (generate at https://hub.docker.com/settings/security)

### AWS ECR (Optional - for ECR instead of/in addition to Docker Hub)
- `AWS_ACCOUNT_ID` - Your AWS account ID
- `AWS_ACCESS_KEY_ID` - AWS IAM access key
- `AWS_SECRET_ACCESS_KEY` - AWS IAM secret key
- `AWS_REGION` - AWS region (e.g., us-east-1)

### EC2 Deployment
- `EC2_HOST` - Public IP or DNS of your EC2 instance
- `EC2_USER` - SSH username (usually `ubuntu` or `ec2-user`)
- `EC2_SSH_KEY` - Private SSH key (multi-line format: copy entire private key content)

## EC2 Setup Instructions

1. **Install Docker on EC2:**
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER
newgrp docker
```

2. **Generate SSH key for GitHub Actions:**
```bash
ssh-keygen -t rsa -b 4096 -f github-actions-key -N ""
cat github-actions-key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

3. **Add private key to GitHub Secrets as `EC2_SSH_KEY`**

## Local Testing

Test the Docker build locally:
```bash
docker build -t churn-prediction-api:latest .
docker run -p 8000:8000 churn-prediction-api:latest
curl http://localhost:8000/schema/swagger
```

## Workflow Triggers

- **On Push:** To `main` or `develop` branches
- **On Pull Request:** Against `main` or `develop` branches
- **Manual Trigger:** Can be added to the workflow if needed

## Pipeline Flow

```
[Push/PR] → [Test] → [Build & Push Docker] → [Deploy to EC2]
     ↓                      ↓                        ↓
  Always            Only on main/develop    Only on main push
   Runs              push (after tests)      (after build success)
```

## Monitoring

Check workflow execution in:
- GitHub Actions tab in your repository
- Look for status badges in PR comments
- Check Codecov for coverage reports

## Troubleshooting

**Tests failing?**
- Run locally: `uv run pytest tests/ -v`

**Docker push failing?**
- Verify Docker Hub token: https://hub.docker.com/settings/security
- Check `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets

**EC2 deployment failing?**
- Verify EC2 instance is running
- Check SSH key permissions: `chmod 600 ~/.ssh/authorized_keys`
- Test SSH manually: `ssh -i your-key ec2-user@your-ec2-ip`
- Verify Docker is installed on EC2
