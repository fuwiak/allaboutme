# 🤖 Automation Test Guide

## ✅ What This Tests

Comprehensive test of **Automation** tab functionality:

1. 🔐 **Authentication** - Login and token validation
2. 📊 **Status Check** - Get automation enabled/disabled state
3. 🔄 **Toggle** - Enable/disable automation
4. 🌍 **Languages** - Get available languages (RU/EN)
5. 🔧 **Language Update** - Enable/disable specific languages
6. 📋 **Logs** - Retrieve automation activity logs
7. ⏰ **Schedule Settings** - Verify schedule configuration
8. ⚙️ **Celery Tasks** - Check background tasks setup

## 🚀 Quick Start

### Prerequisites

1. **Backend running:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

2. **Celery worker running:**
```bash
cd backend
source .venv/bin/activate
celery -A app.tasks.celery_app worker --beat --loglevel=info
```

3. **Redis running** (required for Celery)

### Run Test

```bash
cd /Users/user/allaboutme
python3 test_automation.py
```

## 📊 Expected Output

```
🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
🌟 AUTOMATION FUNCTIONALITY TEST 🌟
🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖

🔗 API Base: http://localhost:8000
👤 User: admin
🕐 Time: 2025-10-15 03:00:00

============================================================
🔐 LOGGING IN
============================================================
✅ Logged in as admin
🔑 Token: eyJhbGciOiJIUzI1NiIs...

============================================================
📊 TEST 1: Get Automation Status
============================================================
✅ Status retrieved successfully
   Enabled: False
   Pending posts: 0
   Published today: 0

============================================================
🔄 TEST 2: Toggle Automation
============================================================

📍 Enabling automation...
✅ Enabled: True

📍 Disabling automation...
✅ Disabled: True

============================================================
🌍 TEST 3: Get Languages
============================================================
✅ Languages retrieved: 2
   • ru: Russian (enabled: True)
   • en: English (enabled: False)

============================================================
🔧 TEST 4: Update Language
============================================================

📍 Enabling Russian...
✅ Russian enabled: True

📍 Enabling English...
✅ English enabled: True

============================================================
📋 TEST 5: Get Automation Logs
============================================================
✅ Logs retrieved: 5 entries
   • schedule_created: success (2025-10-15 02:00:00)
   • post_published: success (2025-10-15 01:30:00)
   • video_generated: success (2025-10-15 01:00:00)

============================================================
⏰ TEST 6: Schedule Settings
============================================================

📍 Updating schedule settings...
✅ Current settings loaded
   Language: ru
   Daily videos: 10

📊 Calculated:
   Interval: 60 minutes
   Posts per day: 17
   Working hours: 07:00 - 00:00 (17 hours)

============================================================
⚙️  TEST 7: Celery Tasks Configuration
============================================================
📋 Expected Celery tasks:
   • app.tasks.automation_tasks.create_daily_schedule_task
   • app.tasks.automation_tasks.process_pending_posts_task
   • app.tasks.automation_tasks.check_and_notify_errors_task

💡 To verify tasks are running:
   1. Check Celery worker logs
   2. Run: celery -A app.tasks.celery_app inspect active
   3. Check Redis for scheduled tasks

============================================================
📊 TEST SUMMARY
============================================================

✅ Passed: 8/8
❌ Failed: 0/8

📋 Details:
   ✅ Login
   ✅ Get Status
   ✅ Toggle Automation
   ✅ Get Languages
   ✅ Update Language
   ✅ Get Logs
   ✅ Schedule Settings
   ✅ Celery Config

🎉 ALL TESTS PASSED! Automation fully functional!

💡 Next steps:
   1. Check Celery worker is running
   2. Verify Redis connection
   3. Test automation in UI: http://localhost:8000/automation
   4. Enable automation and check scheduled posts

🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
```

## 🔍 What Each Test Checks

### Test 1: Get Status
- ✅ API endpoint responds
- ✅ Returns enabled/disabled state
- ✅ Shows pending and published counts
- ✅ No auth errors

### Test 2: Toggle Automation
- ✅ Can enable automation
- ✅ Can disable automation
- ✅ State changes persist
- ✅ No database errors

### Test 3: Get Languages
- ✅ Returns all languages (RU, EN)
- ✅ Shows enabled status for each
- ✅ Proper JSON structure

### Test 4: Update Language
- ✅ Can enable Russian
- ✅ Can enable English
- ✅ Changes save to database
- ✅ Multiple languages can be active

### Test 5: Get Logs
- ✅ Retrieves automation logs
- ✅ Shows recent activity
- ✅ Includes action, status, timestamp
- ✅ Pagination works (limit param)

### Test 6: Schedule Settings
- ✅ Can retrieve current settings
- ✅ Shows daily video count
- ✅ Calculates posts per day
- ✅ Validates time ranges

### Test 7: Celery Config
- ✅ Lists expected background tasks
- ✅ Provides verification commands
- ✅ Checks task registration

## 🐛 Troubleshooting

### Test fails with "Connection refused"
```bash
# Start backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Test fails with "401 Unauthorized"
```bash
# Check if default user exists in database
# Default: username=admin, password=admin
```

### "Languages not found" error
```bash
# Run migrations
cd backend
alembic upgrade head
```

### "Celery tasks not working"
```bash
# Start Celery worker
cd backend
celery -A app.tasks.celery_app worker --beat --loglevel=info
```

### "Redis connection failed"
```bash
# Start Redis (macOS)
brew services start redis

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

## 📋 Manual UI Testing

After automated tests pass, test in browser:

### 1. Open Automation Tab
```
http://localhost:8000/automation
```

### 2. Check Status
- [ ] Shows current automation state (Active/Inactive)
- [ ] Shows pending posts count
- [ ] Shows published today count

### 3. Toggle Automation
- [ ] Click "Enable Automation" button
- [ ] Status changes to "Active"
- [ ] Click "Disable Automation"
- [ ] Status changes to "Inactive"

### 4. Schedule Settings
- [ ] Post Interval slider (10-120 minutes)
- [ ] Start Hour selector (0-23)
- [ ] End Hour selector (0-23)
- [ ] Min Posts/Day input
- [ ] Max Posts/Day input
- [ ] Real-time calculation shows posts per day
- [ ] Click "Save Schedule"

### 5. Languages
- [ ] Russian checkbox
- [ ] English checkbox
- [ ] Changes save immediately

### 6. Activity Logs
- [ ] Shows recent automation actions
- [ ] Displays timestamps
- [ ] Shows success/failure status

## 🎯 Success Criteria

All tests must pass:
- ✅ All API endpoints return 200
- ✅ Data structure matches schema
- ✅ Changes persist in database
- ✅ No authentication errors
- ✅ Celery tasks registered
- ✅ UI displays correctly
- ✅ Settings save successfully

## 📚 Related Documentation

- Backend API: `http://localhost:8000/docs`
- Celery Setup: `backend/run_celery.sh`
- Database Models: `backend/app/models_extended.py`
- Frontend: `frontend/src/routes/automation/+page.svelte`

---

**✨ Test automation functionality end-to-end! 🤖**

