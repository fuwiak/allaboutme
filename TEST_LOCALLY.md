# 🧪 Local Testing Guide

## Step-by-step guide to test AllAboutMe locally

---

## Step 1: Start Database & Redis

### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL + Redis
docker-compose up -d

# Verify they're running
docker ps

# You should see:
# - allaboutme-db (PostgreSQL on port 5432)
# - allaboutme-redis (Redis on port 6379)
```

### Option B: Native Installation

**PostgreSQL:**
```bash
# macOS
brew install postgresql@16
brew services start postgresql@16

# Create database
createdb allaboutme
```

**Redis:**
```bash
# macOS
brew install redis
brew services start redis
```

---

## Step 2: Setup Backend

### 2.1 Create Virtual Environment

```bash
cd backend

# Create venv
python -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 2.2 Install Dependencies

```bash
# Install all Python packages
pip install -r requirements.txt

# This will install:
# - FastAPI, Uvicorn
# - SQLAlchemy, Alembic, psycopg2
# - Celery, Redis
# - Groq, python-telegram-bot
# - moviepy, gtts, pillow
# - and more...
```

### 2.3 Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env  # or use your favorite editor
```

**Minimal .env configuration:**
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/allaboutme

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Secret (change this!)
JWT_SECRET_KEY=dev-secret-key-for-testing-only

# Groq API (REQUIRED for script generation)
GROQ_API_KEY=your-groq-api-key-here

# Telegram (REQUIRED for notifications)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TG_MOD_CHAT_ID=your-chat-id

# HeyGen (OPTIONAL - for paid video generation)
HEYGEN_API_KEY=your-heygen-key
HEYGEN_TEMPLATE_ID=your-template-id

# Other social media (OPTIONAL)
FB_TOKEN=
YOUTUBE_TOKEN=
TIKTOK_TOKEN=
```

### 2.4 Run Database Migrations

```bash
# Still in backend/ directory
alembic upgrade head

# You should see:
# INFO  [alembic.runtime.migration] Running upgrade  -> xxx, initial schema
```

### 2.5 Migrate Config (Optional)

If you have old `config.yaml` file:

```bash
cd backend
python migrate_config.py

# This imports your old settings into PostgreSQL
```

### 2.6 Start Backend Services

**Terminal 1: FastAPI Server**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

**Terminal 2: Celery Worker**
```bash
cd backend
source .venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info

# You should see:
# [tasks]
#   . app.tasks.video_tasks.generate_scripts_task
#   . app.tasks.video_tasks.generate_video_task
#   . app.tasks.publish_tasks.publish_video_task
# celery@hostname ready.
```

### 2.7 Test Backend

Open browser: http://localhost:8000/docs

You should see **FastAPI Swagger UI** with all endpoints.

**Test the API:**

1. **Health Check:**
   - GET `/health`
   - Click "Try it out" → "Execute"
   - Should return: `{"status": "ok"}`

2. **Login:**
   - POST `/api/auth/login`
   - Request body:
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```
   - Should return JWT token

3. **Get Scripts:**
   - GET `/api/scripts`
   - Add Authorization header: `Bearer <your-token>`
   - Should return empty list `[]` (initially)

---

## Step 3: Setup Frontend

### 3.1 Install Dependencies

```bash
cd frontend

# Install npm packages
npm install

# This installs:
# - SvelteKit
# - Tailwind CSS
# - TypeScript
# - Vite
```

### 3.2 Configure Environment (Optional)

```bash
# Copy example
cp .env.example .env

# Edit if needed (default is fine for local testing)
nano .env
```

Default `.env`:
```bash
VITE_API_URL=http://localhost:8000
```

### 3.3 Start Development Server

```bash
cd frontend
npm run dev

# You should see:
# VITE v5.x.x  ready in XXX ms
#
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose
```

### 3.4 Test Frontend

Open browser: http://localhost:5173

You should see the **login page** with:
- Beautiful gradient background
- Login form
- "AllAboutMe" title

**Test login:**
- Username: `admin`
- Password: `admin123`
- Click "Login"
- Should redirect to Dashboard

---

## Step 4: End-to-End Testing

### Test 1: Generate Scripts

1. Go to **Dashboard**
2. Click **"Generate Scripts"** button
3. Watch the progress modal appear
4. Wait for completion (~10-30 seconds)
5. Scripts should appear in **Drafts → Scripts tab**

**What happens behind the scenes:**
- Frontend calls `/api/generate/scripts`
- Backend creates Celery task
- Returns task_id
- Frontend opens WebSocket to `/ws/progress/{task_id}`
- Celery worker generates scripts using Groq API
- Progress updates sent via WebSocket
- Scripts saved to PostgreSQL

### Test 2: Generate Post Text

1. Go to **Drafts → Scripts tab**
2. Click on a script card
3. Click **"✨ Generate"** button next to "Текст для озвучки"
4. Wait ~5 seconds
5. Clean post text appears
6. Modal shows the generated text

**What happens:**
- Calls `/api/generate/post-text/{script_id}`
- Uses Groq API to create clean text from scenario
- Updates script in database
- Returns text to frontend

### Test 3: Create Video

1. In the same script card
2. Click **"🎬 Create Video"**
3. Progress modal opens
4. Watch real-time progress updates
5. Wait for completion (1-3 minutes for open-source, 2-5 for HeyGen)

**What happens:**
- Saves script changes
- Calls `/api/generate/video`
- Creates Celery task for video generation
- WebSocket connects for progress
- Generates voice (gTTS or HeyGen)
- Creates video (MoviePy or HeyGen)
- Sends Telegram notification
- Video appears in **Drafts → Videos tab**

### Test 4: Publish Video

1. Go to **Publish** page
2. Click on a completed video
3. Click **"📤 Publish"**
4. Select platforms (e.g., Telegram)
5. Click **"Publish to X platforms"**
6. Watch progress
7. Video published!

**What happens:**
- Calls `/api/publish/{video_id}`
- Creates publish task
- Publishes to selected platforms
- Creates publication records
- Updates status

### Test 5: Update Settings

1. Go to **Settings**
2. **Content Settings tab:**
   - Change "Daily Videos" to `3`
   - Edit themes: `astrology,tarot,numerology`
   - Modify system prompt
3. Click **"💾 Save Settings"**
4. Settings updated in database

---

## Troubleshooting

### Backend Issues

**Problem: Database connection error**
```bash
# Check PostgreSQL is running
docker ps | grep postgres
# OR
brew services list | grep postgres

