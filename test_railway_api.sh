#!/bin/bash

# Test Railway deployment
# Replace YOUR_RAILWAY_URL with your actual Railway URL from the dashboard

RAILWAY_URL="https://web-production-b84b0.up.railway.app"

echo "=========================================="
echo "Testing Railway Deployment"
echo "=========================================="
echo ""

# Test 1: Health check
echo "1. Testing health endpoint..."
curl -s "${RAILWAY_URL}/health" | jq '.' 2>/dev/null || curl -s "${RAILWAY_URL}/health"
echo ""
echo ""

# Test 2: Root endpoint
echo "2. Testing root endpoint..."
curl -s "${RAILWAY_URL}/" | jq '.' 2>/dev/null || curl -s "${RAILWAY_URL}/"
echo ""
echo ""

# Test 3: Query with Pure Vector system (minimal test - no movies ingested yet)
echo "3. Testing query endpoint (Pure Vector)..."
curl -X POST "${RAILWAY_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test query",
    "system": "pure_vector",
    "limit": 3
  }' | jq '.' 2>/dev/null || curl -X POST "${RAILWAY_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "system": "pure_vector", "limit": 3}'
echo ""
echo ""

echo "=========================================="
echo "Tests complete!"
echo "=========================================="
