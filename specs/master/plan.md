# Implementation Plan: Docusaurus Interactive Textbook

**Branch**: `master` | **Date**: 2026-02-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/master/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Docusaurus-based interactive textbook for Physical AI and Humanoid Robotics with 6-8 concise chapters, optimized for mobile reading (<45 minutes total), and deployed to Vercel. The textbook must deliver a clean, modern UI with fast page loads (<3 seconds), responsive design, and excellent mobile experience. Content will be written in Markdown for maintainability, with syntax-highlighted code examples and visual diagrams.

## Technical Context

**Language/Version**: JavaScript/TypeScript with Node.js 18+
**Primary Dependencies**: Docusaurus 3.x, React 18, MDX
**Storage**: N/A (static site generation)
**Testing**: Jest + React Testing Library
**Target Platform**: Web (static site, Vercel deployment)
**Project Type**: Web application (frontend only)
**Performance Goals**: <3s initial load, >90 Lighthouse performance score, <1s page navigation
**Constraints**: <3s p95 load time, mobile-responsive, works on low-end devices
**Scale/Scope**: 6-8 chapters, ~45 minutes total reading time, static content

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **Mission Alignment**: This is Core Deliverable #1 from the constitution - "A Docusaurus-based interactive textbook with 6-8 short, clean, modern chapters."

✅ **Architecture Principles**:
- Frontend extremely simple and readable (Docusaurus provides this)
- Clean folder structure (`/website` as specified in constitution)
- No complex dependencies (Docusaurus is the only major dependency)

✅ **Success Criteria**:
- Clean UI, fast loading, mobile friendly (all addressed in NFRs)
- Book readable in <45 minutes (FR1.2)
- Fully deployed to Vercel (FR4.1)

✅ **Constraints**:
- Works on low-end devices (NFR2 addresses this)
- Avoids complexity (static site generation, no backend)
- No extra animation beyond minimal useful motion (out of scope)

✅ **Non-Goals Respected**:
- No overly long chapters (FR1.2 enforces conciseness)
- No complex robotics code (content only)

**GATE STATUS**: ✅ PASS - No violations. Feature fully aligned with constitution.

## Project Structure

### Documentation (this feature)

```text
specs/master/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command) ✅
├── data-model.md        # Phase 1 output (/sp.plan command) ✅
├── quickstart.md        # Phase 1 output (/sp.plan command) ✅
├── contracts/           # Phase 1 output (/sp.plan command) ✅
│   ├── README.md
│   ├── content-schema.yaml
│   ├── content-api.yaml
│   ├── user-progress-api.yaml
│   └── future-api.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
website/                          # Docusaurus static site (Web application)
├── docs/                         # Markdown content files
│   ├── intro.md                  # Introduction/landing page
│   ├── 01-foundations/
│   │   └── index.md
│   ├── 02-sensors-actuators/
│   │   └── index.md
│   ├── 03-control-systems/
│   │   └── index.md
│   ├── 04-perception/
│   │   └── index.md
│   ├── 05-motion-planning/
│   │   └── index.md
│   ├── 06-learning-adaptation/
│   │   └── index.md
│   ├── 07-integration/
│   │   └── index.md
│   └── 08-future-directions/
│       └── index.md
├── src/
│   ├── components/               # Custom React components (if needed)
│   ├── css/
│   │   └── custom.css            # Theme customization
│   └── pages/                    # Custom pages (optional)
├── static/
│   ├── img/                      # Images and diagrams
│   └── files/                    # Downloadable resources
├── docusaurus.config.js          # Docusaurus configuration
├── sidebars.js                   # Sidebar navigation config
├── package.json                  # Dependencies
├── package-lock.json             # Dependency lock file
└── vercel.json                   # Vercel deployment config

tests/                            # Testing (future)
├── e2e/                          # Playwright E2E tests
├── unit/                         # Jest unit tests
└── lighthouse/                   # Performance tests
```

**Structure Decision**: Web application structure (Option 2 variant - frontend only). This is a static site with no backend component for this feature. The `/website` directory contains the complete Docusaurus application. Backend, RAG, and other features are separate deliverables per the constitution and will be added in future features.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
