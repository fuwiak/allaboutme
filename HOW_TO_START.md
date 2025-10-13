# 🚀 How to Start - Simple Guide

## Your API Key is Already Added! ✅

You added GROQ_API_KEY to `backend/run_celery.sh` - great!

---

## Current Status:

- ✅ Docker: Running (PostgreSQL + Redis)
- ✅ Backend: Running on http://localhost:8000
- ✅ Frontend: Running on http://localhost:5173
- ⏳ Celery: Needs restart with your GROQ_API_KEY

---

## 🔄 Restart Celery (with your GROQ key):

**In a NEW terminal:**

```bash
cd /Users/user/allaboutme/backend
./run_celery.sh
```

You should see:
```
🔄 Starting Celery Worker...
Environment:
  DATABASE_URL: postgresql://postgres:postgres@localhost:5433...
  REDIS_URL: redis://localhost:6379/0
  STORAGE_PATH: /tmp/allaboutme
  GROQ_API_KEY: ZmRhOTM5ZjdmOGM1NDQ...
  
celery@your-machine ready.
```

---

## ✅ Test Now:

1. **Go to**: http://localhost:5173
2. **Login**: `admin` / `admin123`
3. **Dashboard** → Click "Generate Scripts"
4. **Wait** for progress modal
5. **Scripts appear** in Drafts! 🎉

---

## 📋 All 4 Terminals:

### Terminal 1: Docker
```bash
docker-compose up -d
# (already running ✅)
```

### Terminal 2: Backend
```bash
cd backend
./run_backend.sh
# (already running ✅)
```

### Terminal 3: Celery ← START THIS NOW!
```bash
cd backend
./run_celery.sh
```

### Terminal 4: Frontend
```bash
cd frontend
npm run dev
# (already running ✅)
```

---

## 🎬 Full Video Flow:

1. **Generate Scripts** → Dashboard → "Generate Scripts" button
2. **Edit Script** → Drafts → Click script → Edit
3. **Generate Post Text** → Click "✨ Generate" button
4. **Create Video** → Click "🎬 Create Video" button
5. **Publish** → Publish page → Select platforms → Publish

---

## 🔑 Login:

```
URL: http://localhost:5173
Username: admin
Password: admin123
```

---

## ⚡ Quick Commands:

```bash
# Check what's running:
docker ps                    # Database & Redis
lsof -i :8000               # Backend (FastAPI)
lsof -i :5173               # Frontend (Vite)
ps aux | grep celery        # Celery worker

# Stop everything:
docker-compose down
pkill -f uvicorn
pkill -f celery
# Ctrl+C in frontend terminal
```

---

## 🎉 Ready to Go!

Just start Celery and you're good! Everything else is already running.

**Start Celery now:**
```bash
cd backend
./run_celery.sh
```

Then test script generation! 🚀

