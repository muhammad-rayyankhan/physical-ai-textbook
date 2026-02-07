# 🆓 Completely Free Deployment Guide

Deploy your Physical AI textbook backend with **$0/month** cost using free tiers.

## 🎯 Free Stack Overview

| Service | Purpose | Free Tier | Cost |
|---------|---------|-----------|------|
| **Render.com** | Backend hosting | 750 hours/month | $0 |
| **Groq** | LLM (Llama 3.1 70B) | 14,400 req/day | $0 |
| **Hugging Face** | Embeddings | Unlimited (rate limited) | $0 |
| **Qdrant Cloud** | Vector database | 1GB storage | $0 |
| **Neon** | PostgreSQL | 0.5GB storage | $0 |
| **Vercel** | Frontend hosting | Unlimited | $0 |
| **Total** | | | **$0/month** |

---

## 📋 Prerequisites

You'll need to create free accounts on:
1. Render.com
2. Groq
3. Hugging Face
4. Qdrant Cloud
5. Neon
6. Vercel (already done)

---

## 🚀 Step-by-Step Deployment

### Step 1: Get API Keys (10 minutes)

#### A. Groq API Key (2 minutes)

1. Go to: https://console.groq.com
2. Sign up with Google/GitHub
3. Click "API Keys" → "Create API Key"
4. Name: `textbook-backend`
5. **Copy the key** (starts with `gsk_`)

#### B. Hugging Face API Key (2 minutes)

1. Go to: https://huggingface.co/settings/tokens
2. Sign up/login
3. Click "New token"
4. Name: `textbook-embeddings`
5. Type: Read
6. **Copy the token** (starts with `hf_`)

#### C. Qdrant Cloud (3 minutes)

1. Go to: https://cloud.qdrant.io
2. Sign up (free tier)
3. Create cluster:
   - Name: `textbook-vectors`
   - Region: Choose closest
   - Plan: Free (1GB)
4. **Copy**:
   - Cluster URL (e.g., `https://xyz.qdrant.io`)
   - API Key

#### D. Neon Database (3 minutes)

1. Go to: https://neon.tech
2. Sign up (free tier)
3. Create project:
   - Name: `textbook-db`
   - Region: Choose closest
4. **Copy connection string**:
   - Format: `postgresql://user:password@host/database`

---

### Step 2: Deploy to Render.com (5 minutes)

#### Option A: Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `muhammad-rayyankhan/physical-ai-textbook`

3. **Configure Service**
   - Name: `textbook-backend`
   - Region: Oregon (or closest)
   - Branch: `master`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

4. **Add Environment Variables**

   Click "Advanced" → Add these variables:

   ```
   QDRANT_URL=<your-qdrant-cluster-url>
   QDRANT_API_KEY=<your-qdrant-api-key>
   QDRANT_COLLECTION=textbook_chunks

   DATABASE_URL=<your-neon-connection-string>

   GROQ_API_KEY=<your-groq-api-key>
   GROQ_MODEL=llama-3.1-70b-versatile

   HUGGINGFACE_API_KEY=<your-huggingface-token>

   API_HOST=0.0.0.0
   API_PORT=$PORT
   CORS_ORIGINS=https://website-seven-eta-74.vercel.app,http://localhost:3000

   ADMIN_API_KEY=92c9bd0af304025abb39a416089d701253a152647799c0d5a877e78622b625c2
   AUTH_SECRET=b4634e2d8123f54d4418bf273afe5a57cfa05752ac1d3ab4c7fb94aced307fc1

   ENVIRONMENT=production
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Note your URL: `https://textbook-backend.onrender.com`

#### Option B: Using render.yaml (Advanced)

The repository includes `backend/render.yaml` for infrastructure-as-code deployment.

---

### Step 3: Ingest Textbook Data (3 minutes)

After deployment succeeds:

1. **Open Render Shell**
   - Go to your service dashboard
   - Click "Shell" tab
   - Run:
     ```bash
     python -m rag.scripts.ingest_textbook --clear
     ```

2. **Monitor Progress**
   - Should see: "Processing chapters..."
   - Should create: ~60-80 chunks
   - Wait for: "Ingestion complete"

---

### Step 4: Connect Frontend (3 minutes)

1. **Copy Render URL**
   - From Render dashboard: `https://textbook-backend.onrender.com`

2. **Update Vercel**
   - Go to: https://vercel.com/dashboard
   - Select your project
   - Settings → Environment Variables
   - Add:
     - Name: `NEXT_PUBLIC_API_URL`
     - Value: `https://textbook-backend.onrender.com`
     - Environment: Production
   - Save

3. **Redeploy Frontend**
   - Deployments → Latest → Redeploy

---

### Step 5: Test Everything (2 minutes)

**Backend Health:**
- Visit: `https://textbook-backend.onrender.com/api/health`
- Should return: `{"status": "healthy"}`

**API Docs:**
- Visit: `https://textbook-backend.onrender.com/docs`
- Should show FastAPI documentation

**Frontend Chat:**
1. Visit: https://website-seven-eta-74.vercel.app
2. Open any chapter
3. Click chat widget (bottom right)
4. Ask: "What is Physical AI?"
5. Should get AI response with citations

---

## ⚠️ Important Notes

### Render Free Tier Limitations

- **Sleep after 15 min inactivity**: First request after sleep takes ~30 seconds
- **750 hours/month**: Enough for moderate usage
- **No credit card required**: Truly free

**Tip**: Keep service awake with a cron job (optional):
```bash
# Use cron-job.org to ping every 14 minutes
https://textbook-backend.onrender.com/api/health
```

### Hugging Face Rate Limits

- Free tier has rate limits
- If you hit limits, requests queue automatically
- Typically not an issue for textbook chatbot usage

---

## 🔧 Troubleshooting

### Build Fails on Render

**Check logs** in Render dashboard → Logs tab

Common issues:
- Missing environment variables
- Python version mismatch
- Dependency conflicts

### Service Sleeps Too Often

Render free tier sleeps after 15 minutes of inactivity. Solutions:
1. Accept the 30-second cold start
2. Use a free uptime monitor (e.g., UptimeRobot)
3. Upgrade to paid plan ($7/month for always-on)

### Embeddings Slow

Hugging Face free tier can be slow during peak times. If this is an issue:
- Wait a few seconds for model to load
- Consider upgrading to Hugging Face Pro ($9/month)
- Or use OpenAI embeddings (~$0.10/month)

---

## 💰 Cost Comparison

| Stack | Monthly Cost |
|-------|--------------|
| **This Setup (All Free)** | $0 |
| Railway + Groq + HF | $5 |
| Railway + OpenAI | $10-15 |
| AWS/GCP | $20-50 |

---

## 📚 Documentation Links

- **Render**: https://render.com/docs
- **Groq**: https://console.groq.com/docs
- **Hugging Face**: https://huggingface.co/docs/api-inference
- **Qdrant**: https://qdrant.tech/documentation
- **Neon**: https://neon.tech/docs

---

## ✅ Deployment Checklist

- [ ] Groq API key obtained
- [ ] Hugging Face token obtained
- [ ] Qdrant cluster created
- [ ] Neon database created
- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] All environment variables configured
- [ ] Textbook data ingested
- [ ] Frontend environment variable updated
- [ ] Frontend redeployed
- [ ] Backend health check passes
- [ ] Chat widget works with AI responses

---

**Ready to deploy?** Follow the steps above and you'll have a completely free, production-ready deployment! 🎉
