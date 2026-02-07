# Railway Backend Deployment Guide

## Quick Deploy via Dashboard

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select Repository**: `muhammad-rayyankhan/physical-ai-textbook`
5. **Configure**:
   - Root Directory: `backend`
   - Build Command: (auto-detected from railway.json)
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

## Required Environment Variables

Add these in Railway Dashboard → Your Service → Variables:

```env
# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=textbook_chunks

# Neon PostgreSQL Database
DATABASE_URL=postgresql://user:password@host/database

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key

# API Configuration
API_HOST=0.0.0.0
API_PORT=$PORT
CORS_ORIGINS=https://website-seven-eta-74.vercel.app,http://localhost:3000

# Admin API Key (for ingestion)
ADMIN_API_KEY=your-secure-random-key

# Environment
ENVIRONMENT=production
```

## Setup External Services

### 1. Qdrant Cloud (Vector Database)

1. Go to https://cloud.qdrant.io
2. Sign up for free tier
3. Create a cluster
4. Copy the cluster URL and API key
5. Add to Railway environment variables

### 2. Neon Database (PostgreSQL)

1. Go to https://neon.tech
2. Sign up for free tier
3. Create a new project
4. Copy the connection string
5. Add to Railway environment variables as `DATABASE_URL`

### 3. OpenAI API Key

1. Go to https://platform.openai.com
2. Create an API key
3. Add to Railway environment variables as `OPENAI_API_KEY`

## After Deployment

### 1. Get Backend URL

Railway will provide a URL like: `https://your-app.railway.app`

### 2. Update Frontend CORS

Update the backend's `CORS_ORIGINS` to include your Vercel URL:
```
CORS_ORIGINS=https://website-seven-eta-74.vercel.app
```

### 3. Update Frontend API URL

In your Vercel project, add environment variable:
```
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

### 4. Ingest Textbook Data

Run the ingestion script to populate the vector database:

```bash
# Option A: Via Railway CLI
railway run python -m rag.scripts.ingest_textbook --clear

# Option B: Create a one-time job in Railway Dashboard
# Command: python -m rag.scripts.ingest_textbook --clear
```

## Verify Deployment

1. **Health Check**: Visit `https://your-app.railway.app/api/health`
2. **API Docs**: Visit `https://your-app.railway.app/docs`
3. **Test Chat**: Use the frontend to ask a question

## Alternative: Railway CLI Deployment

If you prefer CLI deployment:

```bash
# Login (opens browser)
railway login

# Link to project
cd backend
railway link

# Deploy
railway up

# Add environment variables
railway variables set QDRANT_URL=https://...
railway variables set QDRANT_API_KEY=...
railway variables set DATABASE_URL=postgresql://...
railway variables set OPENAI_API_KEY=sk-...
railway variables set CORS_ORIGINS=https://website-seven-eta-74.vercel.app
railway variables set ADMIN_API_KEY=your-secure-key
railway variables set ENVIRONMENT=production

# Check logs
railway logs
```

## Troubleshooting

### Build Fails
- Check Railway logs for errors
- Verify `requirements.txt` is correct
- Ensure Python 3.11 is specified in `nixpacks.toml`

### Database Connection Error
- Verify `DATABASE_URL` format is correct
- Check Neon database is active
- Ensure IP allowlist includes Railway IPs (or set to allow all)

### Vector Store Error
- Verify Qdrant cluster is running
- Check API key is correct
- Ensure collection exists (created during ingestion)

### CORS Error
- Add Vercel URL to `CORS_ORIGINS`
- Ensure no trailing slashes in URLs
- Redeploy after changing environment variables

## Cost Estimate

- **Railway**: $5/month (Hobby plan) or free trial
- **Qdrant**: Free tier (1GB)
- **Neon**: Free tier (0.5GB)
- **OpenAI**: Pay-per-use (~$0.01-0.10 per query)

**Total**: ~$5-10/month

## Next Steps

1. Deploy backend to Railway
2. Set up Qdrant and Neon
3. Configure environment variables
4. Run data ingestion
5. Update frontend with backend URL
6. Test end-to-end functionality
