# Deployment Guide - Railway

## Pre-Deployment Checklist

### 1. Test Backend Locally

```bash
cd backend

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup local database
# Install PostgreSQL if not installed
export DATABASE_URL="postgresql://localhost/allaboutme"
export REDIS_URL="redis://localhost:6379/0"

# Run migrations
alembic upgrade head

# Migrate config.yaml to database
python migrate_config.py

# Start backend
uvicorn app.main:app --reload --port 8000

# In another terminal: Start Celery
celery -A app.tasks.celery_app worker --loglevel=info
```

Test endpoints: http://localhost:8000/docs

### 2. Test Frontend Locally

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit if needed (default: VITE_API_URL=http://localhost:8000)

# Start dev server
npm run dev
```

Visit: http://localhost:5173
Login: `admin` / `admin123`

## Railway Deployment

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Create new project
3. Add services:
   - **PostgreSQL** (native service)
   - **Redis** (native service)

### Step 2: Connect GitHub Repository

1. In Railway project, click "New Service"
2. Select "GitHub Repo"
3. Connect your repository
4. Railway will auto-detect Dockerfile

### Step 3: Add Volume for Storage

1. In your service settings
2. Go to "Volumes"
3. Add volume:
   - Mount Path: `/storage`
   - Size: 10GB (or more based on needs)

### Step 4: Configure Environment Variables

In Railway service settings → Variables, add:

```bash
# Database (auto from PostgreSQL service)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (auto from Redis service)
REDIS_URL=${{Redis.REDIS_URL}}

# JWT Secret (generate random string)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-this

# Groq API
GROQ_API_KEY=your-groq-api-key

# HeyGen (optional, for paid video generation)
HEYGEN_API_KEY=your-heygen-api-key
HEYGEN_TEMPLATE_ID=your-template-id
HEYGEN_AVATAR_ID=your-avatar-id

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TG_MOD_CHAT_ID=your-moderation-chat-id
TG_PUBLIC_CHAT_ID=your-public-channel-id

# Social Media (optional)
FB_TOKEN=your-facebook-token
FB_PAGE_ID=your-page-id
IG_USER_ID=your-instagram-user-id
YOUTUBE_TOKEN=your-youtube-token
TIKTOK_TOKEN=your-tiktok-token

# App
DEBUG=False
STORAGE_PATH=/storage
PORT=8000
```

### Step 5: Deploy

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Complete migration to Svelte + FastAPI"
   git push origin main
   ```

2. Railway will automatically:
   - Build Docker image (multi-stage: Node + Python)
   - Run database migrations
   - Start Celery worker
   - Start FastAPI server

3. Check deployment logs in Railway dashboard

### Step 6: Access Your App

Railway will provide you with a URL like:
`https://your-app-name.railway.app`

Default login: `admin` / `admin123`

**Important**: Change default password immediately after first login!

## Post-Deployment

### Migrate Existing Data

If you have data in `config.yaml`:

```bash
# SSH into Railway or run locally then push DB
python backend/migrate_config.py
```

### Monitor Logs

In Railway dashboard:
- Check service logs
- Monitor PostgreSQL performance
- Check Celery worker status
- Monitor storage usage

### Scaling

Railway automatically scales based on:
- CPU usage
- Memory usage
- Request load

For heavy video generation workload, consider:
- Increasing RAM allocation
- Adding more Celery workers
- Upgrading volume storage

## Troubleshooting

### Database Connection Issues

```bash
# Check DATABASE_URL is correctly set
# Ensure PostgreSQL service is running
# Verify migrations ran successfully
```

### Redis Connection Issues

```bash
# Check REDIS_URL is correctly set
# Ensure Redis service is running
# Test connection in Python
```

### Celery Not Processing Tasks

```bash
# Check Celery worker logs
# Verify REDIS_URL connection
# Ensure tasks are properly imported
```

### Video Generation Fails

```bash
# Check GROQ_API_KEY is valid
# For HeyGen: verify HEYGEN_API_KEY and HEYGEN_TEMPLATE_ID
# Check storage volume has space
# Review error logs
```

### Frontend 404 Errors

```bash
# Ensure frontend build completed successfully
# Check static files are in backend/app/static
# Verify fallback routing in main.py
```

## Maintenance

### Update Dependencies

```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

### Database Backups

Railway PostgreSQL includes automatic backups.
Additional manual backup:

```bash
# Export database
pg_dump $DATABASE_URL > backup.sql

# Import database
psql $DATABASE_URL < backup.sql
```

### Clean Old Videos

```bash
# Will run automatically via cleanup_old_files() in storage
# Or manually:
python -c "from backend.app.storage import cleanup_old_files; cleanup_old_files(30)"
```

## Security Checklist

- [ ] Change default admin password
- [ ] Use strong JWT_SECRET_KEY
- [ ] Enable HTTPS (Railway provides this automatically)
- [ ] Restrict CORS origins in production
- [ ] Use environment variables for all secrets
- [ ] Enable Railway's built-in DDoS protection
- [ ] Regularly rotate API keys
- [ ] Monitor access logs

## Cost Optimization

Railway pricing based on:
- Compute time
- Database storage
- Redis memory
- Volume storage
- Bandwidth

Tips to reduce costs:
1. Use open-source video generator (free, no HeyGen costs)
2. Set up video cleanup policy (delete old files)
3. Optimize Celery worker concurrency
4. Use Railway's sleep feature for non-production envs

## Support

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- SvelteKit Docs: https://kit.svelte.dev
- Celery Docs: https://docs.celeryq.dev

---

**Migration Complete!** 🎉

You now have a modern, scalable video generation platform running on Railway with:
- ✅ FastAPI backend
- ✅ SvelteKit frontend
- ✅ PostgreSQL database
- ✅ Redis + Celery for async tasks
- ✅ WebSocket real-time updates
- ✅ Multi-platform publishing

