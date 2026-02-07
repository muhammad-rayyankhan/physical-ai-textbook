# Demo Materials Guide: Interactive Docusaurus Textbook

**Purpose**: Create demo video or screenshots for documentation (Task T077)

## Overview

This guide provides instructions for creating professional demo materials to showcase the Interactive Docusaurus Textbook.

---

## Option 1: Screenshots (Recommended for Quick Documentation)

### Required Screenshots

Capture the following screenshots to demonstrate all key features:

#### 1. Homepage/Introduction
- **What to capture**: Landing page with course overview
- **URL**: `https://your-site.vercel.app/`
- **Key elements**: Title, navigation, introduction content
- **Filename**: `01-homepage.png`

#### 2. Chapter View (Desktop)
- **What to capture**: Full chapter page with sidebar and TOC
- **URL**: `https://your-site.vercel.app/chapter-01`
- **Key elements**: Sidebar navigation, chapter content, table of contents
- **Filename**: `02-chapter-desktop.png`

#### 3. Mobile View
- **What to capture**: Chapter on mobile viewport
- **Device**: iPhone 12 Pro (390x844) or similar
- **Key elements**: Hamburger menu, readable text, responsive layout
- **Filename**: `03-mobile-view.png`

#### 4. Code Example with Syntax Highlighting
- **What to capture**: Chapter with code block
- **URL**: Any chapter with code examples
- **Key elements**: Syntax highlighting, copy button, line numbers
- **Filename**: `04-code-example.png`

#### 5. Navigation Features
- **What to capture**: Sidebar expanded with all chapters
- **Key elements**: Chapter list, current chapter highlighted, prev/next buttons
- **Filename**: `05-navigation.png`

#### 6. Lighthouse Performance Score
- **What to capture**: Chrome DevTools Lighthouse results
- **Key elements**: Performance score >90, all metrics
- **Filename**: `06-lighthouse-score.png`

### How to Capture Screenshots

**Using Chrome DevTools**:
1. Open the deployed site in Chrome
2. Press F12 to open DevTools
3. For mobile screenshots:
   - Press Ctrl+Shift+M to toggle device toolbar
   - Select device (iPhone 12 Pro)
4. Press Ctrl+Shift+P to open command palette
5. Type "screenshot" and select:
   - "Capture full size screenshot" (for full page)
   - "Capture screenshot" (for visible area)

**Using Browser Extensions**:
- **Awesome Screenshot**: Full page capture with annotations
- **Fireshot**: Professional screenshot tool
- **Nimbus Screenshot**: Video + screenshot capture

**Using Built-in Tools**:
- **Windows**: Win+Shift+S (Snipping Tool)
- **Mac**: Cmd+Shift+4 (Screenshot utility)

### Screenshot Specifications

- **Format**: PNG (for quality) or WebP (for size)
- **Resolution**: 1920x1080 for desktop, actual device resolution for mobile
- **File size**: <500KB per image (optimize if needed)
- **Location**: Save to `website/static/img/demo/`

---

## Option 2: Demo Video (Recommended for Comprehensive Showcase)

### Video Structure (2-3 minutes)

**Intro (15 seconds)**:
- Show homepage
- Brief overview: "Interactive textbook for Physical AI and Humanoid Robotics"

**Feature Showcase (90 seconds)**:
1. **Navigation** (20s):
   - Click through chapters using sidebar
   - Show prev/next buttons
   - Demonstrate table of contents

2. **Content Quality** (30s):
   - Scroll through a chapter
   - Highlight clear typography
   - Show images/diagrams

3. **Code Examples** (20s):
   - Show syntax highlighting
   - Demonstrate copy button
   - Show multiple language support

4. **Mobile Responsiveness** (20s):
   - Switch to mobile view (DevTools)
   - Show hamburger menu
   - Demonstrate smooth scrolling

**Performance Demo (30 seconds)**:
- Show Lighthouse audit results
- Highlight >90 performance score
- Show fast page load time

**Outro (15 seconds)**:
- Show all 6 chapters
- Display reading time <45 minutes
- End with deployed URL

### Recording Tools

**Free Options**:
- **OBS Studio**: Professional screen recording (Windows/Mac/Linux)
- **ShareX**: Screen recording with editing (Windows)
- **QuickTime**: Built-in screen recording (Mac)
- **Windows Game Bar**: Win+G (Windows 10/11)

