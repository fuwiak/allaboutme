# 🤖 Automation Features - Complete Guide

## ✅ What Was Added:

### 1. 🌍 Language Switcher (RU/EN)
- Switch between Russian and English
- Affects script generation
- Affects captions and hashtags

### 2. 🤖 Autonomous Operation
- Automatic schedule creation (daily at 00:01)
- Automatic script generation
- Automatic video creation
- Automatic publishing to all platforms

### 3. 📅 Smart Scheduling
- Publishes 07:00 - 00:00
- Even distribution (10-15 videos/day)
- Configurable intervals

### 4. 🔔 Error Notifications
- Automatic Telegram alerts on failures
- Hourly error summaries
- You only check results

### 5. ⚙️ Easy Configuration
- Change themes in UI
- Modify prompts
- Adjust video count
- All without code changes

---

## 🎯 How Automation Works:

### Daily Flow:

```
00:01 → Create Schedule (10-15 time slots)
07:00 → First post scheduled
  ↓
  Generate script → Generate video → Publish
  ↓
08:30 → Second post
  ↓
  Generate script → Generate video → Publish
  ↓
... (continues throughout day)
  ↓
23:30 → Last post
```

### Error Handling:

```
Error occurs → Log to database → Send Telegram notification
```

---

## 📋 New Endpoints:

```
POST   /api/automation/enable          - Turn on automation
POST   /api/automation/disable         - Turn off automation
GET    /api/automation/status          - Check if running
GET    /api/automation/schedule        - View today's schedule
POST   /api/automation/schedule/create - Create new schedule
GET    /api/automation/logs            - View automation logs
POST   /api/automation/languages/{code}/activate - Switch language
GET    /api/automation/languages       - List languages
```

---

## 🆕 New Page: /automation

### Features:

1. **Automation Toggle**:
   - Big green button: ✅ Включено
   - Big gray button: ⏸️ Выключено
   - Click to enable/disable

2. **Stats Cards**:
   - Pending posts count
   - Published today count

3. **Language Switcher**:
   - 🇷🇺 Русский button
   - 🇬🇧 English button
   - Click to switch

4. **Automation Logs**:
   - Real-time logs
   - Color-coded (ERROR, WARNING, INFO)
   - Shows what automation is doing
   - Notification status

---

## 🔧 Configuration:

### Settings You Can Change:

1. **Daily Videos Count**: Settings → Content → Daily Videos
2. **Themes**: Settings → Content → Themes (comma-separated)
3. **System Prompt**: Settings → Content → System Prompt
4. **Caption Template**: Settings → Content → Caption Template
5. **Publishing Times**: Hardcoded 07:00-00:00 (можно добавить в settings)

### Example Themes (Astrology-focused):

```
daily horoscope,
Mercury retrograde facts,
Human Design - Generator tips,
Numerology life path,
Matrix of Destiny insights,
Zodiac compatibility,
Moon phases,
Astro memes,
Planetary transits,
Spiritual awakening
```

---

## 🚀 How to Use Automation:

### Step 1: Configure

1. Go to **Settings**
2. Set **Daily Videos**: 10-15
3. Add **Themes** (astrology-related)
4. Set **System Prompt** for script style
5. Add **API Keys** (Groq, Telegram, social media)

### Step 2: Enable

1. Go to **Automation** page
2. Click **"✅ Включено"** button
3. System creates schedule automatically

### Step 3: Forget About It! 😎

System will:
- Generate scripts every few hours
- Create videos automatically
- Publish to all platforms
- Send you error notifications if something breaks

### Step 4: Check Results

1. **Automation** page → See logs
2. **Publish** page → See published videos
3. **Telegram** → Get notifications

---

## 📱 Platforms Supported:

1. **Telegram** - Channel posts
2. **YouTube** - Shorts
3. **TikTok** - Videos
4. **Instagram** - Reels

All published automatically based on schedule!

---

## 🔔 Notification Types:

### You'll Get Telegram Alerts For:

- ❌ **Errors**: Script generation failed
- ❌ **Errors**: Video creation failed
- ❌ **Errors**: Publishing failed
- ℹ️ **Info**: Daily schedule created
- ✅ **Success**: Videos published (optional)

---

## ⚙️ Behind the Scenes:

### Celery Beat Tasks:

1. **00:01 daily** - Create schedule for the day
2. **Every 5 min** - Process pending posts
3. **Every hour** - Check and send error notifications

### Database Tables:

- `scheduled_posts` - Publishing schedule
- `automation_logs` - Activity logs
- `languages` - Language settings

---

## 🎯 Access New Page:

1. Login to app
2. Click **"Automation"** in navigation
3. See automation controls!

---

## 📊 Migration Impact:

**New Files:**
- `backend/app/models_extended.py` - New DB models
- `backend/app/services/scheduler_service.py` - Scheduling logic
- `backend/app/tasks/automation_tasks.py` - Celery tasks
- `backend/app/routers/automation.py` - API endpoints
- `frontend/src/routes/automation/+page.svelte` - UI page

**Total**: ~500 new lines of code

---

## ✅ What You Asked For:

1. ✅ Language switcher (RU/EN flag)
2. ✅ Astrology/numerology focused themes
3. ✅ Auto-publish to Reels, Shorts, TikTok
4. ✅ Time distribution (07:00-00:00, 10-15 videos)
5. ✅ Autonomous operation
6. ✅ Error notifications
7. ✅ Easy theme/prompt configuration

---

**Everything implemented! Go to /automation page and enable it!** 🚀

