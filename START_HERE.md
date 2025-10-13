# 🚀 START HERE - Quick Testing Guide

## Step 1: Start Database & Redis

```bash
# Start PostgreSQL + Redis using Docker
docker-compose up -d

# Verify they're running
docker ps
```

## Step 2: Start Backend (3 commands)

```bash
# Terminal 1: Backend API
cd backend
source .venv/bin/activate || python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit this with your API keys!
export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/allaboutme"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET_KEY="test-secret-key"
export STORAGE_PATH="/tmp/allaboutme"
export GROQ_API_KEY="your-groq-key-here"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

```bash
# Terminal 2: Celery Worker
cd backend
source .venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

## Step 3: Start Frontend

```bash
# Terminal 3: Frontend
cd frontend
npm install
npm run dev
```

## Step 4: Test!

1. **Backend API**: http://localhost:8000/docs
2. **Frontend App**: http://localhost:5173
3. **Login**: `admin` / `admin123`

## Quick Test Script

```bash
# Test backend automatically
./test_backend.sh
```

## Stop Everything

```bash
# Stop Docker
docker-compose down

# Stop backend & frontend (Ctrl+C in all terminals)
```

---

## Environment Variables You NEED:

Edit `backend/.env`:

```bash
# Minimal setup
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/allaboutme
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-this-secret
GROQ_API_KEY=your-groq-api-key        # GET THIS FROM groq.com
TELEGRAM_BOT_TOKEN=your-telegram-token # GET THIS FROM @BotFather
TG_MOD_CHAT_ID=your-chat-id           # Your Telegram chat ID
```

## Full Documentation

- **TEST_LOCALLY.md** - Complete testing guide
- **QUICK_START.md** - 5-minute setup
- **DEPLOYMENT_GUIDE.md** - Deploy to Railway
- **README.md** - Full documentation

---

**Questions?** Check TEST_LOCALLY.md for troubleshooting!

