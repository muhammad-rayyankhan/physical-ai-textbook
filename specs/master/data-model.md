# Data Model: Interactive Docusaurus Textbook

**Feature**: Interactive Docusaurus Textbook
**Date**: 2026-01-20
**Phase**: Phase 1 - Data Model & Structure

## Overview

This document defines the data structures, content schema, and metadata for the interactive textbook. Since this is a static site, the "data model" focuses on content structure, frontmatter schemas, and navigation configuration rather than database entities.

---

## Content Structure

### Chapter Hierarchy

```
Textbook
├── Introduction (intro.md)
├── Chapter 1: Foundations (chapter-01/)
│   ├── index.md (chapter overview)
│   ├── history.md (optional subsection)
│   └── key-concepts.md (optional subsection)
├── Chapter 2: Sensors & Perception (chapter-02/)
│   └── index.md
├── Chapter 3: Actuation & Control (chapter-03/)
│   └── index.md
├── Chapter 4: Learning & Intelligence (chapter-04/)
│   └── index.md
├── Chapter 5: Integration & Systems (chapter-05/)
│   └── index.md
└── Chapter 6: Future & Ethics (chapter-06/)
    └── index.md
```

**Design Rationale**:
- Flat structure (1-2 levels max) for simplicity
- Each chapter is self-contained
- Optional subsections for longer chapters
- Total: 6-8 pages (meets <45 min reading time)

---

## Frontmatter Schema

### Page Metadata (All Pages)

```yaml
---
id: string                    # Unique identifier (e.g., "intro", "chapter-01")
title: string                 # Page title (e.g., "Introduction to Physical AI")
sidebar_label: string         # Short label for sidebar (e.g., "Intro")
sidebar_position: number      # Order in sidebar (1, 2, 3...)
description: string           # SEO description (150-160 chars)
keywords: string[]            # SEO keywords
reading_time: number          # Estimated reading time in minutes
---
```

**Example**:
```yaml
---
id: intro
title: Introduction to Physical AI and Humanoid Robotics
sidebar_label: Introduction
sidebar_position: 1
description: Learn the fundamentals of Physical AI and Humanoid Robotics in this interactive textbook
keywords: [physical ai, humanoid robotics, robotics course, ai education]
reading_time: 5
---
```

### Chapter Metadata (Extended)

For chapter index pages, add additional metadata:

```yaml
---
# ... base metadata above ...
chapter_number: number        # Chapter number (1-6)
learning_objectives: string[] # List of learning objectives
key_takeaways: string[]       # Summary points (3-5 items)
prerequisites: string[]       # Required knowledge (optional)
---
```

**Example**:
```yaml
---
id: chapter-01
title: Foundations of Physical AI
sidebar_label: Chapter 1
sidebar_position: 2
description: Explore the history, key concepts, and foundational principles of Physical AI
keywords: [physical ai, robotics history, ai fundamentals]
reading_time: 7
chapter_number: 1
learning_objectives:
  - Understand the definition and scope of Physical AI
  - Learn the historical evolution of robotics and AI
  - Identify key concepts and terminology
key_takeaways:
  - Physical AI combines embodied systems with intelligent algorithms
  - The field has evolved from industrial automation to humanoid robotics
  - Key concepts include sensing, actuation, and learning
prerequisites:
  - Basic understanding of computer science
  - Familiarity with programming concepts
---
```

---

## Navigation Configuration

### Sidebar Structure (sidebars.js)

```javascript
module.exports = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'chapter-01/index',
        'chapter-02/index',
        'chapter-03/index',
        'chapter-04/index',
        'chapter-05/index',
        'chapter-06/index',
      ],
    },
  ],
};
```

**Design Rationale**:
- Simple linear navigation (no nested categories)
- Auto-generated from frontmatter `sidebar_position`
- Collapsible category for chapters
- Introduction separate from chapters

---

## Content Entities

### 1. Chapter

**Attributes**:
- `id`: Unique identifier (string)
- `number`: Chapter number (1-6)
- `title`: Full chapter title (string)
- `description`: Brief description (string, 150-160 chars)
- `reading_time`: Estimated minutes (number)
- `learning_objectives`: List of objectives (string[])
- `key_takeaways`: Summary points (string[], 3-5 items)
- `prerequisites`: Required knowledge (string[], optional)

**Validation Rules**:
- `id` must be unique across all pages
- `number` must be 1-6
- `title` must be 10-100 characters
- `description` must be 150-160 characters (SEO optimal)
- `reading_time` must be 5-10 minutes per chapter
- `learning_objectives` must have 3-5 items
- `key_takeaways` must have 3-5 items

**Example**:
```json
{
  "id": "chapter-01",
  "number": 1,
  "title": "Foundations of Physical AI",
  "description": "Explore the history, key concepts, and foundational principles of Physical AI and humanoid robotics",
  "reading_time": 7,
  "learning_objectives": [
    "Understand the definition and scope of Physical AI",
    "Learn the historical evolution of robotics and AI",
    "Identify key concepts and terminology"
  ],
  "key_takeaways": [
    "Physical AI combines embodied systems with intelligent algorithms",
    "The field has evolved from industrial automation to humanoid robotics",
    "Key concepts include sensing, actuation, and learning"
  ],
  "prerequisites": ["Basic computer science knowledge"]
}
```

