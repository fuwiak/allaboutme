#!/bin/bash

echo "🧪 Testing AllAboutMe Installation..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

# Check Node
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found"
    exit 1
fi

# Check backend structure
echo ""
echo "Checking backend structure..."
for dir in "backend/app" "backend/app/routers" "backend/app/services" "backend/app/tasks" "backend/alembic"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} $dir missing"
    fi
done

# Check backend files
echo ""
echo "Checking backend files..."
for file in "backend/app/main.py" "backend/app/models.py" "backend/requirements.txt" "Dockerfile" "railway.json" "start.sh"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# Check frontend structure
echo ""
echo "Checking frontend structure..."
for dir in "frontend/src" "frontend/src/routes" "frontend/src/lib" "frontend/src/lib/components"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} $dir missing"
    fi
done

# Check frontend files
echo ""
echo "Checking frontend files..."
for file in "frontend/package.json" "frontend/svelte.config.js" "frontend/vite.config.ts" "frontend/tailwind.config.js"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# Check frontend pages
echo ""
echo "Checking frontend pages..."
for file in "frontend/src/routes/+page.svelte" "frontend/src/routes/dashboard/+page.svelte" "frontend/src/routes/drafts/+page.svelte" "frontend/src/routes/publish/+page.svelte" "frontend/src/routes/settings/+page.svelte"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

# Check frontend components
echo ""
echo "Checking frontend components..."
for file in "frontend/src/lib/api.ts" "frontend/src/lib/stores.ts" "frontend/src/lib/websocket.ts" "frontend/src/lib/components/ProgressModal.svelte" "frontend/src/lib/components/ScriptCard.svelte" "frontend/src/lib/components/VideoCard.svelte"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file missing"
    fi
done

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Installation check complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Test backend:  cd backend && pip install -r requirements.txt"
echo "  2. Test frontend: cd frontend && npm install"
echo "  3. Read QUICK_START.md for detailed instructions"
echo ""

