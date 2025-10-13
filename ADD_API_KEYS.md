# 🔑 How to Add API Keys

## Problem
Celery worker shows: `Invalid API Key` for Groq

## Solution

### Step 1: Edit run_celery.sh

```bash
cd backend
nano run_celery.sh
```

### Step 2: Replace API Keys (line 12-15)

Change this:
```bash
export GROQ_API_KEY="your-groq-api-key-here"  # ← CHANGE THIS!
export TELEGRAM_BOT_TOKEN="your-telegram-token"
export TG_MOD_CHAT_ID="your-chat-id"
export HEYGEN_API_KEY="your-heygen-key"
```

To your real keys:
```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxx"  # Your real Groq key
export TELEGRAM_BOT_TOKEN="1234567890:ABCDefGhIjKlMnOpQrStUvWxYz"  # Optional
export TG_MOD_CHAT_ID="-1001234567890"  # Optional
export HEYGEN_API_KEY="your-real-heygen-key"  # Optional
```

### Step 3: Restart Celery

```bash
# Stop current Celery (Ctrl+C in Terminal 3)
# Then start again:
cd backend
./run_celery.sh
```

### Step 4: Test Script Generation

1. Go to http://localhost:5173
2. Login: `admin` / `admin123`
3. Dashboard → Click "Generate Scripts"
4. Progress modal should show
5. Scripts generated! ✅

---

## 📍 Where to Get API Keys:

### Groq API Key (REQUIRED for script generation)
1. Go to: https://console.groq.com
2. Sign up / Login
3. Go to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

### Telegram Bot Token (OPTIONAL - for notifications)
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions
5. Copy token (format: `123456:ABC-DEF...`)

### Get Telegram Chat ID (OPTIONAL)
1. Create a group or channel
2. Add your bot to it
3. Send a message
4. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. Look for `"chat":{"id":-1001234567890}`
6. Copy the ID

### HeyGen API Key (OPTIONAL - for paid video generation)
1. Go to: https://app.heygen.com
2. Sign up / Login
3. Go to Settings → API Keys
4. Create new key
5. Copy the key

---

## 🔄 Quick Commands:

### Add Groq Key:
```bash
# Edit run_celery.sh
nano backend/run_celery.sh

# Change line 12:
export GROQ_API_KEY="gsk_your_real_key_here"

# Save and restart Celery
```

### Alternative: Use .env file

Create `backend/.env`:
```bash
cd backend
nano .env
```

Add:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/allaboutme
REDIS_URL=redis://localhost:6379/0
STORAGE_PATH=/tmp/allaboutme
JWT_SECRET_KEY=dev-secret
GROQ_API_KEY=gsk_your_real_key_here
TELEGRAM_BOT_TOKEN=your_token
TG_MOD_CHAT_ID=your_chat_id
```

Then modify `run_celery.sh` to load from .env:
```bash
# Load from .env
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi
```

---

## ✅ After Adding Keys:

1. Restart Celery: `./run_celery.sh`
2. Go to Dashboard
3. Click "Generate Scripts"
4. Should work now! ✅

---

**Priority**: Add `GROQ_API_KEY` first - it's required for script generation!

