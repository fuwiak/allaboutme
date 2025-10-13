# 🚨 Quick Fix - Backend Not Running

## Problem
Frontend shows: `http proxy error: /api/auth/login ECONNREFUSED`

**Reason**: Backend (FastAPI) is not running!

---

## Solution: Start Backend

### Step 1: Start Database (if not running)

```bash
# In terminal 1
docker-compose up -d

# Verify
docker ps
# Should show: allaboutme-db and allaboutme-redis
```

### Step 2: Setup Backend (FIRST TIME ONLY)

```bash
# In terminal 2
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Minimal .env (REQUIRED):**
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/allaboutme
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=dev-secret-change-this
GROQ_API_KEY=your-groq-api-key-here
TELEGRAM_BOT_TOKEN=your-telegram-token
TG_MOD_CHAT_ID=your-chat-id
```

**Run migrations:**
```bash
alembic upgrade head
```

### Step 3: Start Backend Server

```bash
# In terminal 2 (with backend/.venv activated)
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ Created default user: admin / admin123
```

### Step 4: Start Celery Worker

```bash
# In terminal 3
cd backend
source .venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info
```

### Step 5: Refresh Frontend

Frontend is already running at http://localhost:5173

Now refresh the page and login!

---

## Default Login Credentials

```
Username: admin
Password: admin123
```

**⚠️ IMPORTANT**: Change this password after first login!

---

## Verify Backend is Working

```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return:
{"status":"ok","app":"AllAboutMe Video Generator"}

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Should return JWT token
```

---

## Quick Check: What's Running?

```bash
# Check ports
lsof -i :5173  # Frontend (Vite)
lsof -i :8000  # Backend (FastAPI)
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
```

All 4 should be active!

---

## Common Issues

### "ModuleNotFoundError" when starting backend
```bash
# Make sure you're in venv
source .venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### "Database connection failed"
```bash
# Start Docker
docker-compose up -d

# Check it's running
docker ps
```

### "Alembic command not found"
```bash
# Install in venv
pip install alembic
```

---

## Status Check

After starting everything, you should have:

- ✅ Terminal 1: Docker (PostgreSQL + Redis)
- ✅ Terminal 2: Backend (FastAPI on :8000)
- ✅ Terminal 3: Celery worker
- ✅ Terminal 4: Frontend (Vite on :5173)

---

## Next: Login and Test!

1. Go to: http://localhost:5173
2. Login: `admin` / `admin123`
3. You should see Dashboard!

---

**Still having issues?** Check `TEST_LOCALLY.md` for detailed troubleshooting.

