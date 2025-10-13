"""Debug script to see full startup errors"""
import os
import sys

# Set environment
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5433/allaboutme"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["JWT_SECRET_KEY"] = "dev-secret-key"
os.environ["STORAGE_PATH"] = "/tmp/allaboutme"  # Use temp dir for local development

print("🔍 Loading app...")

try:
    from app.main import app
    print("✅ App imported successfully!")
    print(f"✅ Routes: {len(app.routes)}")
    
    # Try to trigger startup event manually
    import asyncio
    from app.main import startup_event
    
    print("🔍 Running startup event...")
    asyncio.run(startup_event())
    print("✅ Startup event completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

