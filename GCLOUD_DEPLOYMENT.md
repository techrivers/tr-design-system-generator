# Deploying to Google Cloud Run

This guide will help you deploy the Design System Generator to Google Cloud Run.

## Prerequisites

1. **Google Cloud Account** - Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK (gcloud CLI)** - Install from [cloud.google.com/sdk](https://cloud.google.com/sdk)
3. **Billing enabled** - Cloud Run requires a billing account (but has generous free tier)

## Initial Setup

### 1. Install Google Cloud SDK

**macOS:**
```bash
# Using Homebrew
brew install --cask google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

**Linux:**
```bash
# Download and install
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download installer from: https://cloud.google.com/sdk/docs/install

### 2. Authenticate and Initialize

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create design-system-agent --name="Design System Agent"

# Set the project as default
gcloud config set project design-system-agent

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Set Billing Account

```bash
# List billing accounts
gcloud billing accounts list

# Link billing account to project
gcloud billing projects link design-system-agent --billing-account=BILLING_ACCOUNT_ID
```

## Deployment Methods

### Method 1: Quick Deploy (Recommended)

This is the fastest way to deploy:

```bash
# Build and deploy in one command
gcloud run deploy design-system-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --max-instances 10
```

**What this does:**
- Builds your Docker image automatically
- Deploys to Cloud Run
- Makes it publicly accessible
- Sets memory to 1GB
- Sets timeout to 5 minutes
- Limits to 10 concurrent instances

### Method 2: Build and Deploy Separately

For more control:

```bash
# Step 1: Build the container image
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/design-system-agent

# Step 2: Deploy to Cloud Run
gcloud run deploy design-system-agent \
  --image gcr.io/$(gcloud config get-value project)/design-system-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --max-instances 10
```

### Method 3: Using Cloud Build (CI/CD)

For automated deployments from Git:

```bash
# Submit build using cloudbuild.yaml
gcloud builds submit --config cloudbuild.yaml

# Deploy the built image
gcloud run deploy design-system-agent \
  --image gcr.io/$(gcloud config get-value project)/design-system-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300
```

## Environment Variables

Set environment variables for your API keys:

```bash
gcloud run services update design-system-agent \
  --update-env-vars OPENAI_API_KEY=your-key-here,ANTHROPIC_API_KEY=your-key-here \
  --region us-central1
```

Or set them during deployment:

```bash
gcloud run deploy design-system-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key-here,ANTHROPIC_API_KEY=your-key-here \
  --memory 1Gi \
  --timeout 300
```

## Configuration Options

### Memory and CPU

```bash
# Adjust memory (128Mi to 8Gi)
--memory 2Gi

# Adjust CPU (1, 2, 4, 6, or 8)
--cpu 2
```

### Timeout

```bash
# Maximum timeout is 60 minutes (3600 seconds)
--timeout 600  # 10 minutes
```

### Scaling

```bash
# Min instances (always running, costs more)
--min-instances 1

# Max instances (auto-scaling limit)
--max-instances 100

# Concurrency (requests per instance)
--concurrency 80
```

### Example Full Deployment

```bash
gcloud run deploy design-system-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 600 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80 \
  --set-env-vars OPENAI_API_KEY=your-key-here
```

## After Deployment

### Get Your Service URL

```bash
# Get the service URL
gcloud run services describe design-system-agent \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

The URL will look like: `https://design-system-agent-xxxxx-uc.a.run.app`

### View Logs

```bash
# Stream logs
gcloud run services logs read design-system-agent \
  --platform managed \
  --region us-central1 \
  --follow

# Or view in console
# https://console.cloud.google.com/run
```

### Update Service

```bash
# Redeploy with new code
gcloud run deploy design-system-agent \
  --source . \
  --platform managed \
  --region us-central1
```

## Cost Estimation

### Free Tier (Always Free)
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds
- 1 GB egress per day

### Beyond Free Tier
- **Requests**: $0.40 per million
- **Memory**: $0.0000025 per GB-second
- **CPU**: $0.0000100 per vCPU-second
- **Egress**: $0.12 per GB (first 10GB free)

**Typical monthly cost**: $0-10 for moderate usage

## Troubleshooting

### Issue: Build fails
```bash
# Check build logs
gcloud builds list --limit=5
gcloud builds log BUILD_ID
```

### Issue: Service won't start
```bash
# Check service logs
gcloud run services logs read design-system-agent --region us-central1
```

### Issue: Timeout errors
- Increase `--timeout` value (max 3600 seconds)
- Optimize your agent processing
- Consider breaking into smaller functions

### Issue: Out of memory
- Increase `--memory` value
- Optimize code to use less memory
- Check for memory leaks

### Issue: Cold start too slow
- Set `--min-instances 1` to keep one instance warm
- Note: This increases costs

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - id: 'auth'
        uses: 'google-github-actions/auth@v1'
        with:
          credentials_json: '${{ secrets.GCP_SA_KEY }}'
      
      - name: 'Set up Cloud SDK'
        uses: 'google-github-actions/setup-gcloud@v1'
      
      - name: 'Deploy to Cloud Run'
        run: |
          gcloud run deploy design-system-agent \
            --source . \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

## Security Best Practices

1. **Use Secret Manager** for sensitive keys:
```bash
# Create secret
echo -n "your-api-key" | gcloud secrets create openai-api-key --data-file=-

# Use in deployment
gcloud run deploy design-system-agent \
  --update-secrets OPENAI_API_KEY=openai-api-key:latest \
  --region us-central1
```

2. **Enable authentication** (if needed):
```bash
# Remove --allow-unauthenticated to require auth
gcloud run deploy design-system-agent \
  --no-allow-unauthenticated
```

3. **Set up custom domain**:
```bash
gcloud run domain-mappings create \
  --service design-system-agent \
  --domain yourdomain.com \
  --region us-central1
```

## Monitoring

### View Metrics
- Go to [Cloud Run Console](https://console.cloud.google.com/run)
- Select your service
- View metrics, logs, and revisions

### Set Up Alerts
```bash
# Create alert policy in Cloud Console
# https://console.cloud.google.com/monitoring/alerting
```

## Next Steps

1. ✅ Deploy using Method 1 (Quick Deploy)
2. ✅ Set environment variables
3. ✅ Test your deployed service
4. ✅ Set up custom domain (optional)
5. ✅ Configure CI/CD (optional)
6. ✅ Set up monitoring and alerts

## Useful Commands

```bash
# List all services
gcloud run services list

# Describe service
gcloud run services describe design-system-agent --region us-central1

# Delete service
gcloud run services delete design-system-agent --region us-central1

# List revisions
gcloud run revisions list --service design-system-agent --region us-central1

# Rollback to previous revision
gcloud run services update-traffic design-system-agent \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

## Support

- **Documentation**: https://cloud.google.com/run/docs
- **Pricing Calculator**: https://cloud.google.com/products/calculator
- **Support**: https://cloud.google.com/support
