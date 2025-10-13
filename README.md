# AllAboutMe - Video Generation Platform

**Version 2.0** - Svelte + FastAPI Migration

## Architecture

- **Frontend**: SvelteKit with Tailwind CSS
- **Backend**: FastAPI with PostgreSQL, Redis, Celery
- **Deployment**: Railway (with volume storage)

## Current Status

### ✅ Completed (Backend)

1. **Project Structure**: Full backend structure created
2. **Database Models**: PostgreSQL models for users, scripts, videos, publications, settings
3. **Authentication**: JWT-based auth with login/register endpoints
4. **API Routers**:
   - `/api/auth` - Login, register, user info
   - `/api/scripts` - CRUD operations for scripts
   - `/api/videos` - CRUD operations for videos
   - `/api/generate` - Script/video generation endpoints
   - `/api/publish` - Social media publishing endpoints
   - `/api/settings` - Settings management
5. **Services**: Migrated from old codebase:
   - `generator.py` - Groq-based script generation
   - `renderer.py` - HeyGen video rendering
   - `opensource_video.py` - Open-source video generation
   - `publisher.py` - Multi-platform publishing
   - `telegram_bot.py` - Telegram notifications
6. **Celery Tasks**: Async tasks for video generation and publishing
7. **WebSocket**: Real-time progress updates via Redis pub/sub
8. **Storage**: Volume-based storage for videos/audio
9. **Deployment Files**: Dockerfile, railway.json, start.sh

### 🚧 In Progress (Frontend)

1. **Basic Structure**: Created frontend directory structure
2. **Configuration**: package.json, svelte.config.js, vite.config.ts, tailwind.config.js
3. **API Client**: TypeScript API client with full endpoint coverage
4. **Stores**: Svelte stores for auth, scripts, videos, settings

### ⏳ To Do

1. **Frontend Pages**:
   - Login page
   - Dashboard with stats
   - Drafts page (scripts & videos)
   - Publish page
   - Settings page
2. **Components**:
   - ScriptCard
   - VideoCard
   - ProgressModal
   - VideoPlayer
3. **WebSocket Client**: Connect to `/ws/progress/{task_id}`
4. **Data Migration Script**: Import config.yaml to database
5. **Cleanup**: Remove old Flet files

## Local Development

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Redis

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
cp .env.example .env
# Edit .env with your credentials

# Run migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload --port 8000

# Start Celery worker (in another terminal)
celery -A app.tasks.celery_app worker --loglevel=info
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Default credentials: `admin` / `admin123`

## Railway Deployment

### Services Required

1. **Main App** (this repo)
2. **PostgreSQL** (Railway native)
3. **Redis** (Railway native)

### Environment Variables

Set these in Railway:

```
DATABASE_URL=<auto from PostgreSQL>
REDIS_URL=<auto from Redis>
JWT_SECRET_KEY=<random string>
GROQ_API_KEY=<your key>
HEYGEN_API_KEY=<your key>
TELEGRAM_BOT_TOKEN=<your token>
TG_MOD_CHAT_ID=<your chat id>
# ... other API keys
```

### Volume

Mount volume at `/storage` for persistent video/audio files.

### Deploy

```bash
git add .
git commit -m "Migration to Svelte + FastAPI"
git push

# Railway will auto-deploy using Dockerfile
```

## API Documentation

After starting the backend, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
allaboutme/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # DB models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── tasks/               # Celery tasks
│   │   └── storage/             # File storage utils
│   ├── alembic/                 # DB migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── routes/              # SvelteKit pages
│   │   └── lib/                 # Components, API, stores
│   └── package.json
├── Dockerfile                   # Multi-stage build
├── railway.json                 # Railway config
└── start.sh                     # Startup script
```

## Migration from Flet

Old files (to be removed after full migration):
- `ui.py`, `bot.py`, `main.py` - Replaced by FastAPI + Svelte
- All `.md` docs - Replaced by this README
- `test_*.py` - No longer needed

Core logic preserved:
- `generator.py` → `backend/app/services/generator.py`
- `renderer.py` → `backend/app/services/renderer.py`
- `opensource_video.py` → `backend/app/services/opensource_video.py`
- `publisher.py` → `backend/app/services/publisher.py`

## License

Private project
