"""FastAPI main application"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import redis
import json
import logging
from pathlib import Path

from .config import settings
from .routers import auth, scripts, videos
from .database import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Video generation API with Svelte frontend",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(scripts.router)
app.include_router(videos.router)

# Upload router
from .routers import upload
app.include_router(upload.router)

# Task management router
from .routers import tasks as tasks_router
app.include_router(tasks_router.router)

# Automation router
from .routers import automation
app.include_router(automation.router)

# Redis client for WebSocket
redis_client = redis.from_url(settings.REDIS_URL)


@app.get("/health")
def health_check():
    """Health check endpoint for Railway"""
    return {"status": "ok", "app": settings.APP_NAME}


@app.websocket("/ws/progress/{task_id}")
async def websocket_progress(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time progress updates"""
    await websocket.accept()
    
    try:
        # Subscribe to Redis pub/sub for this task
        pubsub = redis_client.pubsub()
        pubsub.subscribe(f"progress:{task_id}")
        
        logger.info(f"WebSocket connected for task: {task_id}")
        
        # Listen for messages
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data']
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                
                await websocket.send_text(data)
                
                # Check if task is completed
                try:
                    msg_data = json.loads(data)
                    if msg_data.get('status') in ['completed', 'failed']:
                        break
                except:
                    pass
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for task: {task_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        try:
            pubsub.unsubscribe(f"progress:{task_id}")
            pubsub.close()
        except:
            pass


# Generator endpoints
from .routers import generator as generator_router
app.include_router(generator_router.router)

# Publisher endpoints  
from .routers import publisher as publisher_router
app.include_router(publisher_router.router)

# Settings endpoints
from .routers import settings as settings_router
app.include_router(settings_router.router)


# Serve static files (SvelteKit build)
static_path = Path(__file__).parent / "static"
if static_path.exists():
    # Mount assets directory only if it exists
    assets_path = static_path / "assets"
    if assets_path.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
        logger.info(f"✅ Mounted static assets from {assets_path}")
    else:
        logger.warning(f"⚠️  Assets directory not found: {assets_path}")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve SvelteKit SPA"""
        file_path = static_path / full_path
        
        # If file exists, serve it
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (SPA routing)
        index_path = static_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        # Frontend not built - return helpful message
        return {
            "message": "AllAboutMe API is running!",
            "frontend": "Not built yet - use /docs for API",
            "docs": "/docs",
            "health": "/health"
        }
else:
    # No static directory at all - API only mode
    @app.get("/")
    async def root():
        """API root when no frontend"""
        return {
            "message": "AllAboutMe API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health",
            "note": "Frontend not available - API only"
        }


@app.on_event("startup")
async def startup_event():
    """Initialize app on startup"""
    logger.info(f"Starting {settings.APP_NAME}")
    
    # Initialize storage
    from .storage import init_storage
    init_storage()
    
    # Create default user and settings if none exist
    from .database import SessionLocal
    from . import models
    
    db = SessionLocal()
    try:
        # Create default user
        user_count = db.query(models.User).count()
        user = None
        if user_count == 0:
            # Use pre-hashed password for startup (bcrypt issue workaround)
            # Hash for "admin123" generated separately
            default_user = models.User(
                username="admin",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaOdDTC"  # admin123
            )
            db.add(default_user)
            db.commit()
            db.refresh(default_user)
            user = default_user
            logger.info("✅ Created default user: admin / admin123")
        else:
            user = db.query(models.User).first()
        
        # Create default settings if none exist
        settings_count = db.query(models.Setting).count()
        if settings_count == 0 and user:
            default_settings = {
                "daily_videos": "10",
                "themes": "астрология, натальные карты, положение планет в знаках зодиака, нумерология, матрица судьбы, Human Design, инсайты для жизни, советы по саморазвитию",
                "system_prompt": "Ты эксперт в эзотерических науках: астрологии, нумерологии, матрице судьбы и Human Design. Создавай короткие, мистические и поэтичные посты с глубоким смыслом.",
                "video_length": "30",
                "language": "ru"
            }
            
            for key, value in default_settings.items():
                setting = models.Setting(
                    user_id=user.id,
                    key=key,
                    value=value
                )
                db.add(setting)
            
            db.commit()
            logger.info("✅ Created default settings with esoteric themes")
    except Exception as e:
        logger.error(f"Error creating defaults: {e}")
    finally:
        db.close()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")

