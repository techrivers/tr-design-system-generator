#!/bin/bash
# Quick deployment script for Google Cloud Run

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Deploying Design System Generator to Google Cloud Run${NC}\n"

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  No project set. Please run:${NC}"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}✓ Project: ${PROJECT_ID}${NC}"

# Check if APIs are enabled
echo -e "\n${BLUE}Checking required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com --quiet 2>/dev/null || true

# Set default values
REGION=${REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-design-system-agent}
MEMORY=${MEMORY:-1Gi}
TIMEOUT=${TIMEOUT:-300}
MAX_INSTANCES=${MAX_INSTANCES:-10}

echo -e "\n${BLUE}Deployment Configuration:${NC}"
echo "  Service: $SERVICE_NAME"
echo "  Region: $REGION"
echo "  Memory: $MEMORY"
echo "  Timeout: ${TIMEOUT}s"
echo "  Max Instances: $MAX_INSTANCES"

# Build and deploy
echo -e "\n${BLUE}Building and deploying...${NC}\n"

gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory $MEMORY \
  --timeout $TIMEOUT \
  --max-instances $MAX_INSTANCES

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --format 'value(status.url)')

echo -e "\n${GREEN}✅ Deployment complete!${NC}\n"
echo -e "${GREEN}Service URL: ${SERVICE_URL}${NC}\n"
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Test your service: curl $SERVICE_URL/health"
echo "  2. Set environment variables:"
echo "     gcloud run services update $SERVICE_NAME --update-env-vars KEY=value --region $REGION"
echo "  3. View logs:"
echo "     gcloud run services logs read $SERVICE_NAME --region $REGION --follow"
