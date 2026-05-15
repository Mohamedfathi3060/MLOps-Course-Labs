# GitHub Actions Setup Checklist

Complete these steps to fully configure the CI/CD pipeline:

## 1. Docker Hub Setup
- [ ] Create Docker Hub account if not already done: https://hub.docker.com
- [ ] Generate access token: https://hub.docker.com/settings/security
- [ ] Add GitHub Secrets:
  - [ ] `DOCKER_USERNAME` = your Docker Hub username
  - [ ] `DOCKER_PASSWORD` = your generated access token

## 2. AWS ECR Setup (Optional - skip if using Docker Hub only)
- [ ] Get AWS Account ID (12-digit number)
- [ ] Create IAM user with ECR permissions or use existing credentials
- [ ] Add GitHub Secrets:
  - [ ] `AWS_ACCOUNT_ID` = your 12-digit AWS account ID
  - [ ] `AWS_ACCESS_KEY_ID` = IAM access key
  - [ ] `AWS_SECRET_ACCESS_KEY` = IAM secret key
  - [ ] `AWS_REGION` = your region (e.g., us-east-1)

## 3. EC2 Instance Setup
- [ ] Launch EC2 instance (Ubuntu 20.04 LTS or later recommended)
- [ ] Copy EC2 public IP or DNS
- [ ] SSH into EC2 and run these commands:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io

# Add current user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Create SSH directory if needed
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

## 4. Generate SSH Key for GitHub Actions
Run on your EC2 instance (or local machine):

```bash
# Generate a new SSH key (no passphrase)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github-actions -N ""

# Add public key to authorized_keys
cat ~/.ssh/github-actions.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Display private key for GitHub Secrets
cat ~/.ssh/github-actions
```

- [ ] Copy the private key output
- [ ] Add GitHub Secrets:
  - [ ] `EC2_HOST` = public IP or DNS of your EC2 instance
  - [ ] `EC2_USER` = username (usually `ubuntu`)
  - [ ] `EC2_SSH_KEY` = paste the entire private key here (multi-line)

## 5. Add GitHub Secrets
Go to: Repository → Settings → Secrets and variables → Actions

Add all required secrets based on your setup choice:

### Minimum (Docker Hub only):
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`

### Full Setup (Docker Hub + ECR + EC2):
- All of the above, plus:
- `AWS_ACCOUNT_ID`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

## 6. Test the Pipeline
- [ ] Make a test commit and push to a branch (not main)
- [ ] Verify tests pass in GitHub Actions
- [ ] Create a PR to verify the workflow
- [ ] Merge to main and verify full deployment

## 7. Verify Deployment
SSH into your EC2 and check:

```bash
# List running containers
docker ps

# Check logs
docker logs churn-prediction-api

# Test health endpoint (on EC2)
curl http://localhost:8000/health

# If accessing from outside, use your EC2 public IP
curl http://<EC2_PUBLIC_IP>:8000/health
```

## Troubleshooting

**Workflow not triggering?**
- Check that you've pushed to `main` or `develop` branch
- Review workflow file is in `.github/workflows/ci-cd.yml`

**Tests failing?**
- Run locally: `uv run pytest tests/ -v`
- Check Python version matches (3.12)

**Docker push fails?**
- Verify Docker Hub credentials
- Check token hasn't expired

**EC2 deployment fails?**
- SSH manually: `ssh -i <your_key> ubuntu@<EC2_IP>`
- Check Docker is running: `docker ps`
- Check Docker can pull images: `docker pull python:3.12-slim`

**Container not starting?**
- Check logs: `docker logs churn-prediction-api`
- Verify port 8000 isn't already in use: `netstat -tuln | grep 8000`

## Next Steps
- Set up HTTPS/SSL certificate for your EC2 (consider using Nginx + Let's Encrypt)
- Configure auto-scaling or load balancer if needed
- Set up monitoring and alerting
- Consider adding database backups if applicable
