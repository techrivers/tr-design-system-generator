# 🚀 Deployment Guide

Complete guide for deploying the Design System Generator.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [Container Deployment](#container-deployment)
- [Cloud Deployment](#cloud-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)
- [Scaling](#scaling)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum Hardware:**
- CPU: 2 cores (4+ recommended)
- RAM: 4GB (8GB+ recommended)
- Storage: 10GB free space
- Network: 100Mbps internet connection

**Software Dependencies:**
- Python 3.8 or higher
- Node.js 16 or higher (for generated component libraries)
- Git for version control

### Operating Systems

**Supported:**
- macOS 10.15+
- Ubuntu 18.04+ / CentOS 7+
- Windows 10+ (WSL recommended)
- Docker containers (any platform)

## Local Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd design-system-agent
```

### 2. Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
# Test Python environment
python -c "import fastapi, uvicorn; print('✅ Python dependencies installed')"

# Test basic functionality
python -c "from main import DesignSystemGenerator; print('✅ Core system working')"
```

### 4. Start Development Server

```bash
# Start web interface
uvicorn web.app:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000
```

### 5. Test Component Generation

```python
from main import DesignSystemGenerator
from models import DesignSystemInput, TargetUser, BrandTrait, Platform

# Quick test
generator = DesignSystemGenerator()
input_data = DesignSystemInput(
    product_idea="Test product",
    target_users=[TargetUser.B2B],
    brand_traits=[BrandTrait.MODERN],
    platforms=[Platform.WEB]
)

result = generator.generate_design_system(input_data)
print(f"Generated {len(result.component_library.components)} components")
```

## Production Deployment

### Option 1: Direct Python Deployment

#### 1. Server Setup

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Create application user
sudo useradd -m -s /bin/bash designsystem
sudo su - designsystem
```

#### 2. Application Deployment

```bash
# Clone repository
git clone <repository-url>
cd design-system-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create production configuration
export HOST=0.0.0.0
export PORT=8000
export WORKERS=4
```

#### 3. Process Management with SystemD

Create `/etc/systemd/system/design-system.service`:

```ini
[Unit]
Description=Design System Generator
After=network.target

[Service]
Type=simple
User=designsystem
WorkingDirectory=/home/designsystem/design-system-agent
Environment=PATH=/home/designsystem/design-system-agent/venv/bin
ExecStart=/home/designsystem/design-system-agent/venv/bin/uvicorn web.app:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 4. Start Service

```bash
# Enable and start service
sudo systemctl enable design-system
sudo systemctl start design-system

# Check status
sudo systemctl status design-system

# View logs
sudo journalctl -u design-system -f
```

#### 5. Nginx Reverse Proxy (Optional)

Create `/etc/nginx/sites-available/design-system`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Handle large file uploads (component libraries)
    client_max_body_size 50M;
}
```

### Option 2: Gunicorn + Nginx

#### 1. Install Gunicorn

```bash
pip install gunicorn
```

#### 2. Create Gunicorn Configuration

`gunicorn.conf.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
```

#### 3. Start with Gunicorn

```bash
gunicorn web.app:app -c gunicorn.conf.py
```

## Container Deployment

### Docker Setup

#### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /home/app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership
RUN chown -R app:app /home/app

# Switch to app user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Docker Compose

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  design-system:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./generated:/home/app/generated
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - design-system
    restart: unless-stopped
```

#### 3. Build and Run

```bash
# Build image
docker build -t design-system-generator .

# Run container
docker run -p 8000:8000 design-system-generator

# Or use docker-compose
docker-compose up -d
```

### Kubernetes Deployment

#### 1. Deployment Manifest

`k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: design-system-generator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: design-system-generator
  template:
    metadata:
      labels:
        app: design-system-generator
    spec:
      containers:
      - name: design-system
        image: your-registry/design-system-generator:latest
        ports:
        - containerPort: 8000
        env:
        - name: HOST
          value: "0.0.0.0"
        - name: PORT
          value: "8000"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 2. Service Manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: design-system-service
spec:
  selector:
    app: design-system-generator
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### 3. Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s-deployment.yaml

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/design-system-generator
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Instance Setup

```bash
# Launch EC2 instance (t3.medium recommended)
# Ubuntu 20.04 LTS, security group with ports 22, 80, 443

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nginx -y
```

#### 2. Application Deployment

```bash
# Clone and setup as above
git clone <repository-url>
cd design-system-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. SystemD Service

Same as local deployment, then:

```bash
# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/design-system
sudo ln -s /etc/nginx/sites-available/design-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL with Let's Encrypt (optional)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Vercel/Netlify Deployment

For the web interface only:

#### 1. Build Configuration

`vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web/app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "web/app.py"
    }
  ]
}
```

#### 2. Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## CI/CD Pipeline

### GitHub Actions Example

`.github/workflows/deploy.yml`:
```yaml
name: Deploy Design System Generator

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/ -v
    - name: Type checking
      run: python -c "from main import DesignSystemGenerator; print('Type check passed')"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to production
      run: |
        echo "Deploy logic here"
        # Add your deployment commands
