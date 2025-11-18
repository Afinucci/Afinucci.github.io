#!/bin/bash

# WWS Inventory Platform - Initialization Script
# This script sets up the development environment

set -e

echo "🚀 WWS Inventory Platform - Development Setup"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env file with your configuration (API keys, etc.)${NC}"
    echo ""
    read -p "Press enter to continue after editing .env file..."
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo ""
echo "📦 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d postgres redis

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 10

echo ""
echo "🗄️ Running database migrations..."
docker-compose run --rm backend alembic upgrade head

echo ""
echo "🌱 Seeding database with sample data..."
docker-compose run --rm backend python app/db/seed.py

echo ""
echo "🚀 Starting all services..."
docker-compose up -d

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo "Services are now running:"
echo "  📱 Frontend:  http://localhost:3000"
echo "  🔌 Backend:   http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "  make logs          - View logs"
echo "  make stop          - Stop all services"
echo "  make restart       - Restart all services"
echo "  make clean         - Clean up containers and volumes"
echo ""
echo "Happy coding! 🎉"
