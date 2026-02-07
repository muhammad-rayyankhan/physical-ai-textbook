# Research: Interactive Docusaurus Textbook

**Feature**: Interactive Docusaurus Textbook
**Date**: 2026-01-20
**Phase**: Phase 0 - Technology Research & Decisions

## Overview

This document captures the research findings, technology decisions, and best practices for building the interactive textbook using Docusaurus. All decisions align with the constitution's principles of simplicity, performance, and maintainability.

---

## Decision 1: Static Site Generator Selection

### Decision
Use **Docusaurus 3.x** as the static site generator for the textbook.

### Rationale
1. **Purpose-built for documentation**: Docusaurus is specifically designed for content-heavy sites like textbooks
2. **Performance**: Static site generation ensures fast load times (<3s requirement)
3. **Developer experience**: Markdown/MDX authoring is simple and maintainable
4. **Built-in features**: Search, navigation, mobile responsiveness out-of-the-box
5. **React ecosystem**: Allows custom components when needed for interactive elements
6. **Vercel compatibility**: Excellent deployment support with zero configuration

### Alternatives Considered
- **Next.js**: More complex, requires custom routing and navigation logic
  - Rejected: Over-engineered for a content-focused site
- **VitePress**: Lighter weight but less feature-complete
  - Rejected: Smaller ecosystem, fewer plugins for future features
- **Custom React app**: Maximum flexibility
  - Rejected: Violates "avoid complexity" principle, would require building navigation, search, etc.
- **Jekyll/Hugo**: Simpler static generators
  - Rejected: No React support for future interactive features (quizzes, chatbot integration)

### Best Practices
1. Use Docusaurus 3.x (latest stable) for modern features and performance
2. Leverage MDX for interactive components within Markdown
3. Use static site generation (SSG) mode, not server-side rendering
4. Implement code splitting for optimal bundle sizes
5. Use Docusaurus plugins sparingly to avoid bloat

---

## Decision 2: Node.js Version & Package Management

### Decision
Use **Node.js 18+ LTS** with **npm** (default package manager).

### Rationale
1. **Compatibility**: Docusaurus 3.x requires Node.js 18+
2. **LTS support**: Node 18 is Long-Term Support, stable and secure
3. **Vercel support**: Vercel fully supports Node 18+ deployments
4. **Simplicity**: npm is included with Node, no additional tooling needed

### Alternatives Considered
- **Node.js 20+**: Newer but not required by Docusaurus
  - Accepted: Can use 20+ if available, 18+ is minimum
- **pnpm/yarn**: Alternative package managers
  - Rejected: npm is sufficient, avoids additional tooling complexity

### Best Practices
1. Lock Node version in `.nvmrc` and `package.json` engines field
2. Use `package-lock.json` for reproducible builds
3. Set `engines` field in package.json to enforce Node 18+
4. Use npm ci in CI/CD for faster, deterministic installs

---

## Decision 3: Content Structure & Organization

### Decision
Organize content into **6 focused chapters** with clear hierarchy and navigation.

### Rationale
1. **Reading time constraint**: 6 chapters allows <45 minute total reading time
2. **Cognitive load**: Shorter chapters improve comprehension and retention
3. **Mobile-friendly**: Smaller chunks work better on mobile devices
4. **Modular**: Each chapter can be updated independently

### Chapter Structure
1. **Introduction**: Course overview, prerequisites, learning objectives (5 min)
2. **Chapter 1 - Foundations**: Physical AI basics, history, key concepts (7 min)
3. **Chapter 2 - Sensors & Perception**: Sensor types, data processing, computer vision (7 min)
4. **Chapter 3 - Actuation & Control**: Motors, servos, control systems (7 min)
5. **Chapter 4 - Learning & Intelligence**: ML basics, reinforcement learning, neural networks (8 min)
6. **Chapter 5 - Integration & Systems**: Putting it together, real-world systems (7 min)
7. **Chapter 6 - Future & Ethics**: Emerging trends, ethical considerations (6 min)

### Best Practices
1. Each chapter: 1000-1200 words (7-8 min reading time)
2. Use clear headings (H2, H3) for scanability
3. Include code examples with syntax highlighting
4. Add diagrams/images for visual concepts (1-2 per chapter)
5. End each chapter with key takeaways (3-5 bullet points)
6. Use consistent formatting across all chapters