# Test connection
psql postgresql://postgres:postgres@localhost:5432/allaboutme
```

**Problem: Redis connection error**
```bash
# Check Redis is running
docker ps | grep redis
# OR
brew services list | grep redis

# Test connection
redis-cli ping
# Should return: PONG
```

**Problem: Celery not processing tasks**
```bash
# Check Celery logs
# Look for errors in Terminal 2 where Celery is running

# Common issues:
# - Redis not running
# - Wrong REDIS_URL in .env
# - Tasks not imported properly
```

**Problem: Migrations fail**
```bash
# Reset database
alembic downgrade base
alembic upgrade head

# OR start fresh
dropdb allaboutme
createdb allaboutme
alembic upgrade head
```

### Frontend Issues

**Problem: npm install fails**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Problem: "Cannot connect to API"**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check VITE_API_URL in .env
cat .env
```

**Problem: Login doesn't work**
```bash
# Check backend logs for errors
# Verify JWT_SECRET_KEY is set
# Try registering new user via API docs
```

### Video Generation Issues

**Problem: Script generation fails**
```bash
# Check GROQ_API_KEY is valid
echo $GROQ_API_KEY

# Check Celery logs for error details
# Verify Groq API quota/limits
```

**Problem: Video generation fails**
```bash
# For open-source:
# - Check moviepy, gtts, pillow are installed
# - Verify /storage directory exists and is writable

# For HeyGen:
# - Verify HEYGEN_API_KEY and HEYGEN_TEMPLATE_ID
# - Check HeyGen account balance
# - Review API error in logs
```

---

## Development Workflow

### Hot Reload

Both backend and frontend support hot reload:

**Backend:**
- Edit any `.py` file in `backend/app/`
- Uvicorn auto-reloads
- API changes immediately available

**Frontend:**
- Edit any `.svelte` or `.ts` file
- Vite hot-reloads
- Changes appear instantly in browser

### Debugging

**Backend:**
```python
# Add print statements
print("DEBUG:", variable)

# Use logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Check logs in terminal
```

**Frontend:**
```typescript
// Use console.log
console.log("DEBUG:", variable);

// Check browser DevTools → Console
```

### Database Inspection

```bash
# Connect to database
psql postgresql://postgres:postgres@localhost:5432/allaboutme

# List tables
\dt

# View data
SELECT * FROM scripts;
SELECT * FROM videos;
SELECT * FROM settings;

# Exit
\q
```

---

## Stopping Services

```bash
# Stop Docker services
docker-compose down

# Stop backend (Ctrl+C in both terminals)
# Stop frontend (Ctrl+C)

# Deactivate Python venv
deactivate
```

---

## Performance Tips

### Speed up development:

1. **Use open-source video generator** (no HeyGen API delays)
2. **Reduce video duration** in settings (15s → 5s for testing)
3. **Keep Celery worker running** (don't restart for each test)
4. **Use browser DevTools** → Network tab to debug API calls

---

## Next Steps

Once local testing works:

1. ✅ Test all features (scripts, videos, publishing)
2. ✅ Verify WebSocket progress works
3. ✅ Check Telegram notifications arrive
4. ✅ Review logs for errors
5. ✅ Ready for Railway deployment!

See `DEPLOYMENT_GUIDE.md` for production deployment.

---

## Quick Commands Reference

```bash
# Start everything
docker-compose up -d                                    # Database + Redis
cd backend && source .venv/bin/activate && \
  uvicorn app.main:app --reload --port 8000 &          # Backend
cd backend && celery -A app.tasks.celery_app worker &  # Celery
cd frontend && npm run dev                              # Frontend

# Stop everything
docker-compose down
pkill -f uvicorn
pkill -f celery
# Ctrl+C in frontend terminal

# Reset database
docker-compose down -v
docker-compose up -d
cd backend && alembic upgrade head
```

---

**Happy testing!** 🧪✨

