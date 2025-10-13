#!/bin/bash

# Script to delete old Flet files and documentation
# Run this AFTER testing the new Svelte + FastAPI version

echo "🧹 Cleaning up old Flet-related files..."

# Backup first
echo "📦 Creating backup..."
mkdir -p _backup_old_files
cp -r ui.py ui_old.py ui.py.bak test_ui.py bot.py run_bot.py _backup_old_files/ 2>/dev/null
cp -r main.py generate_video.py scheduler.py check_setup.py get_chat_id.py _backup_old_files/ 2>/dev/null

# Delete old UI files
echo "🗑️  Deleting old UI files..."
rm -f ui.py ui_old.py ui.py.bak test_ui.py

# Delete old bot files (keep bot_simple.py - it's migrated)
echo "🗑️  Deleting old bot files..."
rm -f bot.py run_bot.py

# Delete old main/scheduler files
echo "🗑️  Deleting old orchestration files..."
rm -f main.py generate_video.py scheduler.py

# Delete old test/setup files
echo "🗑️  Deleting old utility files..."
rm -f check_setup.py get_chat_id.py test_*.py quick_*.py

# Delete old documentation (keep README.md, DEPLOYMENT_GUIDE.md, MIGRATION_STATUS.md)
echo "🗑️  Deleting old documentation..."
rm -f CHANGELOG_*.md UPDATE_*.md FIXES_*.md WORKFLOW*.md 
rm -f UI_CONTROL.md HEYGEN_*.md ERROR_MODAL_UPDATE.md OPENSOURCE_*.md
rm -f TELEGRAM_SETUP.md QUICK_START*.md VIDEO_PREVIEW_UPDATE.md
rm -f MIGRATION_TO_FLET_1.0.md TEST_HEYGEN_README.md TWO_STEP_GENERATION.md
rm -f БЫСТРЫЙ_СТАРТ.md ГОТОВО.txt ЗАПУСК.md ИНСТРУКЦИЯ.md

# Delete log files
echo "🗑️  Deleting log files..."
rm -f *.log

# Delete start scripts (replaced by new start.sh)
echo "🗑️  Deleting old start scripts..."
rm -f start.bat

# Delete n8n workflow (if not using)
echo "🗑️  Deleting n8n files..."
rm -f n8n_video_generation_workflow.json N8N_WORKFLOW_README.md

# Keep these important files:
# - config.yaml (will be migrated to DB)
# - env.template (reference)
# - requirements.txt (old, but reference)
# - renderer.py, generator.py, publisher.py, opensource_video.py (migrated to backend/app/services/)
# - bot_simple.py (migrated to backend/app/services/telegram_bot.py)

echo "✅ Cleanup complete!"
echo ""
echo "Backed up files are in: _backup_old_files/"
echo ""
echo "Next steps:"
echo "1. Test the new Svelte + FastAPI version"
echo "2. Run: python backend/migrate_config.py (to migrate config.yaml to database)"
echo "3. If everything works, you can delete _backup_old_files/"
echo ""
echo "Files that were kept (for reference):"
echo "  - config.yaml (migrate to DB with migrate_config.py)"
echo "  - env.template (reference for environment variables)"
echo "  - requirements.txt (old version - use backend/requirements.txt)"
echo ""

