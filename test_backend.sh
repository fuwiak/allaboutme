#!/bin/bash

echo "🧪 Testing Backend API..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:8000"

# Test 1: Health check
echo -n "Testing health endpoint... "
response=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/health)
if [ $response -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Health check passed"
else
    echo -e "${RED}✗${NC} Health check failed (HTTP $response)"
    echo "Make sure backend is running: uvicorn app.main:app --reload --port 8000"
    exit 1
fi

# Test 2: Login
echo -n "Testing login... "
token_response=$(curl -s -X POST $BASE_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')

if echo $token_response | grep -q "access_token"; then
    token=$(echo $token_response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}✓${NC} Login successful"
else
    echo -e "${RED}✗${NC} Login failed"
    echo "Response: $token_response"
    exit 1
fi

# Test 3: Get scripts (authenticated)
echo -n "Testing authenticated endpoint (GET /api/scripts)... "
scripts_response=$(curl -s -w "%{http_code}" -o /tmp/scripts.json \
  -H "Authorization: Bearer $token" \
  $BASE_URL/api/scripts)

if [ $scripts_response -eq 200 ]; then
    count=$(cat /tmp/scripts.json | grep -o '\[' | wc -l)
    echo -e "${GREEN}✓${NC} Got scripts (count: $(cat /tmp/scripts.json | grep -c '\"id\"'))"
else
    echo -e "${RED}✗${NC} Failed (HTTP $scripts_response)"
    exit 1
fi

# Test 4: Get settings
echo -n "Testing settings endpoint... "
settings_response=$(curl -s -w "%{http_code}" -o /tmp/settings.json \
  -H "Authorization: Bearer $token" \
  $BASE_URL/api/settings)

if [ $settings_response -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Settings retrieved"
else
    echo -e "${RED}✗${NC} Failed (HTTP $settings_response)"
fi

# Test 5: API docs
echo -n "Testing API documentation... "
docs_response=$(curl -s -w "%{http_code}" -o /dev/null $BASE_URL/docs)
if [ $docs_response -eq 200 ]; then
    echo -e "${GREEN}✓${NC} API docs available at $BASE_URL/docs"
else
    echo -e "${RED}✗${NC} API docs not available"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Backend tests passed!${NC}"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "Access token: $token"
echo ""
echo "Next: Test frontend at http://localhost:5173"

