#!/bin/bash
set -e

echo "🚀 Starting AllAboutMe..."
echo ""

# Print all environment info for debugging
echo "📋 Environment Variables:"
echo "  DATABASE_URL: ${DATABASE_URL:0:80}..."
echo "  REDIS_URL: ${REDIS_URL:0:50}..."
echo "  STORAGE_PATH: ${STORAGE_PATH:-not set}"
echo "  PORT: ${PORT:-8000}"
echo "  GROQ_API_KEY: ${GROQ_API_KEY:0:20}${GROQ_API_KEY:+...}"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is not set!"
    echo "Please add PostgreSQL database in Railway:"
    echo "  1. Click '+ New'"
    echo "  2. Select 'Database' → 'PostgreSQL'"
    echo "  3. Railway will auto-set DATABASE_URL"
    exit 1
fi

# Check if REDIS_URL is set
if [ -z "$REDIS_URL" ]; then
    echo "⚠️  WARNING: REDIS_URL is not set!"
    echo "Celery may not work. Add Redis database in Railway."
fi

echo "✅ DATABASE_URL is set"
echo "✅ REDIS_URL is set"
echo ""

# Test database connection before migrations
echo "🔍 Testing database connection..."
cd backend
python -c "
from app.database import engine
try:
    with engine.connect() as conn:
        print('✅ Database connection successful!')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    import sys
    sys.exit(1)
" || {
    echo "❌ Cannot connect to database!"
    echo "Check if PostgreSQL service is running in Railway."
    exit 1
}
echo ""

# Run database migrations
echo "📦 Running database migrations..."
alembic upgrade head || {
    echo "❌ Migration failed! Check DATABASE_URL is correct."
    echo "Current DATABASE_URL: ${DATABASE_URL:0:80}..."
    exit 1
}
echo "✅ Migrations complete"
echo ""

# Start Celery worker with Beat in background
echo "🔄 Starting Celery worker with Beat scheduler..."
celery -A app.tasks.celery_app worker --beat --loglevel=info --concurrency=2 &

# Start FastAPI with uvicorn
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
