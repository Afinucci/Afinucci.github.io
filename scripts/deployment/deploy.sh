#!/bin/bash

# WWS Inventory Platform - Deployment Script
# This script deploys the application to production

set -e

echo "🚀 WWS Inventory Platform - Deployment"
echo "======================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check environment
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${RED}❌ ENVIRONMENT variable not set${NC}"
    echo "Usage: ENVIRONMENT=production ./deploy.sh"
    exit 1
fi

echo "Environment: $ENVIRONMENT"
echo ""

# Confirmation for production
if [ "$ENVIRONMENT" = "production" ]; then
    echo -e "${YELLOW}⚠️  WARNING: Deploying to PRODUCTION${NC}"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Deployment cancelled"
        exit 0
    fi
fi

echo ""
echo "1️⃣  Running tests..."
make test || {
    echo -e "${RED}❌ Tests failed. Deployment aborted.${NC}"
    exit 1
}

echo ""
echo "2️⃣  Building Docker images..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

echo ""
echo "3️⃣  Pushing images to registry..."
# Add your registry push commands here
# docker push your-registry/wws-backend:latest
# docker push your-registry/wws-frontend:latest

echo ""
echo "4️⃣  Running database migrations..."
# Add migration commands for production
# kubectl exec -it deployment/backend -- alembic upgrade head

echo ""
echo "5️⃣  Deploying to Kubernetes..."
# kubectl apply -f infrastructure/kubernetes/

echo ""
echo "6️⃣  Waiting for deployment to complete..."
# kubectl rollout status deployment/backend
# kubectl rollout status deployment/frontend

echo ""
echo "7️⃣  Running health checks..."
# Add health check commands

echo ""
echo "======================================="
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo "Next steps:"
echo "  - Monitor logs: kubectl logs -f deployment/backend"
echo "  - Check status: kubectl get pods"
echo "  - Rollback if needed: kubectl rollout undo deployment/backend"
echo ""
