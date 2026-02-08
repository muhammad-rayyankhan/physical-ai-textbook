#!/bin/bash
# Test the chat endpoint after DATABASE_URL fix

echo "Testing chat endpoint..."
echo ""

curl -X POST https://rayyan-11-physical-ai-textbook-backend.hf.space/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}' \
  2>&1 | head -50

echo ""
echo ""
echo "If you see an answer with citations, the deployment is successful!"