```

### Docker CI/CD

`.github/workflows/docker.yml`:
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker image
      run: docker build -t design-system-generator .
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag design-system-generator your-registry/design-system-generator:latest
        docker push your-registry/design-system-generator:latest
```

## Monitoring

### Application Monitoring

#### 1. Health Check Endpoint

The application includes a health check endpoint:

```bash
curl http://localhost:8000/health
# Returns: {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
```

#### 2. Prometheus Metrics (Optional)

Add `prometheus_client` to requirements and expose metrics:

```python
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### Logging

#### 1. Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
        }
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

#### 2. Log Aggregation

Use tools like ELK stack or CloudWatch for log aggregation.

### Performance Monitoring

#### 1. Response Time Monitoring

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### 2. Memory Usage Monitoring

```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return {
        'rss': process.memory_info().rss / 1024 / 1024,  # MB
        'vms': process.memory_info().vms / 1024 / 1024,  # MB
        'percent': process.memory_percent()
    }
```

## Scaling

### Horizontal Scaling

#### 1. Load Balancer Setup

Using Nginx as load balancer:

```nginx
upstream design_system_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://design_system_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 2. Multiple Worker Processes

```bash
# Start multiple instances
uvicorn web.app:app --host 127.0.0.1 --port 8000 --workers 4
uvicorn web.app:app --host 127.0.0.1 --port 8001 --workers 4
uvicorn web.app:app --host 127.0.0.1 --port 8002 --workers 4
uvicorn web.app:app --host 127.0.0.1 --port 8003 --workers 4
```

### Caching

#### 1. Result Caching

Cache generated design systems:

```python
from cachetools import TTLCache
import hashlib

cache = TTLCache(maxsize=100, ttl=3600)  # 1 hour TTL

def get_cache_key(input_data: DesignSystemInput) -> str:
    data_str = json.dumps(input_data.model_dump(), sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

def generate_with_cache(input_data: DesignSystemInput):
    cache_key = get_cache_key(input_data)

    if cache_key in cache:
        return cache[cache_key]

    result = generator.generate_design_system(input_data)
    cache[cache_key] = result
    return result
```

### Database Integration (Optional)

For persistent caching and analytics:

```python
# models.py additions
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GenerationResult(Base):
    __tablename__ = 'generation_results'

    id = Column(Integer, primary_key=True)
    input_hash = Column(String(32), unique=True)
    input_data = Column(JSON)
    output_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    generation_time = Column(Integer)  # milliseconds
```

## Troubleshooting

### Common Issues

#### 1. Memory Issues

**Symptoms:** Application crashes with memory errors

**Solutions:**
```bash
# Increase system limits
echo 'vm.max_map_count=262144' >> /etc/sysctl.conf
sysctl -p

# Use smaller batch sizes
export MAX_WORKERS=2
export BATCH_SIZE=10
```

#### 2. Port Conflicts

**Symptoms:** Port 8000 already in use

**Solutions:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8001
```

#### 3. File Permission Issues

**Symptoms:** Cannot write generated files

**Solutions:**
```bash
# Create generated directory
mkdir -p generated
chmod 755 generated

# Or run as different user
sudo -u www-data uvicorn web.app:app
```

#### 4. Slow Generation

**Symptoms:** Generation takes too long

**Solutions:**
```bash
# Enable caching
export ENABLE_CACHE=true

# Increase workers
export WORKERS=8

# Use faster storage
# Move to SSD storage
```

#### 5. CORS Issues

**Symptoms:** Browser blocks API calls

**Solutions:**
```python
# Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Debug Mode

Enable debug logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG

# Start with debug
uvicorn web.app:app --reload --log-level debug
```

### Health Checks

```bash
# API health check
curl http://localhost:8000/health

# Component generation test
curl -X POST http://localhost:8000/generate \\
  -H "Content-Type: application/json" \\
  -d '{"product_idea":"test","target_users":["B2B"],"brand_traits":["modern"],"platforms":["web"]}'
```

This deployment guide covers all aspects of getting the Design System Generator running in production environments, from simple single-server setups to complex cloud deployments with monitoring and scaling.

