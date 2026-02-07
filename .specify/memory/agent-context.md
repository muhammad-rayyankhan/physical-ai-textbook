# Physical AI Textbook Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-21

## Active Technologies

### Frontend Framework
- **Docusaurus 3.x**: Static site generator for documentation and content-heavy sites
- **React 18.x**: UI library (required by Docusaurus)
- **MDX**: Markdown with JSX support for interactive components

### Runtime & Build Tools
- **Node.js 18+ LTS**: JavaScript runtime
- **npm 9+**: Package manager
- **Webpack**: Module bundler (built into Docusaurus)

### Styling
- **CSS Variables**: Theme customization via Docusaurus
- **CSS Modules**: Component-specific styles

### Testing
- **Jest**: Unit testing framework
- **Playwright**: End-to-end testing (cross-browser)
- **Lighthouse CI**: Performance testing and regression detection

### Deployment
- **Vercel**: Static site hosting and deployment
- **Git**: Version control

### Future Technologies (Planned)
- **FastAPI**: Backend framework (RAG/Auth features)
- **Better-Auth**: Authentication system
- **Qdrant**: Vector database for RAG
- **Neon**: PostgreSQL database
- **Railway**: Backend deployment platform

## Project Structure

```text
book/
├── .specify/
│   ├── memory/
│   │   ├── constitution.md      # Project principles
│   │   └── agent-context.md     # This file
│   ├── templates/               # SDD templates
│   └── scripts/                 # Automation scripts
├── specs/
│   └── master/                  # Current feature (Docusaurus textbook)
│       ├── spec.md              # Feature specification
│       ├── plan.md              # Implementation plan
│       ├── research.md          # Technology research
│       ├── data-model.md        # Content structure
│       ├── quickstart.md        # Developer setup guide
│       └── contracts/           # API contracts (future)
├── history/
│   ├── prompts/                 # Prompt History Records
│   └── adr/                     # Architecture Decision Records
├── website/                     # Docusaurus site (to be created)
│   ├── docs/                    # Markdown content
│   ├── src/                     # Custom components
│   ├── static/                  # Images and assets
│   ├── docusaurus.config.js    # Configuration
│   ├── sidebars.js             # Navigation config
│   └── package.json            # Dependencies
├── backend/                     # Backend services (future)
├── CLAUDE.md                    # Agent instructions
└── README.md                    # Project overview
```

## Commands

### Development
```bash
# Navigate to website directory
cd website

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve

# Clear cache
npm run clear
```

### Testing
```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e

# Run performance tests
npm run lighthouse
```

### Deployment
```bash
# Deploy to Vercel (automatic on git push to main)
git push origin main

# Manual deployment with Vercel CLI
vercel deploy
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/chapter-name

# Commit changes
git add .
git commit -m "Add Chapter X: Title"

# Push and create PR
git push origin feature/chapter-name
```

## Code Style

### Markdown/MDX
- Use frontmatter for all pages (id, title, sidebar_label, etc.)
- Keep paragraphs short (3-4 sentences max)
- Use H2 (##) and H3 (###) for structure (H1 is auto-generated)
- Add alt text to all images
- Use language tags for code blocks (```python, ```javascript, etc.)
- Keep reading time to 5-10 minutes per chapter

### JavaScript/React (Custom Components)
- Use functional components with hooks
- Follow Docusaurus component conventions
- Keep components simple and focused
- Use CSS modules for styling
- Avoid heavy client-side libraries

### CSS
- Use CSS variables for theming
- Follow mobile-first approach
- Maintain WCAG AA color contrast (4.5:1)
- Avoid inline styles

### File Naming
- Chapters: `chapter-01/index.md`, `chapter-02/index.md`
- Images: `kebab-case.webp` or `kebab-case.png`
- Components: `PascalCase.jsx`
- Styles: `kebab-case.module.css`

## Performance Budgets

### Content
- Per chapter: 1000-1200 words (7-8 min reading)
- Total textbook: 7000-8500 words (45 min reading)
- Images per chapter: 1-2 max
- Code examples per chapter: 2-3 max

### Bundle Size
- Initial JavaScript: <200KB (gzipped)
- Images: <100KB each (WebP optimized)
- Per chapter: ~5-10KB added to bundle

### Load Time
- Initial page load: <3s (3G connection)
- Time to Interactive (TTI): <200ms
- First Contentful Paint (FCP): <1.5s
- Lighthouse score: >90 (all categories)

## Recent Changes

### Feature 1: Interactive Docusaurus Textbook (Current)
**Status**: Phase 1 Complete (Design & Contracts)
**Added**:
- Docusaurus 3.x as static site generator
- 6-chapter content structure
- Performance optimization strategy (<3s load time)
- Testing strategy (Jest, Playwright, Lighthouse CI)
- API contracts for future backend integration
- Vercel deployment configuration

**Key Decisions**:
- Chose Docusaurus over Next.js for simplicity and built-in features
- Node.js 18+ LTS for compatibility
- Static generation for performance
- Mobile-first responsive design
- Aggressive performance optimization for low-end devices

**Next Steps**:
- Phase 2: Generate tasks.md with implementation steps
- Implement Docusaurus site structure
- Write chapter content
- Deploy to Vercel

<!-- MANUAL ADDITIONS START -->
<!-- Add any manual context or notes here -->
<!-- MANUAL ADDITIONS END -->
