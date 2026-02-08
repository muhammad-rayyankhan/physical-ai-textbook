# Hugging Face Spaces Deployment (100% Free, No Credit Card)

## Why Hugging Face Spaces?

- ✅ Completely free forever
- ✅ No credit card required
- ✅ Native FastAPI support
- ✅ Perfect for AI/ML applications
- ✅ Deploy from GitHub
- ✅ Always-on, no cold starts
- ✅ 16GB RAM, 8 CPU cores (free tier)

---

## Step 1: Create Hugging Face Account (2 minutes)

1. Go to: https://huggingface.co/join
2. Sign up with email (no credit card needed)
3. Verify your email
4. Login to dashboard

---

## Step 2: Create a New Space (3 minutes)

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `physical-ai-textbook-backend`
   - **License**: MIT
   - **Select SDK**: **Docker** (important!)
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public
3. Click **"Create Space"**

---

## Step 3: Prepare Deployment Files (5 minutes)

We need to create a few files for Hugging Face Spaces.

### A. Create `Dockerfile`

In `D:\book\backend\`, create a file named `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### B. Create `.env` file for Hugging Face

In `D:\book\backend\`, create `.env`:

```env
QDRANT_URL=<your-qdrant-cluster-url>
QDRANT_API_KEY=<your-qdrant-api-key>
QDRANT_COLLECTION=textbook_chunks
DATABASE_URL=<your-neon-postgres-connection-string>
GROQ_API_KEY=<your-groq-api-key>
GROQ_MODEL=llama-3.3-70b-versatile
HUGGINGFACE_API_KEY=<your-huggingface-api-key>
API_HOST=0.0.0.0
API_PORT=7860
CORS_ORIGINS=https://website-seven-eta-74.vercel.app,http://localhost:3000
AUTH_SECRET=<generate-random-secret>
ENVIRONMENT=production
USE_OPENAI_EMBEDDINGS=false
USE_OPENAI_LLM=false
```

### C. Create `README.md` for the Space

In `D:\book\backend\`, create `README.md`:

```markdown
---
title: Physical AI Textbook Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Physical AI & Humanoid Robotics Textbook - Backend API

RAG-powered chatbot backend for the Physical AI textbook.

## Features
- FastAPI backend
- Qdrant vector database
- Groq LLM integration
- PostgreSQL for user data

## API Endpoints
- `/api/health` - Health check
- `/docs` - Interactive API documentation
- `/api/chat/query` - Chat endpoint
```

---

## Step 4: Push to Hugging Face (5 minutes)

### Option A: Using Git (Recommended)

```bash
cd D:\book\backend

# Add Hugging Face Space as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/physical-ai-textbook-backend

# Push to Hugging Face
git add Dockerfile README.md .env
git commit -m "Deploy to Hugging Face Spaces"
git push hf master:main
```

### Option B: Using Hugging Face Web Interface

1. Go to your Space page
2. Click **"Files"** tab
3. Click **"Add file"** → **"Upload files"**
4. Upload:
   - `Dockerfile`
   - `README.md`
   - `.env`
   - All files from `backend/` folder
5. Click **"Commit changes to main"**

---

## Step 5: Configure Environment Variables (3 minutes)

1. In your Space page, click **"Settings"** tab
2. Scroll to **"Repository secrets"**
3. Add each variable from your `.env` file:
   - Click **"New secret"**
   - Name: `QDRANT_URL`, Value: `https://0e07f4f7...`
   - Repeat for all variables

**Important**: Use secrets for sensitive data instead of committing `.env`

---

## Step 6: Wait for Build (5-10 minutes)

1. Go to **"App"** tab in your Space
2. You'll see build logs
3. Wait for "Running on http://0.0.0.0:7860"
4. Space will automatically be live

---

## Step 7: Test Your Deployment (2 minutes)

Your backend will be at:
```
https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space
```

Test endpoints:
- Health: `https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space/api/health`
- Docs: `https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space/docs`

---

## Step 8: Ingest Data (5 minutes)

You need to run the ingestion script once. Two options:

### Option A: Add to Dockerfile (Automatic)

Update your `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run ingestion on startup (only once)
RUN python -m rag.scripts.ingest_textbook --docs-dir ../website/docs || true

EXPOSE 7860

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Option B: Manual via API

Create an admin endpoint to trigger ingestion (safer).

---

## Step 9: Update Frontend (2 minutes)

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update `NEXT_PUBLIC_API_URL`:
   ```
   https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space
   ```
3. Redeploy

---

## Step 10: Test End-to-End (2 minutes)

1. Visit: https://website-seven-eta-74.vercel.app
2. Open chat widget
3. Ask: "What is physical AI?"
4. Verify you get an answer with citations

---

## 🎉 Deployment Complete!

**Your URLs:**
- Frontend: https://website-seven-eta-74.vercel.app
- Backend: https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space
- API Docs: https://YOUR_USERNAME-physical-ai-textbook-backend.hf.space/docs

---

## 📊 Free Tier Limits

**Hugging Face Spaces Free Tier:**
- ✅ 16GB RAM
- ✅ 8 CPU cores
- ✅ 50GB storage
- ✅ Always-on
- ✅ No time limits
- ✅ HTTPS included
- ⚠️ Public by default (can't make private on free tier)

---

## 🔄 Updating Your Code

```bash
cd D:\book\backend
git add .
git commit -m "Update backend"
git push hf master:main
```

Space will automatically rebuild.

---

## 🔧 Troubleshooting

### Build fails
- Check build logs in "App" tab
- Verify Dockerfile syntax
- Ensure all dependencies in requirements.txt

### App crashes
- Check logs in "App" tab
- Verify environment variables are set
- Test locally first: `docker build -t test . && docker run -p 7860:7860 test`

### Slow performance
- Free tier has limited resources
- Consider upgrading to paid tier if needed
- Optimize your code

---

## 💰 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Hugging Face Spaces | Free | $0 |
| Vercel | Free | $0 |
| Qdrant Cloud | Free | $0 |
| Neon PostgreSQL | Free | $0 |
| Groq API | Free | $0 |
| **Total** | | **$0/month** |

---

## 📝 Important Notes

1. **Public by default** - Your Space is public (code visible)
2. **Use secrets** - Don't commit API keys in code
3. **Always-on** - No cold starts unlike some platforms
4. **Community support** - Great for educational projects
5. **Docker-based** - Full control over environment

---

**Estimated Total Time**: 30-40 minutes
**Difficulty**: Beginner-friendly
**Cost**: $0 (completely free)
