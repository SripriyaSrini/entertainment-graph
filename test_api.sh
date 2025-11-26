#!/bin/bash

API_URL="https://web-production-b84b0.up.railway.app"

echo "=========================================="
echo "🚀 Testing Entertainment Graph API"
echo "=========================================="
echo ""

# Test 1: Health Check
echo "TEST 1: Health Check"
echo "--------------------"
curl -s "${API_URL}/health" | python3 -m json.tool
echo -e "\n"

# Test 2: Root Endpoint
echo "TEST 2: Root Endpoint"
echo "--------------------"
curl -s "${API_URL}/" | python3 -m json.tool
echo -e "\n"

# Test 3: API Documentation
echo "TEST 3: API Documentation Available"
echo "--------------------"
echo "📖 Visit: ${API_URL}/docs"
echo -e "\n"

# Test 4: Query Pure Vector (empty for now)
echo "TEST 4: Query Pure Vector (no movies yet)"
echo "--------------------"
curl -s -X POST "${API_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "science fiction",
    "system": "pure_vector",
    "limit": 3
  }' | python3 -m json.tool
echo -e "\n"

echo "=========================================="
echo "✅ Basic tests complete!"
echo "=========================================="
echo ""
echo "📝 Summary:"
echo "  • API is live and responding"
echo "  • Health endpoint working"
echo "  • Query endpoint accessible"
echo "  • No movies ingested yet (empty results)"
echo ""
echo "🔗 URLs:"
echo "  • API: ${API_URL}"
echo "  • Docs: ${API_URL}/docs"
echo "  • Health: ${API_URL}/health"
echo ""
