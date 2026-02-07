# Hugging Face API Setup Guide

Get your free Hugging Face API token for embeddings.

## Why Hugging Face?

- **Free**: Unlimited API calls (rate limited)
- **No Credit Card**: Free tier doesn't require payment
- **Fast**: Serverless inference
- **Reliable**: Same model as local (all-MiniLM-L6-v2)
- **No Installation**: No need to download large models

## Getting Your Token (2 minutes)

### Step 1: Create Account

1. Go to: https://huggingface.co
2. Click "Sign Up"
3. Sign up with:
   - Email
   - Google account
   - GitHub account

### Step 2: Create Access Token

1. After login, go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Configure:
   - Name: `textbook-embeddings`
   - Type: **Read** (not Write)
4. Click "Generate token"
5. **Copy the token** (starts with `hf_`)
   - ⚠️ Save it now - you can regenerate but better to save

### Step 3: Add to Render

In Render Dashboard → Your Service → Environment:

```
HUGGINGFACE_API_KEY
Value: hf_your_token_here
```

## Rate Limits (Free Tier)

- **Requests**: Rate limited (typically 1-2 req/sec)
- **Models**: Access to all public models
- **Compute**: Shared serverless infrastructure

For a textbook chatbot, this is more than sufficient!

## Testing Your Token

Test with curl:

```bash
curl https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2 \
  -H "Authorization: Bearer hf_your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "Hello world"}'
```

Should return a 384-dimensional embedding vector.

## Model Information

**Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Speed**: Fast (~50ms per request)
- **Quality**: Good for semantic search
- **Size**: 80MB (but you don't download it!)

## Troubleshooting

### "Model is loading" Error

First request to a model may take 20-30 seconds to load. Subsequent requests are fast.

Solution: The API includes `"wait_for_model": true` option which handles this automatically.

### Rate Limit Errors

If you hit rate limits:
- Free tier: ~1-2 requests/second
- Wait a moment and retry
- Consider Hugging Face Pro ($9/month) for higher limits

### Token Invalid

- Check token starts with `hf_`
- Verify token type is "Read"
- Regenerate token if needed

## Upgrading (Optional)

If you need higher rate limits:

**Hugging Face Pro** ($9/month):
- Higher rate limits
- Priority access
- Faster inference
- Private models

For most textbook chatbots, free tier is sufficient.

## Alternative: OpenAI Embeddings

If Hugging Face is too slow, you can use OpenAI:

**Cost**: ~$0.02 per 1M tokens (~$0.10/month for textbook)

Update environment variables:
```
USE_OPENAI_EMBEDDINGS=true
OPENAI_API_KEY=sk-your-key
```

And update `rag.py` to import from `embeddings.py` instead of `embeddings_hf.py`.

---

**Documentation**: https://huggingface.co/docs/api-inference
**Models**: https://huggingface.co/models?pipeline_tag=feature-extraction
