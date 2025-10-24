# Deployment Guide

This guide covers deployment options for the EduLearn platform.

## Local Development

See the main [README.md](README.md) for local setup instructions.

## Docker Compose Deployment

### Development
```bash
docker-compose up --build
```

### Production
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/edulearn
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=edulearn
      - POSTGRES_USER=edulearn_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## AWS ECS Deployment

### Step 1: Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Terraform** installed (>= 1.3.0)
4. **Docker** installed

### Step 2: Configure AWS

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., eu-central-1)
```

### Step 3: Set Up Terraform

1. **Create terraform.tfvars:**
```hcl
aws_region = "eu-central-1"
environment = "dev"
project_name = "edulearn"
db_password = "YourSecurePassword123!"
backend_image_tag = "latest"
frontend_image_tag = "latest"
```

2. **Initialize Terraform:**
```bash
cd terraform
terraform init
```

3. **Review the plan:**
```bash
terraform plan
```

4. **Apply the infrastructure:**
```bash
terraform apply
```

This will create:
- VPC with public/private subnets
- ECR repositories
- RDS PostgreSQL database
- ECS cluster
- Application Load Balancer
- Security groups
- IAM roles

### Step 4: Build and Push Docker Images

After ECR repositories are created:

```bash
# Get ECR login command
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-central-1.amazonaws.com

# Build and push backend
cd backend
docker build -t edulearn-backend .
docker tag edulearn-backend:latest <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-backend:latest
docker push <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-backend:latest

# Build and push frontend
cd ../frontend
docker build -t edulearn-frontend .
docker tag edulearn-frontend:latest <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-frontend:latest
docker push <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-frontend:latest
```

### Step 5: Deploy Services

ECS services should automatically deploy. Check status:

```bash
aws ecs list-services --cluster edulearn-cluster
aws ecs describe-services --cluster edulearn-cluster --services edulearn-backend-service
```

### Step 6: Get Application URL

```bash
terraform output alb_dns_name
```

Access:
- Frontend: `http://<alb-dns-name>`
- Backend API: `http://<alb-dns-name>:8000`
- API Docs: `http://<alb-dns-name>:8000/docs`

## CI/CD with GitHub Actions

### Setup

1. **Add GitHub Secrets:**
   - Go to repository Settings > Secrets and variables > Actions
   - Add:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`

2. **Workflow runs automatically on:**
   - Push to `main` branch
   - Pull requests to `main`

3. **Workflow includes:**
   - Backend tests
   - Docker image builds
   - Push to ECR
   - Optional Terraform deployment

## Database Migration

### Using Alembic (Recommended)

```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Manual Setup

The application automatically creates tables on startup via SQLAlchemy's `create_all()`.

## Monitoring

### CloudWatch Logs

ECS services automatically send logs to CloudWatch:
- Backend logs: `/ecs/edulearn/backend`
- Frontend logs: `/ecs/edulearn/frontend`

### Health Checks

- Backend: `http://<url>:8000/health`
- Frontend: `http://<url>/`

## Scaling

### Manual Scaling

Update ECS service desired count:
```bash
aws ecs update-service --cluster edulearn-cluster --service edulearn-backend-service --desired-count 3
```

### Auto Scaling

Add auto-scaling policies:
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/edulearn-cluster/edulearn-backend-service \
  --min-capacity 2 \
  --max-capacity 10
```

## Security Considerations

1. **Database:**
   - Use strong passwords
   - Enable encryption at rest
   - Use private subnets

2. **Application:**
   - Set secure `SECRET_KEY`
   - Use HTTPS in production
   - Enable ALB SSL/TLS termination

3. **Access:**
   - Restrict security groups
   - Use IAM roles (not users)
   - Enable VPC flow logs

4. **Secrets:**
   - Use AWS Secrets Manager
   - Never commit secrets
   - Rotate credentials regularly

## Troubleshooting

### ECS Tasks Not Starting

1. Check CloudWatch logs
2. Verify security group rules
3. Check task definition
4. Verify image in ECR

### Database Connection Issues

1. Check security group allows ECS tasks
2. Verify database endpoint
3. Check credentials
4. Verify subnet group

### ALB Health Check Failing

1. Check target group health
2. Verify security groups
3. Check container ports
4. Review task logs

## Cost Optimization

- Use `t3.micro` instances for dev
- Enable ECR lifecycle policies
- Set CloudWatch log retention
- Use spot instances for non-critical workloads
- Enable RDS automated backups only when needed

## Backup and Recovery

### Database Backups

RDS automatic backups are enabled by default (7-day retention). Manual snapshot:

```bash
aws rds create-db-snapshot \
  --db-instance-identifier edulearn-db \
  --db-snapshot-identifier edulearn-snapshot-$(date +%Y%m%d)
```

### Restore from Snapshot

```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier edulearn-db-restored \
  --db-snapshot-identifier edulearn-snapshot-YYYYMMDD
```
