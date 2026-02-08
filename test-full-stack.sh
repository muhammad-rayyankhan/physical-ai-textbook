#!/bin/bash
# Full Stack Integration Test

echo "=========================================="
echo "Physical AI Textbook - Full Stack Test"
echo "=========================================="
echo ""

echo "1. Testing Backend Health..."
curl -s https://rayyan-11-physical-ai-textbook-backend.hf.space/api/health | python -m json.tool
echo ""

echo "2. Testing Backend Chat Endpoint..."
curl -s -X POST https://rayyan-11-physical-ai-textbook-backend.hf.space/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}' | python -m json.tool | head -30
echo ""

echo "3. Frontend URL:"
echo "   https://website-seven-eta-74.vercel.app"
echo ""

echo "4. Manual Test Required:"
echo "   - Open the frontend URL in your browser"
echo "   - Click the chat button (bottom right corner)"
echo "   - Type: 'What is Physical AI?'"
echo "   - Verify you get an answer with citations"
echo ""

echo "=========================================="
echo "If the chat widget works, deployment is complete!"
echo "=========================================="
