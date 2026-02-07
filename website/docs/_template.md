---
id: template
title: Chapter Title Here
sidebar_label: Chapter X
sidebar_position: X
description: Brief description for SEO (150-160 characters)
keywords: [keyword1, keyword2, keyword3, keyword4]
reading_time: 7
chapter_number: X
learning_objectives:
  - Learning objective 1
  - Learning objective 2
  - Learning objective 3
key_takeaways:
  - Key takeaway 1
  - Key takeaway 2
  - Key takeaway 3
---

# Chapter X: Chapter Title Here

*Estimated reading time: 7 minutes*

## Introduction

Brief introduction to the chapter topic...

## Main Section 1

Content for the first main section...

### Subsection 1.1

Detailed content...

## Main Section 2

Content for the second main section...

## Code Example

```python title="example.py"
# Example code with syntax highlighting
class Example:
    def __init__(self):
        self.value = 0

    def method(self):
        return self.value
```

## Key Takeaways

- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

---

**Next:** [Chapter X+1: Next Chapter Title](../chapter-XX/index.md) →

---

## Markdown Authoring Guidelines

### Frontmatter Requirements

All chapter files MUST include the following frontmatter fields:

- `id`: Unique identifier (e.g., "chapter-01", "intro")
- `title`: Full chapter title (10-100 characters)
- `sidebar_label`: Short label for sidebar (3-30 characters)
- `sidebar_position`: Order in sidebar (1-based integer)
- `description`: SEO description (150-160 characters)
- `keywords`: Array of 3-10 keywords
- `reading_time`: Estimated minutes (5-10 per chapter)
- `chapter_number`: Chapter number (1-8)
- `learning_objectives`: Array of 3-5 objectives
- `key_takeaways`: Array of 3-5 takeaways

### Content Guidelines

**Reading Time:**
- Target: 5-10 minutes per chapter
- Word count: ~1000-1200 words per chapter
- Total textbook: <45 minutes reading time

**Structure:**
- Use H2 (##) for main sections
- Use H3 (###) for subsections
- Keep paragraphs short (3-4 sentences max)
- Use bullet points for lists

**Code Examples:**
- Include 2-3 code examples per chapter
- Use language tags for syntax highlighting (python, javascript, bash, etc.)
- Add titles to code blocks: ```python title="filename.py"
- Keep examples concise and runnable

**Images:**
- Place images in `/website/static/img/`
- Use WebP format when possible
- Optimize to <100KB per image
- Always include descriptive alt text
- Reference: `![Alt text](./img/image-name.webp)`

**Links:**
- Use relative links for internal navigation
- Link to next chapter at the end
- Link to previous chapter if helpful

**Accessibility:**
- Use semantic HTML headings (don't skip levels)
- Provide alt text for all images
- Ensure color contrast meets WCAG AA standards
- Use descriptive link text (not "click here")

### Validation Checklist

Before committing a chapter, verify:

- [ ] Frontmatter includes all required fields
- [ ] Description is 150-160 characters
- [ ] Reading time is 5-10 minutes
- [ ] 3-5 learning objectives listed
- [ ] 3-5 key takeaways listed
- [ ] Code examples have syntax highlighting
- [ ] Images have alt text
- [ ] Internal links work
- [ ] No spelling errors
- [ ] Consistent terminology used

### Example Frontmatter

```yaml
---
id: chapter-01
title: Foundations of Physical AI
sidebar_label: Chapter 1
sidebar_position: 2
description: Explore the history, key concepts, and foundational principles of Physical AI and humanoid robotics
keywords: [physical ai, robotics history, ai fundamentals, humanoid robots]
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
---
```