---

## Decision 4: Performance Optimization Strategy

### Decision
Implement **aggressive performance optimization** to meet <3s load time requirement.

### Rationale
1. **Constitution requirement**: Must support low-end devices
2. **User experience**: Fast loading improves engagement and completion rates
3. **Mobile users**: Many learners will access on phones with slower connections
4. **SEO benefits**: Performance impacts search rankings

### Optimization Techniques
1. **Static generation**: Pre-render all pages at build time
2. **Code splitting**: Lazy load non-critical components
3. **Image optimization**: Use WebP format, lazy loading, responsive images
4. **Minimal JavaScript**: Avoid heavy client-side libraries
5. **CSS optimization**: Inline critical CSS, defer non-critical styles
6. **CDN delivery**: Leverage Vercel's global CDN
7. **Prefetching**: Docusaurus prefetches linked pages on hover

### Performance Budgets
- Initial load: <3s on 3G connection
- Time to Interactive (TTI): <200ms
- First Contentful Paint (FCP): <1.5s
- Lighthouse score: >90 (all categories)
- Bundle size: <200KB initial JavaScript
- Images: <100KB per image (optimized)

### Best Practices
1. Use Lighthouse CI in testing pipeline
2. Monitor bundle size with webpack-bundle-analyzer
3. Optimize images before committing (use tools like ImageOptim)
4. Avoid importing large libraries (moment.js, lodash, etc.)
5. Use Docusaurus's built-in optimizations (don't override)

---

## Decision 5: Testing Strategy

### Decision
Implement **three-tier testing**: unit tests (Jest), E2E tests (Playwright), and performance tests (Lighthouse CI).

### Rationale
1. **Quality assurance**: Catch bugs before deployment
2. **Performance monitoring**: Ensure load time requirements are met
3. **Mobile compatibility**: Verify responsive design works
4. **Regression prevention**: Automated tests prevent breaking changes

### Testing Layers

#### 1. Unit Tests (Jest)
- Test custom React components
- Test utility functions
- Test configuration logic
- Coverage target: >80% for custom code

#### 2. E2E Tests (Playwright)
- Test navigation between chapters
- Test mobile responsiveness (viewport testing)
- Test search functionality
- Test code example rendering
- Run on Chrome, Firefox, Safari

#### 3. Performance Tests (Lighthouse CI)
- Run on every PR
- Fail if performance score <90
- Monitor bundle size changes
- Track load time metrics

### Best Practices
1. Run tests in CI/CD pipeline (GitHub Actions)
2. Use Playwright's mobile emulation for responsive testing
3. Set up Lighthouse CI budgets for performance regression detection
4. Test on real devices when possible (not just emulators)
5. Keep tests fast (<5 min total execution time)

---

## Decision 6: Deployment Strategy

### Decision
Deploy to **Vercel** with automatic deployments on git push.

### Rationale
1. **Constitution requirement**: Vercel specified for frontend deployment
2. **Zero configuration**: Vercel auto-detects Docusaurus projects
3. **Free tier**: Sufficient for educational project
4. **Performance**: Global CDN, edge caching, automatic HTTPS
5. **Preview deployments**: Every PR gets a preview URL
6. **Analytics**: Built-in web analytics (optional)

### Deployment Configuration
- **Build command**: `npm run build`
- **Output directory**: `website/build`
- **Node version**: 18.x (specified in package.json)
- **Environment variables**: None required for static site
- **Custom domain**: Can be added later

### Best Practices
1. Use `vercel.json` for configuration (if needed)
2. Enable automatic deployments from main branch
3. Use preview deployments for PR reviews
4. Set up deployment notifications (Slack/Discord)
5. Monitor deployment logs for build errors
6. Use Vercel Analytics for performance monitoring (optional)

---

## Decision 7: Styling & Theming Approach

### Decision
Use **Docusaurus's built-in theming system** with minimal custom CSS.

### Rationale
1. **Simplicity**: Avoid CSS framework complexity (Tailwind, Bootstrap, etc.)
2. **Consistency**: Docusaurus theme is battle-tested and accessible
3. **Maintainability**: Less custom code to maintain
4. **Performance**: No additional CSS framework overhead
5. **Customization**: Can override CSS variables for branding

