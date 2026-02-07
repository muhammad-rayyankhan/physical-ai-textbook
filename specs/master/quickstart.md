# Quickstart Guide: Interactive Docusaurus Textbook

**Feature**: Interactive Docusaurus Textbook
**Date**: 2026-01-20
**Phase**: Phase 1 - Developer Setup

## Overview

This guide will help you set up the development environment and start working on the interactive textbook. The setup process takes approximately 10-15 minutes.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18+ LTS ([Download](https://nodejs.org/))
- **npm**: Version 9+ (included with Node.js)
- **Git**: For version control ([Download](https://git-scm.com/))
- **Code Editor**: VS Code recommended ([Download](https://code.visualstudio.com/))

### Verify Installation

```bash
node --version  # Should show v18.x.x or higher
npm --version   # Should show 9.x.x or higher
git --version   # Should show 2.x.x or higher
```

---

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd book
```

### 2. Install Dependencies

```bash
cd website
npm install
```

This will install:
- Docusaurus 3.x
- React 18.x
- All required plugins and dependencies

**Expected time**: 2-3 minutes

### 3. Start Development Server

```bash
npm start
```

This will:
- Start the development server on `http://localhost:3000`
- Enable hot reloading (changes appear instantly)
- Open your browser automatically

**Expected output**:
```
[INFO] Starting the development server...
[SUCCESS] Docusaurus website is running at: http://localhost:3000/
```

---

## Project Structure

```
website/
├── docs/                    # Markdown content files
│   ├── intro.md            # Introduction chapter
│   ├── chapter-01/         # Chapter 1: Foundations
│   ├── chapter-02/         # Chapter 2: Sensors & Perception
│   ├── chapter-03/         # Chapter 3: Actuation & Control
│   ├── chapter-04/         # Chapter 4: Learning & Intelligence
│   ├── chapter-05/         # Chapter 5: Integration & Systems
│   └── chapter-06/         # Chapter 6: Future & Ethics
├── src/
│   ├── components/         # Custom React components
│   ├── css/                # Custom styles
│   │   └── custom.css      # Theme customization
│   └── pages/              # Custom pages (landing, about)
├── static/
│   ├── img/                # Images and diagrams
│   └── assets/             # Other static assets
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Sidebar navigation config
├── package.json            # Dependencies
└── vercel.json             # Vercel deployment config
```

---

## Common Tasks

### Creating a New Chapter

1. Create a new directory in `docs/`:
   ```bash
   mkdir docs/chapter-07
   ```

2. Create an `index.md` file with frontmatter:
   ```markdown
   ---
   id: chapter-07
   title: Your Chapter Title
   sidebar_label: Chapter 7
   sidebar_position: 8
   description: Brief description for SEO
   keywords: [keyword1, keyword2]
   reading_time: 7
   chapter_number: 7
   ---

   # Your Chapter Title

   Your content here...
   ```

3. The chapter will automatically appear in the sidebar

### Editing Existing Content

1. Navigate to the chapter file (e.g., `docs/chapter-01/index.md`)
2. Edit the Markdown content
3. Save the file
4. Changes appear instantly in the browser (hot reload)

### Adding Images

1. Place images in `static/img/`:
   ```bash
   cp my-diagram.png website/static/img/
   ```

2. Reference in Markdown:
   ```markdown
   ![Alt text description](./img/my-diagram.png)
   ```

3. Optimize images before adding:
   - Use WebP format when possible
   - Keep file size < 100KB
   - Use descriptive alt text for accessibility

### Adding Code Examples

Use fenced code blocks with language tags:

````markdown
```python title="robot_controller.py"
class RobotController:
    def __init__(self, name):
        self.name = name
```
````

Supported languages: python, javascript, typescript, bash, json, yaml, and more.

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/chapter-name
```

### 2. Make Changes

- Edit Markdown files in `docs/`
- Add images to `static/img/`
- Customize styles in `src/css/custom.css` (if needed)

### 3. Test Locally

```bash
npm start  # Development server
npm run build  # Production build test
npm run serve  # Test production build locally
```

### 4. Commit Changes

```bash
git add .
git commit -m "Add Chapter 7: Your Chapter Title"
```

### 5. Push and Create PR

```bash
git push origin feature/chapter-name
# Create PR on GitHub
```

---

## Building for Production

### Build the Site

```bash
npm run build
```

This will:
- Generate static HTML/CSS/JS in `build/` directory
- Optimize assets for production
- Minify code for performance

**Expected time**: 30-60 seconds

### Test Production Build Locally

```bash
npm run serve
```

This serves the production build at `http://localhost:3000` for testing.

### Deployment to Vercel

Deployment is automatic when you push to the main branch:

1. Push to main branch:
   ```bash
   git push origin main
   ```

2. Vercel automatically:
   - Detects the push
   - Runs `npm run build`
   - Deploys to production
   - Provides a live URL

**Expected time**: 2-3 minutes

---

## Configuration

### Docusaurus Config (docusaurus.config.js)

Key settings you might need to modify:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',  // Site title
  tagline: 'An Interactive Textbook',        // Subtitle
  url: 'https://your-domain.vercel.app',     // Production URL
  baseUrl: '/',                              // Base path

  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      // Add navbar items here
    },
    footer: {
      // Customize footer
    },
  },
};
```

### Sidebar Config (sidebars.js)

The sidebar is auto-generated from frontmatter `sidebar_position` values. Manual configuration is optional.

### Custom Styles (src/css/custom.css)

Customize colors, fonts, and spacing using CSS variables:

```css
:root {
  --ifm-color-primary: #2e8555;  /* Primary brand color */
  --ifm-font-family-base: system-ui, -apple-system, sans-serif;
}
```

---

## Testing

### Run Unit Tests

```bash
npm test
```

### Run E2E Tests (Playwright)

```bash
npm run test:e2e
```

### Run Performance Tests (Lighthouse CI)

```bash
npm run lighthouse
```

---

## Troubleshooting

### Port 3000 Already in Use

```bash
# Kill the process using port 3000
npx kill-port 3000

# Or use a different port
npm start -- --port 3001
```

### Build Fails with "Out of Memory"

```bash
# Increase Node memory limit
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### Hot Reload Not Working

1. Stop the dev server (Ctrl+C)
2. Clear cache: `npm run clear`
3. Restart: `npm start`

### Images Not Loading

- Verify image path is correct (relative to `static/`)
- Check file extension matches (case-sensitive on Linux)
- Ensure image file exists in `static/img/`

---

## Performance Optimization

### Check Bundle Size

```bash
npm run build
npx webpack-bundle-analyzer build/webpack-stats.json
```

### Optimize Images

Use tools like:
- **ImageOptim** (Mac): https://imageoptim.com/
- **Squoosh** (Web): https://squoosh.app/
- **Sharp** (CLI): `npm install -g sharp-cli`

### Monitor Performance

```bash
# Run Lighthouse audit
npm run lighthouse

# Check load time
npm run build && npm run serve
# Open http://localhost:3000 and check DevTools Network tab
```

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start development server |
| `npm run build` | Build for production |
| `npm run serve` | Serve production build locally |
| `npm run clear` | Clear cache |
| `npm test` | Run unit tests |
| `npm run test:e2e` | Run E2E tests |
| `npm run lighthouse` | Run performance tests |
| `npm run lint` | Lint code |
| `npm run format` | Format code with Prettier |

---

## Resources

### Documentation
- [Docusaurus Docs](https://docusaurus.io/docs)
- [Markdown Guide](https://www.markdownguide.org/)
- [MDX Documentation](https://mdxjs.com/)

### Deployment
- [Vercel Deployment Guide](https://vercel.com/docs/frameworks/docusaurus)
- [Vercel CLI](https://vercel.com/docs/cli)

### Performance
- [Web Performance Best Practices](https://web.dev/performance/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)

### Testing
- [Playwright Documentation](https://playwright.dev/)
- [Jest Documentation](https://jestjs.io/)

---

## Getting Help

### Common Issues
1. Check the [Troubleshooting](#troubleshooting) section above
2. Search [Docusaurus GitHub Issues](https://github.com/facebook/docusaurus/issues)
3. Ask in [Docusaurus Discord](https://discord.gg/docusaurus)

### Project-Specific Help
- Review the [Constitution](../../.specify/memory/constitution.md) for project principles
- Check the [Feature Spec](./spec.md) for requirements
- Review the [Implementation Plan](./plan.md) for architecture decisions

---

## Next Steps

After completing the setup:

1. ✅ Verify development server is running
2. ✅ Explore the existing chapter structure
3. ✅ Read the [Data Model](./data-model.md) to understand content structure
4. ✅ Review the [API Contracts](./contracts/) for future integration
5. → Start writing chapter content or implementing features

---

## Quick Reference

### Frontmatter Template

```yaml
---
id: chapter-id
title: Full Chapter Title
sidebar_label: Short Label
sidebar_position: 1
description: SEO description (150-160 chars)
keywords: [keyword1, keyword2, keyword3]
reading_time: 7
chapter_number: 1
learning_objectives:
  - Objective 1
  - Objective 2
  - Objective 3
key_takeaways:
  - Takeaway 1
  - Takeaway 2
  - Takeaway 3
---
```

### Content Guidelines

- **Reading time**: 5-10 minutes per chapter
- **Word count**: 1000-1200 words per chapter
- **Images**: 1-2 per chapter, <100KB each
- **Code examples**: 2-3 per chapter
- **Headings**: Use H2 (##) and H3 (###) for structure
- **Paragraphs**: Keep short (3-4 sentences max)

---

**Last Updated**: 2026-01-20
**Maintainer**: Physical AI Textbook Team
