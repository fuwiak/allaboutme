#!/bin/bash
set -e

echo "🚀 Starting AllAboutMe..."

# Run database migrations
echo "📦 Running database migrations..."
cd backend
alembic upgrade head

# Start Celery worker with Beat in background
echo "🔄 Starting Celery worker with Beat scheduler..."
celery -A app.tasks.celery_app worker --beat --loglevel=info --concurrency=2 &

# Start FastAPI with uvicorn
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