**Paid Options**:
- **Camtasia**: Professional video editing
- **ScreenFlow**: Mac screen recording and editing
- **Loom**: Quick browser-based recording

### Video Specifications

- **Resolution**: 1920x1080 (1080p)
- **Frame rate**: 30 fps minimum
- **Format**: MP4 (H.264 codec)
- **Length**: 2-3 minutes
- **File size**: <50MB (use compression if needed)
- **Audio**: Optional voiceover or background music

### Recording Tips

1. **Preparation**:
   - Close unnecessary browser tabs
   - Clear browser cache for fresh load
   - Prepare script or outline
   - Test recording setup first

2. **During Recording**:
   - Move mouse slowly and deliberately
   - Pause briefly between actions
   - Avoid rapid scrolling
   - Keep cursor visible

3. **Post-Production**:
   - Trim unnecessary parts
   - Add text overlays for key features
   - Include captions if using voiceover
   - Export in web-friendly format

---

## Option 3: Animated GIFs (For Quick Feature Demos)

Create short GIFs to demonstrate specific features:

### GIF 1: Navigation Flow
- **Duration**: 5-10 seconds
- **Action**: Click through 3 chapters using sidebar
- **Filename**: `navigation-demo.gif`

### GIF 2: Mobile Responsiveness
- **Duration**: 5-10 seconds
- **Action**: Resize browser from desktop to mobile
- **Filename**: `responsive-demo.gif`

### GIF 3: Code Copy Feature
- **Duration**: 3-5 seconds
- **Action**: Hover over code block, click copy button
- **Filename**: `code-copy-demo.gif`

### GIF Creation Tools

- **ScreenToGif**: Free, powerful GIF recorder (Windows)
- **LICEcap**: Simple GIF recorder (Windows/Mac)
- **Gifox**: Professional GIF tool (Mac)
- **CloudApp**: Browser-based GIF creation

### GIF Specifications

- **Resolution**: 1280x720 (720p)
- **Frame rate**: 15-20 fps
- **File size**: <5MB per GIF
- **Loop**: Infinite loop
- **Optimization**: Use tools like Gifsicle or ezgif.com

---

## Documentation Integration

### Where to Use Demo Materials

1. **README.md**: Add screenshots to project README
2. **GitHub Repository**: Create `/docs/demo/` folder
3. **Deployment Guide**: Include in DEPLOYMENT.md
4. **Presentation**: Use for stakeholder demos
5. **Social Media**: Share on Twitter, LinkedIn, etc.

### Example README Section

```markdown
## Demo

### Live Site
🌐 [View Live Demo](https://your-site.vercel.app)

### Screenshots

#### Desktop View
![Desktop View](./website/static/img/demo/02-chapter-desktop.png)

#### Mobile View
![Mobile View](./website/static/img/demo/03-mobile-view.png)

#### Performance
![Lighthouse Score](./website/static/img/demo/06-lighthouse-score.png)

### Video Demo
📹 [Watch Demo Video](link-to-video)
```

---

## Checklist for T077

- [ ] Capture 6 required screenshots
- [ ] Optimize images (<500KB each)
- [ ] Save to `website/static/img/demo/`
- [ ] OR: Record 2-3 minute demo video
- [ ] OR: Create 3 animated GIFs for key features
- [ ] Update README.md with demo materials
- [ ] Upload video to YouTube/Vimeo (if applicable)
- [ ] Add demo links to DEPLOYMENT.md

---

## Quick Start (Minimal Approach)

If time is limited, capture these 3 essential screenshots:

1. **Homepage** - Shows overall design
2. **Chapter with code** - Shows content quality and syntax highlighting
3. **Lighthouse score** - Shows performance metrics

This minimal set demonstrates the core value proposition in under 5 minutes.

---

## Next Steps After Creating Demo Materials

1. Update tasks.md to mark T077 as complete
2. Share demo materials with stakeholders
3. Add to project documentation
4. Use for marketing/promotion
5. Include in deployment validation

---

**Estimated Time**:
- Screenshots only: 10-15 minutes
- Demo video: 30-45 minutes
- Animated GIFs: 15-20 minutes

**Tools Needed**: Browser, screen capture tool, image optimizer

**Output Location**: `website/static/img/demo/` or external hosting for video
