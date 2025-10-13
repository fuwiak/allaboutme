#!/bin/bash

echo "🚀 Starting AllAboutMe Backend..."

# Move to backend directory
cd "$(dirname "$0")"

# Activate venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/allaboutme"
export REDIS_URL="redis://localhost:6379/0"
export STORAGE_PATH="/tmp/allaboutme"
export JWT_SECRET_KEY="dev-secret"

# Optional: Load from .env if exists
if [ -f ".env" ]; then
    echo "Loading .env file..."
    set -a
    source .env
    set +a
fi

# Run migrations if needed
echo "Checking migrations..."
alembic upgrade head 2>/dev/null || echo "Migrations already up to date"

# Start server
echo "Starting FastAPI on http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

