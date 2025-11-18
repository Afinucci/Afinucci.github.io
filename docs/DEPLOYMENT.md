# Deployment Guide

This guide covers deploying the WWS Inventory Platform to production environments.

## Deployment Options

1. **Cloud Platforms (Recommended)**
   - Kubernetes (Azure AKS / AWS EKS / GKE)
   - Docker Compose on VPS
   - Platform-as-a-Service (Railway, Render, Fly.io)

2. **Self-Hosted**
   - On-premises servers
   - Private cloud

## Prerequisites

- Domain name configured
- SSL certificate (Let's Encrypt recommended)
- Cloud account (Azure/AWS/GCP)
- Container registry access
- Database backup strategy

## Production Environment Variables

Create a production `.env` file with real values:

```env
# Environment
ENVIRONMENT=production

# Database (use managed database service)
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db-host:5432/wws_inventory

# Redis (use managed Redis service)
REDIS_URL=redis://prod-redis-host:6379/0

# AI Services
OPENAI_API_KEY=sk-prod-your-actual-key
ANTHROPIC_API_KEY=sk-ant-prod-your-actual-key
PINECONE_API_KEY=your-prod-pinecone-key
PINECONE_ENVIRONMENT=your-pinecone-env

# Security (generate strong random keys!)
SECRET_KEY=use-openssl-rand-hex-64-to-generate
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## Kubernetes Deployment

### 1. Build and Push Images

```bash
# Build images
docker build -t your-registry/wws-backend:v1.0.0 ./backend
docker build -t your-registry/wws-frontend:v1.0.0 ./frontend

# Push to registry
docker push your-registry/wws-backend:v1.0.0
docker push your-registry/wws-frontend:v1.0.0
```

### 2. Create Kubernetes Resources

```yaml
# infrastructure/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wws-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wws-backend
  template:
    metadata:
      labels:
        app: wws-backend
    spec:
      containers:
      - name: backend
        image: your-registry/wws-backend:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: wws-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
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
---
apiVersion: v1
kind: Service
metadata:
  name: wws-backend-service
spec:
  selector:
    app: wws-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 3. Create Secrets

```bash
# Create secrets from env file
kubectl create secret generic wws-secrets \
  --from-env-file=.env.production

# Or create individual secrets
kubectl create secret generic wws-secrets \
  --from-literal=database-url="postgresql://..." \
  --from-literal=openai-api-key="sk-..." \
  --from-literal=secret-key="..."
```

### 4. Deploy

```bash
# Apply all configurations
kubectl apply -f infrastructure/kubernetes/

# Check deployment status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/wws-backend
```

### 5. Configure Ingress

```yaml
# infrastructure/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: wws-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    - yourdomain.com
    secretName: wws-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wws-backend-service
            port:
              number: 80
  - host: yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: wws-frontend-service
            port:
              number: 80
```

## Docker Compose Production

For simpler deployments on a single VPS:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    image: your-registry/wws-backend:latest
    restart: always
    environment:
      - ENVIRONMENT=production
    env_file:
      - .env.production
    depends_on:
      - postgres
      - redis
    networks:
      - wws-network

  frontend:
    image: your-registry/wws-frontend:latest
    restart: always
    env_file:
      - .env.production
    depends_on:
      - backend
    networks:
      - wws-network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - wws-network

  postgres:
    image: timescale/timescaledb:latest-pg15
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - wws-network

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - wws-network

volumes:
  postgres_data:
  redis_data:

networks:
  wws-network:
    driver: bridge
```

Deploy with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Database Migrations

**Before deploying:**

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Or in Kubernetes:
kubectl exec -it deployment/wws-backend -- alembic upgrade head
```

**For zero-downtime migrations:**
1. Deploy new code (backward compatible)
2. Run migrations
3. Deploy code that uses new schema

## Health Checks

Add health check endpoints:

```python
# backend/app/main.py
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": settings.VERSION
    }

@app.get("/ready")
async def readiness_check():
    # Check database connection
    # Check Redis connection
    # Check external services
    return {"status": "ready"}
```

## Monitoring

### Application Monitoring

**Sentry for Error Tracking:**

```python
# backend/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
    )
```

**Prometheus Metrics:**

```python
from prometheus_client import Counter, Histogram, generate_latest

request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Infrastructure Monitoring

**Grafana Dashboards:**
- CPU and Memory usage
- Request rate and latency
- Database connections
- Error rates
- AI token usage

## Backup Strategy

### Database Backups

```bash
# Daily automated backups
0 2 * * * pg_dump -U postgres wws_inventory | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz

# Retention: Keep last 30 days
find /backups -name "db_*.sql.gz" -mtime +30 -delete
```

### File Backups

```bash
# Backup volumes
docker run --rm \
  -v wws_postgres_data:/data \
  -v /backups:/backup \
  alpine tar czf /backup/postgres_$(date +\%Y\%m\%d).tar.gz /data
```

## Security Checklist

- [ ] Use HTTPS everywhere
- [ ] Enable CORS properly
- [ ] Set secure session cookies
- [ ] Use strong SECRET_KEY
- [ ] Enable rate limiting
- [ ] Set up WAF (Web Application Firewall)
- [ ] Regular security updates
- [ ] Database encryption at rest
- [ ] Secure API keys in secrets manager
- [ ] Enable audit logging
- [ ] Set up intrusion detection
- [ ] Regular penetration testing

## Scaling Strategies

### Horizontal Scaling

```bash
# Scale backend pods
kubectl scale deployment wws-backend --replicas=5

# Auto-scaling based on CPU
kubectl autoscale deployment wws-backend \
  --cpu-percent=70 \
  --min=3 \
  --max=10
```

### Database Scaling

- Read replicas for queries
- Connection pooling (PgBouncer)
- Query optimization
- Indexing strategy

### Caching Strategy

- Redis for session data
- CDN for static assets
- API response caching
- Database query caching

## CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run tests
        run: make test

      - name: Build and push images
        run: |
          docker build -t ${{ secrets.REGISTRY }}/wws-backend:${{ github.ref_name }} ./backend
          docker push ${{ secrets.REGISTRY }}/wws-backend:${{ github.ref_name }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/wws-backend \
            backend=${{ secrets.REGISTRY }}/wws-backend:${{ github.ref_name }}

      - name: Wait for rollout
        run: kubectl rollout status deployment/wws-backend

      - name: Run migrations
        run: kubectl exec deployment/wws-backend -- alembic upgrade head
```

## Rollback Plan

```bash
# Kubernetes rollback
kubectl rollout undo deployment/wws-backend

# To specific revision
kubectl rollout undo deployment/wws-backend --to-revision=2

# View rollout history
kubectl rollout history deployment/wws-backend
```

## Performance Optimization

1. **Enable caching**: Redis, CDN
2. **Database optimization**: Indexes, query optimization
3. **Code optimization**: Async operations, connection pooling
4. **Load balancing**: Distribute traffic
5. **CDN**: Static assets delivery
6. **Compression**: Enable gzip
7. **Image optimization**: WebP, lazy loading

## Cost Optimization

- Use spot instances for non-critical workloads
- Auto-scaling to match demand
- Optimize AI token usage
- Use managed services wisely
- Monitor and eliminate waste
- Consider reserved instances

## Support and Maintenance

### Regular Tasks

- **Daily**: Monitor logs and alerts
- **Weekly**: Review metrics and performance
- **Monthly**: Security updates, backups verification
- **Quarterly**: Capacity planning, cost review
- **Annually**: Disaster recovery drill

### Emergency Contacts

- DevOps: devops@yourcompany.com
- Security: security@yourcompany.com
- On-call: Use PagerDuty

---

**Need help with deployment? Open an issue on GitHub!**
