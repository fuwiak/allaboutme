#!/bin/bash
set -e

echo "🚀 Starting AllAboutMe..."

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is not set!"
    echo "Please add PostgreSQL database in Railway:"
    echo "  1. Click '+ New'"
    echo "  2. Select 'Database' → 'PostgreSQL'"
    echo "  3. Railway will auto-set DATABASE_URL"
    exit 1
fi

echo "✅ DATABASE_URL is set"
echo "   ${DATABASE_URL:0:50}..."

# Run database migrations
echo "📦 Running database migrations..."
cd backend
alembic upgrade head || {
    echo "❌ Migration failed! Check DATABASE_URL is correct."
    echo "Current DATABASE_URL: ${DATABASE_URL:0:80}..."
    exit 1
}

# Start Celery worker with Beat in background
echo "🔄 Starting Celery worker with Beat scheduler..."
celery -A app.tasks.celery_app worker --beat --loglevel=info --concurrency=2 &

# Start FastAPI with uvicorn
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
