# 🚀 Quick Deployment Checklist

## ✅ COMPLETED (by Claude)

1. ✅ Frontend deployed to Vercel
   - URL: https://website-seven-eta-74.vercel.app

2. ✅ GitHub repository synced
   - Repo: https://github.com/muhammad-rayyankhan/physical-ai-textbook

3. ✅ Backend configured for Railway
   - Procfile, railway.json, nixpacks.toml created

4. ✅ Documentation created
   - DEPLOYMENT-STATUS.md
   - RAILWAY-DEPLOYMENT.md

---

## 🎯 YOUR NEXT STEPS (25 minutes)

### Step 1: Deploy Backend (5 min)
```
1. Open: https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub
4. Select: muhammad-rayyankhan/physical-ai-textbook
5. Root Directory: backend
6. Deploy
```

### Step 2: Setup Services (10 min)

**Qdrant (Vector DB)**
- Go to: https://cloud.qdrant.io
- Sign up → Create cluster
- Copy: URL + API Key

**Neon (PostgreSQL)**
- Go to: https://neon.tech
- Sign up → Create project
- Copy: Connection string

**OpenAI**
- Go to: https://platform.openai.com/api-keys
- Create key
- Copy: API key (sk-...)

### Step 3: Add Environment Variables (5 min)

In Railway Dashboard → Variables, paste:

```env
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-qdrant-key>
QDRANT_COLLECTION=textbook_chunks
DATABASE_URL=<your-neon-connection-string>
OPENAI_API_KEY=<your-openai-key>
API_HOST=0.0.0.0
API_PORT=$PORT
CORS_ORIGINS=https://website-seven-eta-74.vercel.app
ADMIN_API_KEY=<random-32-char-string>
ENVIRONMENT=production
```

### Step 4: Ingest Data (2 min)

Railway Dashboard → Settings → One-off Commands:
```bash
python -m rag.scripts.ingest_textbook --clear
```

### Step 5: Connect Frontend (2 min)

Vercel Dashboard → Environment Variables:
```
NEXT_PUBLIC_API_URL=<your-railway-url>
```
Then redeploy.

### Step 6: Test (1 min)

1. Visit: `<your-railway-url>/api/health`
2. Visit: https://website-seven-eta-74.vercel.app
3. Ask chatbot: "What is Physical AI?"

---

## 📱 Quick Commands (Alternative CLI Method)

```bash
cd D:\book\backend
railway login
railway init
railway up
railway variables set QDRANT_URL=...
railway variables set QDRANT_API_KEY=...
railway variables set DATABASE_URL=...
railway variables set OPENAI_API_KEY=...
railway variables set CORS_ORIGINS=https://website-seven-eta-74.vercel.app
railway variables set ADMIN_API_KEY=$(openssl rand -hex 32)
railway variables set ENVIRONMENT=production
railway run python -m rag.scripts.ingest_textbook --clear
```

---

## 💰 Cost: ~$6-10/month
## ⏱️ Time: ~25 minutes

**Start here**: https://railway.app
