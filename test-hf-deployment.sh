#!/bin/bash
# Test Hugging Face Spaces Deployment

BASE_URL="https://rayyan-11-physical-ai-textbook-backend.hf.space"

echo "Testing Hugging Face Spaces Backend Deployment"
echo "=============================================="
echo ""

echo "1. Testing root endpoint..."
curl -s "$BASE_URL/" | jq '.' || echo "Failed"
echo ""

echo "2. Testing health check..."
curl -s "$BASE_URL/api/health" | jq '.' || echo "Failed"
echo ""

echo "3. Testing chat query..."
curl -s -X POST "$BASE_URL/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?"}' | jq '.' || echo "Failed"
echo ""

echo "4. API Documentation available at:"
echo "   $BASE_URL/docs"
echo ""

echo "Deployment test complete!"
