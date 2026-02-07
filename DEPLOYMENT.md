# Deployment Guide: Physical AI Textbook

## Prerequisites

- GitHub repository with the textbook code
- Vercel account (free tier is sufficient)
- Git installed locally

## Step 1: Prepare Repository

Ensure your repository is up to date:

```bash
# Check git status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Complete textbook implementation with all 6 chapters"

# Push to GitHub
git push origin master
```

## Step 2: Connect to Vercel

### Option A: Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository
4. Vercel will auto-detect Docusaurus configuration
5. Click "Deploy"

### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from website directory
cd website
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No
# - Project name? physical-ai-textbook (or your choice)
# - Directory? ./ (current directory)
# - Override settings? No

# For production deployment
vercel --prod
```

## Step 3: Verify Deployment

After deployment completes:

1. **Check the live URL**: Vercel will provide a URL like `https://your-project.vercel.app`
2. **Test all chapters**: Navigate through all 6 chapters
3. **Test mobile responsiveness**: Open on mobile device or use browser DevTools
4. **Verify performance**: Check page load times
5. **Test navigation**: Ensure sidebar, TOC, and prev/next buttons work

## Step 4: Configure Custom Domain (Optional)

If you have a custom domain:

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed by Vercel
4. Wait for DNS propagation (can take up to 48 hours)

## Step 5: Enable Automatic Deployments

Vercel automatically deploys on every push to your main branch:

- **Production**: Pushes to `master` or `main` branch
- **Preview**: Pull requests get preview URLs
- **Rollback**: Easy rollback to previous deployments in Vercel Dashboard

## Deployment Configuration

The project includes `website/vercel.json` with optimal settings:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "installCommand": "npm install",
  "framework": "docusaurus",
  "devCommand": "npm start"
}
```

## Performance Checklist

After deployment, verify:

- [ ] Page load time < 3 seconds
- [ ] All chapters accessible
- [ ] Navigation works smoothly
- [ ] Code syntax highlighting displays correctly
- [ ] Images load properly
- [ ] Mobile responsiveness works
- [ ] Dark mode toggle works
- [ ] Search functionality works (if enabled)

## Troubleshooting

### Build Fails

```bash
# Test build locally first
cd website
npm run build

# Check for errors
npm run serve
```

### Environment Variables

If you need environment variables:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add variables for Production, Preview, or Development
3. Redeploy to apply changes

### Custom Build Settings

If you need to override build settings:

1. Go to Vercel Dashboard → Your Project → Settings → General
2. Modify Build & Development Settings
3. Save and redeploy

## Monitoring

### Vercel Analytics (Optional)

Enable analytics to track:
- Page views
- Performance metrics
- User demographics
- Traffic sources

### Performance Monitoring

Use Lighthouse CI for continuous monitoring:

```bash
# Install Lighthouse CI
npm install -g @lhci/cli

# Run audit
lhci autorun --collect.url=https://your-project.vercel.app
```

## Rollback

If you need to rollback to a previous version:

1. Go to Vercel Dashboard → Your Project → Deployments
2. Find the previous working deployment
3. Click "..." → "Promote to Production"

## Support

- **Vercel Documentation**: https://vercel.com/docs
- **Docusaurus Deployment**: https://docusaurus.io/docs/deployment
- **GitHub Issues**: Report issues in your repository

---

## Quick Deploy Commands

```bash
# One-time setup
npm install -g vercel
vercel login

# Deploy to production
cd website
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs
```

---

**Estimated Deployment Time**: 2-3 minutes
**Cost**: Free (Vercel free tier)
**Maintenance**: Automatic deployments on git push
