# PythonAnywhere Deployment Guide (100% Free)

## Prerequisites
- GitHub repository: https://github.com/muhammad-rayyankhan/physical-ai-textbook
- All API keys ready (Groq, Hugging Face, Qdrant, Neon)
- No credit card required ✅

## Step 1: Create PythonAnywhere Account (2 minutes)

1. Go to: https://www.pythonanywhere.com/registration/register/beginner/
2. Sign up with email (no credit card needed)
3. Verify your email
4. Login to dashboard

## Step 2: Clone Your Repository (3 minutes)

1. **Open Bash Console**:
   - Dashboard → "Consoles" tab → "Bash"

2. **Clone your repo**:
```bash
git clone https://github.com/muhammad-rayyankhan/physical-ai-textbook.git
cd physical-ai-textbook/backend
```

3. **Verify files**:
```bash
ls -la
# Should see: src/, requirements.txt, etc.
```

## Step 3: Create Virtual Environment (3 minutes)

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 textbook-env

# Activate it (should auto-activate after creation)
workon textbook-env

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

## Step 4: Set Up Web App (5 minutes)

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Select**:
   - Domain: `yourusername.pythonanywhere.com` (free subdomain)
   - Python version: **3.10**
   - Framework: **Manual configuration**
4. **Click Next** through the prompts

## Step 5: Configure ASGI File (5 minutes)

1. **In Web tab**, find "ASGI configuration file" link
2. **Click to edit** (opens in browser editor)
3. **Replace entire content** with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/physical-ai-textbook/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['QDRANT_URL'] = 'YOUR_QDRANT_URL'
os.environ['QDRANT_API_KEY'] = 'YOUR_QDRANT_API_KEY'
os.environ['QDRANT_COLLECTION'] = 'textbook_chunks'
os.environ['DATABASE_URL'] = 'YOUR_NEON_DATABASE_URL'
os.environ['GROQ_API_KEY'] = 'YOUR_GROQ_API_KEY'
os.environ['GROQ_MODEL'] = 'llama-3.3-70b-versatile'
os.environ['HUGGINGFACE_API_KEY'] = 'YOUR_HUGGINGFACE_API_KEY'
os.environ['API_HOST'] = '0.0.0.0'
os.environ['API_PORT'] = '8000'
os.environ['CORS_ORIGINS'] = 'https://website-seven-eta-74.vercel.app,http://localhost:3000'
os.environ['AUTH_SECRET'] = 'YOUR_AUTH_SECRET'
os.environ['ENVIRONMENT'] = 'production'

# Import your FastAPI app
from src.main import app as application
```

4. **Replace `yourusername`** with your actual PythonAnywhere username
5. **Save the file** (Ctrl+S or click Save button)

## Step 6: Configure Virtual Environment Path (2 minutes)

1. **In Web tab**, scroll to "Virtualenv" section
2. **Enter path**:
```
/home/yourusername/.virtualenvs/textbook-env
```
3. **Replace `yourusername`** with your actual username

## Step 7: Reload Web App (1 minute)

1. **Scroll to top** of Web tab
2. **Click green "Reload" button**
3. **Wait** for reload to complete (~30 seconds)

## Step 8: Test Deployment (2 minutes)

1. **Visit your site**:
```
https://yourusername.pythonanywhere.com/api/health
```

2. **Should see**:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {...}
}
```

3. **Check API docs**:
```
https://yourusername.pythonanywhere.com/docs
```

## Step 9: Ingest Textbook Data (5 minutes)

1. **Open Bash Console** (or use existing one)
2. **Navigate to backend**:
```bash
cd ~/physical-ai-textbook/backend
workon textbook-env
```

3. **Run ingestion**:
```bash
python -m rag.scripts.ingest_textbook --docs-dir ../website/docs --verbose
```

4. **Wait for completion** (~2-3 minutes)
5. **Verify**:
```bash
# Should see: "48 documents stored"
```

## Step 10: Update Frontend (2 minutes)

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Add new variable**:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://yourusername.pythonanywhere.com`
3. **Save**
4. **Redeploy** (automatic)

## Step 11: Test End-to-End (2 minutes)

1. **Visit**: https://website-seven-eta-74.vercel.app
2. **Open chat widget** (bottom right)
3. **Ask**: "What is physical AI?"
4. **Verify**: You get an answer with citations

---

## 🎉 Deployment Complete!

**Your URLs:**
- Frontend: https://website-seven-eta-74.vercel.app
- Backend: https://yourusername.pythonanywhere.com
- API Docs: https://yourusername.pythonanywhere.com/docs
- Health Check: https://yourusername.pythonanywhere.com/api/health

---

## 📊 Free Tier Limits

**PythonAnywhere Free Tier:**
- ✅ Always-on (no sleep)
- ✅ 512MB RAM
- ✅ 100 seconds CPU/day
- ✅ HTTPS included
- ⚠️ Slower than paid tiers
- ⚠️ Limited to whitelisted external sites (Groq, Hugging Face, Qdrant should work)

**If you hit limits:**
- Upgrade to Hacker plan ($5/month) for more resources
- Or use multiple free accounts (not recommended)

---

## 🔧 Troubleshooting

### Error: "Could not import module"
```bash
# In bash console:
cd ~/physical-ai-textbook/backend
workon textbook-env
pip install -r requirements.txt
# Then reload web app
```

### Error: "Connection refused" to external services
- PythonAnywhere has a whitelist for external connections
- Check: https://www.pythonanywhere.com/whitelist/
- Groq, Hugging Face, Qdrant should be allowed
- If not, request whitelist addition

### Error: "502 Bad Gateway"
- Check error log in Web tab → "Error log" link
- Usually means Python error in your code
- Fix the error and reload

### Slow Response Times
- Free tier has limited CPU
- First request after idle may be slow
- Consider upgrading if needed

### Out of CPU Quota
- Free tier: 100 seconds/day
- Check usage: Dashboard → Account tab
- Resets daily at midnight UTC
- Optimize code or upgrade

---

## 🔄 Updating Your Code

When you make changes:

```bash
# In bash console:
cd ~/physical-ai-textbook
git pull origin master
cd backend
workon textbook-env
pip install -r requirements.txt  # If dependencies changed

# Then reload web app in Web tab
```

---

## 📝 Important Notes

1. **Keep your API keys secure** - They're in the ASGI file
2. **Free tier limitations** - May be slow under load
3. **Always-on** - Unlike Render, no cold starts
4. **Backup your data** - PythonAnywhere can delete inactive free accounts after 3 months
5. **Monitor usage** - Check CPU quota daily

---

## 💰 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| PythonAnywhere | Free | $0 |
| Vercel | Free | $0 |
| Qdrant Cloud | Free | $0 |
| Neon PostgreSQL | Free | $0 |
| Groq API | Free | $0 |
| Hugging Face | Free | $0 |
| **Total** | | **$0/month** |

---

## 🆘 Need Help?

- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Check error logs**: Web tab → Error log link
- **Check server logs**: Web tab → Server log link

---

**Estimated Total Time**: 30-35 minutes
**Difficulty**: Beginner-friendly
**Cost**: $0 (completely free)
