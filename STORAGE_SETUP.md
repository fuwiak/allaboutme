# 📁 Storage Setup - Video & Audio Access

## ✅ Problem Solved

**Before:** Videos saved as local file paths (e.g., `/tmp/ai24tv/video_xxx.mp4`)  
**After:** Videos accessible via HTTP (e.g., `/storage/videos/video_1.mp4`)

## 🎯 How It Works Now

### 1. Storage Structure

```
STORAGE_PATH/
  ├── videos/
  │   ├── video_1.mp4
  │   ├── video_2.mp4
  │   └── ...
  ├── audio/
  │   ├── audio_1.mp3
  │   ├── audio_2.mp3
  │   └── ...
  └── backgrounds/
      ├── custom_bg_1.png
      └── ...
```

### 2. HTTP Access

**Backend mounts storage:**
```python
app.mount("/storage", StaticFiles(directory=STORAGE_PATH))
```

**Access URLs:**
- Video: `http://yourdomain.com/storage/videos/video_1.mp4`
- Audio: `http://yourdomain.com/storage/audio/audio_1.mp3`
- Background: `http://yourdomain.com/storage/backgrounds/image.png`

### 3. Frontend Usage

```svelte
<!-- VideoCard.svelte -->
<video controls>
  <source src="/storage/videos/video_{video.id}.mp4" type="video/mp4" />
</video>

<audio controls>
  <source src="/storage/audio/audio_{video.id}.mp3" type="audio/mpeg" />
</audio>
```

## 🚀 Railway Configuration

### Step 1: Set STORAGE_PATH

**In Railway App Service → Variables:**
```
STORAGE_PATH=/app/storage
```

**Why `/app/storage`:**
- `/app` is the working directory on Railway
- `/storage` creates persistent subfolder
- Survives deployments (if using volumes)

### Step 2: Add Volume (Optional, Recommended)

**For persistent storage across deployments:**

1. Railway → App Service → Settings
2. Add Volume
3. Mount Path: `/app/storage`
4. Size: 1 GB (or more)

**Without volume:** Files deleted on redeploy  
**With volume:** Files persist permanently

### Step 3: Environment Variables Summary

```bash
# Database
DATABASE_URL=postgresql://postgres:...@postgres.railway.internal:5432/railway?sslmode=require

# Redis
REDIS_URL=redis://default:...@redis.railway.internal:6379

# Storage
STORAGE_PATH=/app/storage

# API Keys
GROQ_API_KEY=gsk_...
ELEVENLABS_API_KEY=sk_...
TELEGRAM_BOT_TOKEN=...
TG_PUBLIC_CHAT_ID=...

# JWT
JWT_SECRET_KEY=your-secret-key-here
```

## 🔧 Local Development

### Current Setup

```bash
# backend/.env
STORAGE_PATH=/tmp/allaboutme
```

**Issue:** `/tmp` gets cleared on restart

**Better:**
```bash
STORAGE_PATH=/Users/user/allaboutme/storage
```

### Create Storage Directory

```bash
mkdir -p /Users/user/allaboutme/storage/{videos,audio,backgrounds}
```

### Update .env

```bash
# Edit backend/.env
STORAGE_PATH=/Users/user/allaboutme/storage
```

## 📊 Video Preview Fix

### Problem

Videos showing as: `file:///tmp/ai24tv/video_xxx.mp4`

### Solution

**1. Backend saves to STORAGE_PATH:**
```python
# In video_tasks.py
video_path = get_video_path(video.id)  # Returns: storage/videos/video_1.mp4
```

**2. Frontend accesses via HTTP:**
```javascript
// VideoCard.svelte
const videoUrl = `/storage/videos/video_${video.id}.mp4`;
```

**3. Backend serves storage:**
```python
# main.py
app.mount("/storage", StaticFiles(directory=STORAGE_PATH))
```

## 🐛 Troubleshooting

### Video not playing in Publish

**Check:**
1. Is file saved to storage?
```bash
ls -lh /tmp/allaboutme/videos/
```

2. Is storage mounted?
```bash
curl http://localhost:8000/storage/videos/video_1.mp4
```

3. Check token:
```javascript
// Browser console
localStorage.getItem('auth_token')
```

### "File not found" error

**Fix:**
```bash
# Create storage structure
mkdir -p $STORAGE_PATH/{videos,audio,backgrounds}

# Check permissions
chmod 755 $STORAGE_PATH
```

### Railway: Videos disappear after deploy

**Solution:** Add Railway Volume

## 📋 Migration Checklist

### Local → Railway

- [x] Mount `/storage` in main.py
- [ ] Set `STORAGE_PATH=/app/storage` in Railway
- [ ] Add Railway Volume (optional but recommended)
- [ ] Redeploy
- [ ] Test video preview

### Files to Keep

```gitignore
# DON'T ignore storage in production
# storage/  ← Remove this line if present

# DO ignore in development
/tmp/
```

## 🎯 Next Steps

1. ✅ Storage mounted in backend
2. Update VideoCard to use correct URLs (if needed)
3. Set STORAGE_PATH in Railway
4. Add Railway Volume for persistence
5. Test video/audio playback

---

**✨ Videos and audio now accessible via HTTP! 🎥🔊**

