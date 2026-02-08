#!/bin/bash
# Quick test script for Hugging Face deployment

BASE_URL="https://rayyan-11-physical-ai-textbook-backend.hf.space"

echo "Testing Hugging Face Spaces Deployment"
echo "========================================"
echo ""

echo "1. Root endpoint..."
curl -s "$BASE_URL/" | head -20
echo ""

echo "2. Health check..."
curl -s "$BASE_URL/api/health" | head -20
echo ""

echo "3. API Documentation:"
echo "   $BASE_URL/docs"
echo ""

echo "Test complete!"