### Styling Strategy
1. Use Docusaurus CSS variables for colors, fonts, spacing
2. Add custom CSS only when necessary (in `src/css/custom.css`)
3. Use CSS modules for component-specific styles
4. Avoid inline styles (use classes)
5. Keep mobile-first approach (Docusaurus default)

### Theme Customization
- **Primary color**: Define brand color in CSS variables
- **Font**: Use system fonts for performance (no web fonts initially)
- **Dark mode**: Leverage Docusaurus's built-in dark mode
- **Layout**: Use default layout, customize only if needed

### Best Practices
1. Use CSS variables for theming (easy to change)
2. Test dark mode thoroughly
3. Ensure sufficient color contrast (WCAG AA compliance)
4. Use semantic HTML for accessibility
5. Avoid CSS-in-JS libraries (adds bundle size)

---

## Decision 8: Content Authoring Workflow

### Decision
Use **Markdown with MDX** for all content, stored in version control.

### Rationale
1. **Simplicity**: Markdown is easy to write and read
2. **Version control**: Git tracks all content changes
3. **Collaboration**: Easy for multiple authors to contribute
4. **Extensibility**: MDX allows React components when needed
5. **Portability**: Markdown can be exported to other formats

### Content Guidelines
1. Write in clear, accessible language (avoid jargon)
2. Use active voice and short sentences
3. Include code examples with language tags for syntax highlighting
4. Add alt text to all images for accessibility
5. Use consistent heading hierarchy (H1 → H2 → H3)
6. Keep paragraphs short (3-4 sentences max)

### MDX Usage
- Use MDX for interactive elements (future: quizzes, demos)
- Import custom components sparingly
- Keep MDX syntax simple (avoid complex JavaScript)
- Test MDX rendering locally before committing

### Best Practices
1. Use a Markdown linter (markdownlint) in CI
2. Spell-check content before committing
3. Review content for reading level (aim for grade 10-12)
4. Use consistent terminology throughout
5. Add frontmatter metadata to each page (title, description, keywords)

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Framework | Docusaurus | 3.x | Purpose-built for documentation, excellent performance |
| Runtime | Node.js | 18+ LTS | Required by Docusaurus, stable and supported |
| UI Library | React | 18.x | Required by Docusaurus, enables interactive components |
| Content Format | Markdown/MDX | - | Simple authoring, version-controllable, extensible |
| Styling | CSS Variables | - | Simple, performant, maintainable |
| Testing (Unit) | Jest | Latest | Standard React testing, built into Docusaurus |
| Testing (E2E) | Playwright | Latest | Cross-browser, mobile testing, reliable |
| Testing (Perf) | Lighthouse CI | Latest | Performance regression detection |
| Deployment | Vercel | - | Zero-config, fast CDN, free tier |
| Package Manager | npm | 9+ | Included with Node, simple, reliable |

---

## Risk Mitigation

### Risk 1: Content Creation Time
- **Mitigation**: Start with chapter outlines, expand iteratively
- **Fallback**: Use AI assistance for initial drafts (human review required)

### Risk 2: Performance on Low-End Devices
- **Mitigation**: Aggressive optimization, performance budgets, real device testing
- **Fallback**: Provide text-only fallback mode if needed

### Risk 3: Mobile Usability Issues
- **Mitigation**: Mobile-first design, responsive testing, real device testing
- **Fallback**: Docusaurus mobile support is excellent by default

### Risk 4: Deployment Issues
- **Mitigation**: Test deployments early, use preview deployments
- **Fallback**: Vercel support is excellent, fallback to Netlify if needed

---

## Next Steps (Phase 1)

1. ✅ Research complete - all technology decisions documented
2. → Generate `data-model.md` (content structure, metadata schema)
3. → Generate `contracts/` (API contracts for future backend integration)
4. → Generate `quickstart.md` (developer setup guide)
5. → Re-evaluate Constitution Check post-design

---

## References

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [Docusaurus Performance Best Practices](https://docusaurus.io/docs/advanced/performance)
- [Vercel Deployment Guide](https://vercel.com/docs/frameworks/docusaurus)
- [MDX Documentation](https://mdxjs.com/)
- [Playwright Testing](https://playwright.dev/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Web Performance Budgets](https://web.dev/performance-budgets-101/)
