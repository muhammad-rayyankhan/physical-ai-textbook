# Ngrok Deployment Guide (100% Free, No Credit Card)

## What is Ngrok?

Ngrok creates a secure tunnel from a public URL to your local backend server. Your backend runs on your computer, and Ngrok makes it accessible from the internet.

**Pros:**
- ✅ Completely free
- ✅ No credit card required
- ✅ Works with your existing local setup
- ✅ Setup in 5 minutes
- ✅ HTTPS included

**Cons:**
- ⚠️ Your computer must stay on
- ⚠️ URL changes each time you restart ngrok (free tier)
- ⚠️ Not suitable for 24/7 production

---

## Step 1: Download Ngrok (2 minutes)

1. **Go to**: https://ngrok.com/download
2. **Sign up** (free, no credit card)
3. **Download** ngrok for Windows
4. **Extract** the zip file to a folder (e.g., `C:\ngrok\`)

---

## Step 2: Get Your Auth Token (1 minute)

1. **After signing up**, you'll see your dashboard
2. **Copy your authtoken** (looks like: `2abc...xyz`)
3. **Or go to**: https://dashboard.ngrok.com/get-started/your-authtoken

---

## Step 3: Configure Ngrok (1 minute)

Open **Command Prompt** or **PowerShell** and run:

```bash
# Navigate to ngrok folder
cd C:\ngrok

# Add your authtoken (replace with your actual token)
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

---

## Step 4: Start Your Backend (if not running)

Open a **new terminal** and run:

```bash
cd D:\book\backend
python -m src.main
```

**Verify it's running:**
- Should be on port 8003 (or 8001/8002)
- Test: http://localhost:8003/api/health

---

## Step 5: Start Ngrok Tunnel (1 minute)

Open **another terminal** and run:

```bash
cd C:\ngrok

# Create tunnel to your backend (replace 8003 with your actual port)
ngrok http 8003
```

**You'll see output like:**
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8003
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

---

## Step 6: Test Your Public URL (1 minute)

**Open in browser:**
```
https://abc123.ngrok-free.app/api/health
```

**You might see an ngrok warning page first:**
- Click "Visit Site" button
- This is normal for free tier

**Expected result:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {...}
}
```

---

## Step 7: Update Frontend (2 minutes)

1. **Go to Vercel Dashboard** → Your Project → Settings → Environment Variables
2. **Add new variable**:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://abc123.ngrok-free.app` (your ngrok URL)
3. **Save**
4. **Redeploy** (automatic)

---

## Step 8: Test End-to-End (2 minutes)

1. **Visit**: https://website-seven-eta-74.vercel.app
2. **Open chat widget** (bottom right)
3. **Ask**: "What is physical AI?"
4. **Verify**: You get an answer with citations

---

## 🎉 Deployment Complete!

**Your URLs:**
- Frontend: https://website-seven-eta-74.vercel.app
- Backend: https://abc123.ngrok-free.app (changes each restart)
- API Docs: https://abc123.ngrok-free.app/docs
- Health Check: https://abc123.ngrok-free.app/api/health

---

## 📝 Important Notes

### Keeping It Running

**You need 3 terminals open:**
1. **Terminal 1**: Backend server
   ```bash
   cd D:\book\backend
   python -m src.main
   ```

2. **Terminal 2**: Ngrok tunnel
   ```bash
   cd C:\ngrok
   ngrok http 8003
   ```

3. **Terminal 3**: For other commands (optional)

### URL Changes on Restart

**Free tier limitation:**
- URL changes every time you restart ngrok
- Example: `https://abc123.ngrok-free.app` → `https://xyz789.ngrok-free.app`

**When URL changes:**
1. Copy new ngrok URL
2. Update Vercel environment variable
3. Redeploy frontend

**To get a static URL:**
- Upgrade to ngrok paid plan ($8/month)
- Or use a different deployment method

### Ngrok Warning Page

Free tier shows a warning page before accessing your site:
- Users must click "Visit Site" button
- This is normal and expected
- Paid plans remove this warning

---

## 🔧 Troubleshooting

### Error: "ngrok not found"
```bash
# Make sure you're in the right directory
cd C:\ngrok
dir  # Should show ngrok.exe
```

### Error: "Failed to start tunnel"
```bash
# Check if your backend is running
curl http://localhost:8003/api/health

# Try a different port if 8003 is not working
ngrok http 8001
# or
ngrok http 8002
```

### Backend Not Responding
```bash
# Restart your backend
cd D:\book\backend
python -m src.main

# Check which port it's using
netstat -ano | findstr "LISTENING" | findstr "800"
```

### Ngrok Tunnel Disconnects
- Free tier has session limits
- Restart ngrok if it disconnects
- Upgrade to paid plan for stable connections

---

## 💰 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Ngrok | Free | $0 |
| Vercel | Free | $0 |
| Qdrant Cloud | Free | $0 |
| Neon PostgreSQL | Free | $0 |
| Groq API | Free | $0 |
| Hugging Face | Free | $0 |
| **Total** | | **$0/month** |

---

## 🚀 Upgrading to Static URL (Optional)

If you want a permanent URL that doesn't change:

**Ngrok Pro ($8/month):**
- Static domain (e.g., `your-app.ngrok.io`)
- No warning page
- Better performance
- More concurrent tunnels

**Alternative:**
- Wait until you can add credit card to Render/Railway
- Use a VPS (DigitalOcean, Linode) - requires more setup

---

## 📚 Useful Commands

```bash
# Start ngrok with custom subdomain (requires paid plan)
ngrok http 8003 --subdomain=my-textbook-api

# View ngrok web interface (shows requests)
# Open browser: http://localhost:4040

# Stop ngrok
# Press Ctrl+C in the ngrok terminal

# Check ngrok status
ngrok status

# View ngrok logs
ngrok logs
```

---

## 🆘 Need Help?

- **Ngrok Docs**: https://ngrok.com/docs
- **Ngrok Dashboard**: https://dashboard.ngrok.com
- **Check ngrok status**: http://localhost:4040 (when running)

---

**Estimated Setup Time**: 5-10 minutes
**Difficulty**: Beginner-friendly
**Cost**: $0 (completely free)
**Limitation**: Computer must stay on, URL changes on restart
