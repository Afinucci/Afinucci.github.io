# Quick Start Guide

Get the WWS Inventory Platform up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- Git installed
- 8GB RAM minimum
- 10GB free disk space

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Afinucci/Afinucci.github.io.git
cd Afinucci.github.io
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

**Required Configuration:**
```env
# Database (default values work for local dev)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/wws_inventory

# Redis (default values work for local dev)
REDIS_URL=redis://redis:6379/0

# AI Services - ADD YOUR KEYS HERE
OPENAI_API_KEY=sk-your-actual-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here

# Security - CHANGE THIS
SECRET_KEY=your-random-secret-key-min-32-characters-long
```

### 3. Start the Platform

```bash
# Automated setup (recommended)
./scripts/setup/init.sh

# OR manual setup
make setup
make start
```

### 4. Verify Installation

```bash
# Check service status
docker-compose ps

# You should see all services as "Up":
# - wws_frontend
# - wws_backend
# - wws_postgres
# - wws_redis
```

### 5. Access the Application

Open your browser and visit:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

## First Steps

### 1. Explore the Dashboard

Visit http://localhost:3000 to see:
- Real-time inventory metrics
- AI insights and recommendations
- Recent activity feed

### 2. Try the AI Chat

In the right panel, try asking:
- "What items are low in stock?"
- "Show me today's orders"
- "What are my top selling products?"
- "Add 50 units to Product X"

### 3. Explore the API

Visit http://localhost:8000/docs to:
- View all available endpoints
- Test API calls interactively
- See request/response schemas

### 4. Sample Data

The database is pre-seeded with:
- 5 sample products
- 2 orders with items
- AI-generated insights
- Stock movement history
- Sample conversation

## Common Commands

```bash
# View logs
make logs                  # All services
make logs-backend         # Backend only
make logs-frontend        # Frontend only

# Stop services
make stop

# Restart services
make restart

# Clean up everything (removes data!)
make clean

# Run tests
make test

# Access database
make db-shell

# Backend shell
make shell-backend

# Run migrations
make migrate
```

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker --version
docker-compose --version

# Check ports are available
lsof -i :3000  # Frontend port
lsof -i :8000  # Backend port
lsof -i :5432  # PostgreSQL port
lsof -i :6379  # Redis port

# If ports are in use, kill processes or change ports in docker-compose.yml
```

### Database connection errors

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
sleep 10
make migrate
```

### Frontend shows errors

```bash
# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### AI features not working

1. Check API keys in `.env`
2. Ensure keys are valid (start with `sk-` for OpenAI, `sk-ant-` for Anthropic)
3. Check backend logs: `make logs-backend`

### Still having issues?

1. Check logs: `make logs`
2. Verify environment: `python scripts/setup/check-env.py`
3. Open an issue on GitHub with:
   - Error message
   - Output from `docker-compose ps`
   - Output from `make logs`

## Next Steps

### Development

1. **Backend Development**
   ```bash
   cd backend
   # Edit files in backend/app/
   # Changes auto-reload with uvicorn --reload
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   # Edit files in frontend/src/
   # Changes auto-reload with Next.js
   ```

3. **Run Tests**
   ```bash
   # Backend tests
   cd backend && pytest

   # Frontend tests
   cd frontend && npm test
   ```

### Customize

1. **Add Products**: Use the API or chat interface
2. **Configure Warehouses**: Edit product locations
3. **Set Reorder Points**: Adjust inventory thresholds
4. **Create Workflows**: Define automated actions

### Deploy

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment guide.

## Learning Resources

- **API Documentation**: http://localhost:8000/docs
- **Architecture**: See [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Contributing**: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Project Plan**: See [PROJECT_PLAN.md](../PROJECT_PLAN.md)

## Support

- **Documentation**: Check `/docs` folder
- **Issues**: https://github.com/Afinucci/Afinucci.github.io/issues
- **Discussions**: https://github.com/Afinucci/Afinucci.github.io/discussions

---

**Ready to build something amazing? Let's go! 🚀**
