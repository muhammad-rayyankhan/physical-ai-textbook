# Groq API Setup Guide

Groq provides fast, free LLM inference with generous rate limits. This guide shows you how to get your API key.

## Why Groq?

- **Free Tier**: Generous free tier with high rate limits
- **Fast**: Extremely fast inference (faster than OpenAI)
- **No Credit Card**: Free tier doesn't require payment info
- **Good Models**: Access to Llama 3.1 70B and other models
- **OpenAI Compatible**: Uses OpenAI-compatible API format

## Getting Your Groq API Key (2 minutes)

### Step 1: Sign Up

1. Go to: https://console.groq.com
2. Click "Sign Up" or "Get Started"
3. Sign up with:
   - Google account (easiest)
   - GitHub account
   - Email address

### Step 2: Create API Key

1. After signing in, you'll be on the dashboard
2. Click "API Keys" in the left sidebar
3. Click "Create API Key"
4. Give it a name: `textbook-backend`
5. Click "Create"
6. **Copy the API key** (starts with `gsk_`)
   - ⚠️ Save it now - you won't see it again!

### Step 3: Add to Railway

In Railway Dashboard → Your Service → Variables:

```
GROQ_API_KEY
Value: gsk_your_api_key_here
```

## Rate Limits (Free Tier)

- **Requests**: 30 requests per minute
- **Tokens**: 14,400 tokens per minute
- **Daily**: 14,400 requests per day

This is more than enough for a textbook chatbot!

## Available Models

The backend is configured to use `llama-3.1-70b-versatile`, which provides:
- High quality responses
- Fast inference
- Good instruction following
- Free tier access

Other available models:
- `llama-3.1-8b-instant` - Faster, smaller model
- `mixtral-8x7b-32768` - Good for longer contexts
- `gemma2-9b-it` - Google's Gemma model

To change models, update the `GROQ_MODEL` environment variable in Railway.

## Testing Your API Key

You can test your API key with curl:

```bash
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer gsk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-70b-versatile",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Troubleshooting

### "Invalid API Key" Error

- Check that you copied the full key (starts with `gsk_`)
- Make sure there are no extra spaces
- Verify the key is active in Groq console

### Rate Limit Errors

- Free tier: 30 requests/minute
- If you hit limits, wait 60 seconds
- Consider upgrading to paid tier for higher limits

### Model Not Found

- Verify model name is correct: `llama-3.1-70b-versatile`
- Check Groq's model list: https://console.groq.com/docs/models

## Cost Comparison

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| **Groq** | 14,400 req/day | $0.05-0.27 per 1M tokens |
| OpenAI | $5 credit (expires) | $0.50-2.00 per 1M tokens |
| Ollama | Unlimited (local) | Server costs only |

## Next Steps

After getting your Groq API key:
1. Add it to Railway environment variables
2. Redeploy your backend
3. Test the `/api/health` endpoint
4. Try asking questions in the frontend chat

---

**Documentation**: https://console.groq.com/docs/quickstart
**API Reference**: https://console.groq.com/docs/api-reference