### 2. Code Example

**Attributes**:
- `language`: Programming language (string, e.g., "python", "javascript")
- `code`: Code snippet (string)
- `caption`: Optional description (string)
- `highlight_lines`: Lines to highlight (number[], optional)

**Validation Rules**:
- `language` must be supported by Prism.js (Docusaurus default)
- `code` must be properly formatted and runnable (when applicable)
- `caption` should explain what the code does

**Example (in Markdown)**:
```markdown
```python title="simple_robot_controller.py"
class RobotController:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)

    def move(self, x, y):
        self.position = (x, y)
        print(f"{self.name} moved to {self.position}")
```
```

### 3. Image/Diagram

**Attributes**:
- `src`: File path (string, relative to `/static/img/`)
- `alt`: Alt text for accessibility (string, required)
- `caption`: Optional caption (string)
- `width`: Optional width (number, pixels)

**Validation Rules**:
- `src` must point to existing file in `/static/img/`
- `alt` must be descriptive (not empty)
- Images must be optimized (<100KB per image)
- Prefer WebP format for better compression

**Example (in Markdown)**:
```markdown
![Humanoid robot architecture diagram](./img/robot-architecture.webp)
*Figure 1: High-level architecture of a humanoid robot system*
```

---

## Configuration Data

### Docusaurus Config (docusaurus.config.js)

Key configuration values:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An Interactive Textbook',
  url: 'https://your-domain.vercel.app',
  baseUrl: '/',

  // Metadata
  metadata: [
    {name: 'keywords', content: 'physical ai, humanoid robotics, ai education'},
    {name: 'description', content: 'Learn Physical AI and Humanoid Robotics through an interactive, AI-native textbook'},
  ],

  // Theme config
  themeConfig: {
    navbar: {
      title: 'Physical AI Textbook',
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Start Reading',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook`,
    },
  },

  // Performance
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
```

---

## State Transitions

Since this is a static site, there are no runtime state transitions. However, content has lifecycle states:

### Content Lifecycle

```
Draft → Review → Published → Updated → Archived
```

**States**:
1. **Draft**: Content being written (not committed to main branch)
2. **Review**: Content in PR, under review
3. **Published**: Content merged to main, deployed to production
4. **Updated**: Published content modified (new version)
5. **Archived**: Old content removed or deprecated

**Transition Rules**:
- Draft → Review: PR created
- Review → Published: PR merged to main
- Published → Updated: New PR with changes merged
- Published → Archived: Content removed from main branch

---

## Data Validation

### Build-Time Validation

Docusaurus validates:
- Frontmatter schema (required fields present)
- Internal links (no broken links)
- Markdown syntax (valid MDX)
- Image references (files exist)

### Custom Validation (Optional)

Add custom validation in CI:
- Reading time accuracy (word count / 200 words per minute)
- SEO description length (150-160 chars)
- Learning objectives count (3-5 items)
- Image file sizes (<100KB)

---

## Integration Points

### Future Backend Integration

When backend features are added (RAG, auth, personalization), the textbook will expose:

**Content API** (future):
- `GET /api/chapters`: List all chapters with metadata
- `GET /api/chapters/:id`: Get chapter content and metadata
- `GET /api/search?q=query`: Search chapter content

**User Progress API** (future):
- `POST /api/progress`: Track user reading progress
- `GET /api/progress/:userId`: Get user's reading history

These APIs will consume the frontmatter metadata defined in this document.

---

## Performance Considerations

### Content Size Budgets

- **Per chapter**: 1000-1200 words (7-8 min reading)
- **Total textbook**: 7000-8500 words (45 min reading)
- **Images per chapter**: 1-2 images max
- **Code examples per chapter**: 2-3 examples max

### Bundle Size Impact

- Each chapter adds ~5-10KB to bundle (gzipped)
- Images add ~20-50KB each (WebP optimized)
- Total initial bundle target: <200KB JavaScript

---

## Accessibility Requirements

### Content Accessibility

- All images must have descriptive `alt` text
- Headings must follow hierarchy (H1 → H2 → H3, no skipping)
- Code examples must have language labels for screen readers
- Color contrast must meet WCAG AA standards (4.5:1 for text)
- Links must have descriptive text (no "click here")

### Metadata for Accessibility

```yaml
---
# ... other frontmatter ...
accessibility:
  has_images: boolean          # Does page contain images?
  has_code: boolean            # Does page contain code examples?
  has_math: boolean            # Does page contain mathematical notation?
---
```

---

## Summary

This data model defines:
1. ✅ Content structure (6 chapters, flat hierarchy)
2. ✅ Frontmatter schema (metadata for all pages)
3. ✅ Navigation configuration (sidebar structure)
4. ✅ Content entities (Chapter, Code Example, Image)
5. ✅ Validation rules (reading time, SEO, accessibility)
6. ✅ Integration points (future backend APIs)
7. ✅ Performance budgets (content size, bundle size)

**Next Steps**:
- Generate API contracts in `/contracts/` directory
- Generate `quickstart.md` for developer setup
- Re-evaluate Constitution Check
