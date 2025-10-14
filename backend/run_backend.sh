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

# Load environment variables from .env file
if [ -f ".env" ]; then
    echo "✅ Loading variables from .env..."
    set -a
    source .env
    set +a
else
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env with default values..."
    
    # Create default .env for local development
    cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/allaboutme
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=dev-secret-key

# Storage
STORAGE_PATH=/tmp/allaboutme

# API Keys (ADD YOUR KEYS HERE!)
GROQ_API_KEY=
HEYGEN_API_KEY=
TELEGRAM_BOT_TOKEN=
TG_MOD_CHAT_ID=
TG_PUBLIC_CHAT_ID=
EOF
    
    echo "✅ Created .env file. Please add your API keys!"
    echo "Edit: backend/.env"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Validate required variables
echo ""
echo "📋 Environment Check:"
echo "  DATABASE_URL: ${DATABASE_URL:0:50}..."
echo "  REDIS_URL: ${REDIS_URL:0:50}..."
echo "  STORAGE_PATH: $STORAGE_PATH"

if [ -n "$GROQ_API_KEY" ]; then
    echo "  ✅ GROQ_API_KEY: ${GROQ_API_KEY:0:20}..."
else
    echo "  ⚠️  GROQ_API_KEY: NOT SET (scripts won't generate)"
fi

echo ""

# Run migrations if needed
echo "📦 Checking migrations..."
alembic upgrade head 2>/dev/null || echo "Migrations already up to date"

# Start server
echo ""
echo "🌐 Starting FastAPI server..."
echo "  Local: http://localhost:8000"
echo "  Docs:  http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
