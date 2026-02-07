#!/bin/bash
# Quick Start Script for RAG Chatbot MVP
# Run this script after installing Ollama and pulling a model

set -e

echo "=========================================="
echo "RAG Chatbot MVP - Quick Start"
echo "=========================================="
echo ""

# Check if Ollama is installed
echo "Step 1: Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo "Please install from: https://ollama.ai"
    exit 1
fi
echo "✅ Ollama is installed"
echo ""

# Check if model is available
echo "Step 2: Checking for Ollama model..."
if ! ollama list | grep -q "llama3.2\|mistral"; then
    echo "❌ No model found!"
    echo "Please run: ollama pull llama3.2"
    exit 1
fi
echo "✅ Model is available"
echo ""

# Install backend dependencies
echo "Step 3: Installing backend dependencies..."
cd backend
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create data directory
echo "Step 4: Creating data directory..."
mkdir -p data/chroma
echo "✅ Data directory created"
echo ""

# Run ingestion
echo "Step 5: Running document ingestion..."
python -m rag.scripts.ingest_textbook --clear
echo "✅ Ingestion complete"
echo ""

# Test backend
echo "Step 6: Testing backend (will start server in background)..."
python -m src.main &
BACKEND_PID=$!
sleep 5

# Test health endpoint
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID
    exit 1
fi

# Test chat endpoint
echo "Testing chat endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}')

if echo "$RESPONSE" | grep -q "answer"; then
    echo "✅ Chat endpoint working"
else
    echo "❌ Chat endpoint failed"
    kill $BACKEND_PID
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Backend setup complete!"
echo "=========================================="
echo ""
echo "Backend is running at: http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""
echo "Next steps:"
echo "1. Open a new terminal"
echo "2. cd website"
echo "3. npm start"
echo "4. Open http://localhost:3000"
echo "5. Click the chat button in the bottom-right corner"
echo ""
echo "To stop the backend: kill $BACKEND_PID"
echo ""
