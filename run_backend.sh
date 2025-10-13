#!/bin/bash

echo "🚀 Starting AllAboutMe Backend..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if in backend directory
if [ ! -f "app/main.py" ]; then
    echo -e "${RED}Error: Must run from backend/ directory${NC}"
    echo "Usage: cd backend && ../run_backend.sh"
    exit 1
fi

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Check if dependencies installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please copy .env.example to .env and configure it"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Export environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/allaboutme"
export REDIS_URL="redis://localhost:6379/0"

# Load .env if exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Check database connection
echo -e "${YELLOW}Checking database...${NC}"
if ! psql "$DATABASE_URL" -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${RED}Cannot connect to database${NC}"
    echo "Make sure Docker is running: docker-compose up -d"
    exit 1
fi

# Run migrations
echo -e "${YELLOW}Running migrations...${NC}"
alembic upgrade head

# Start server
echo -e "${GREEN}Starting FastAPI server on http://localhost:8000${NC}"
echo ""
echo "API Docs: http://localhost:8000/docs"
echo "Login: admin / admin123"
echo ""
uvicorn app.main:app --reload --port 8000

