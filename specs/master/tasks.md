# Tasks: Interactive Docusaurus Textbook

**Input**: Design documents from `/specs/master/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Project root**: `D:\book\`
- **Website directory**: `website/` (Docusaurus site)
- **Content**: `website/docs/` (Markdown chapters)
- **Configuration**: `website/docusaurus.config.js`, `website/sidebars.js`
- **Custom components**: `website/src/components/`
- **Styles**: `website/src/css/`
- **Static assets**: `website/static/img/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Docusaurus project and basic structure

- [X] T001 Create website directory and initialize Docusaurus 3.x project with classic preset
- [X] T002 Install Node.js dependencies (Docusaurus 3.x, React 18, MDX) in website/package.json
- [X] T003 [P] Configure package.json scripts (start, build, serve, clear) in website/package.json
- [X] T004 [P] Create .gitignore for website directory (node_modules, build, .docusaurus)
- [X] T005 [P] Set Node.js version to 18+ in website/.nvmrc and package.json engines field

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Docusaurus configuration that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Configure docusaurus.config.js with site metadata (title, tagline, url, baseUrl)
- [X] T007 [P] Configure theme settings in docusaurus.config.js (navbar, footer, color mode)
- [X] T008 [P] Create custom CSS variables for branding in website/src/css/custom.css
- [X] T009 Create docs directory structure (website/docs/) with placeholder files
- [X] T010 [P] Configure sidebars.js with basic navigation structure
- [X] T011 [P] Create static assets directory structure (website/static/img/)
- [X] T012 [P] Configure Vercel deployment in website/vercel.json (build command, output directory)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Mobile Reading Experience (Priority: P1) 🎯 MVP

**Goal**: Enable learners to read the textbook smoothly on mobile devices with responsive design

**Independent Test**: Open site on mobile device (or browser DevTools mobile emulation), verify text is readable, navigation works, and no horizontal scrolling occurs

### Implementation for User Story 1

- [X] T013 [P] [US1] Verify Docusaurus responsive breakpoints in website/src/css/custom.css
- [X] T014 [P] [US1] Configure mobile-friendly navbar in website/docusaurus.config.js (hamburger menu)
- [X] T015 [US1] Test responsive design on multiple viewport sizes (320px, 375px, 768px, 1024px)
- [X] T016 [US1] Optimize font sizes and line heights for mobile readability in website/src/css/custom.css
- [X] T017 [US1] Ensure touch targets are at least 44x44px for mobile accessibility

**Checkpoint**: At this point, the site should be fully responsive and readable on mobile devices

---

## Phase 4: User Story 2 - Quick Chapter Navigation (Priority: P2)

**Goal**: Enable learners to navigate quickly between chapters to find specific topics

**Independent Test**: Click through all chapters in sidebar, verify navigation is fast (<1s), sidebar highlights current chapter, and table of contents works

### Implementation for User Story 2

- [X] T018 [P] [US2] Configure sidebar navigation structure in website/sidebars.js (all 6-8 chapters)
- [X] T019 [P] [US2] Enable sidebar auto-collapse on mobile in website/docusaurus.config.js
- [X] T020 [US2] Configure table of contents (TOC) depth and position in website/docusaurus.config.js
- [X] T021 [US2] Add "Previous" and "Next" navigation buttons (enabled by default in Docusaurus)
- [X] T022 [US2] Test navigation performance (verify <1s page transitions)
- [X] T023 [US2] Configure sidebar position and collapsibility in website/docusaurus.config.js

**Checkpoint**: At this point, navigation should be fast and intuitive across all chapters

---

## Phase 5: User Story 3 - Clear Code Examples (Priority: P3)

**Goal**: Provide clear code examples with syntax highlighting so learners can understand implementation details

**Independent Test**: View chapters with code examples, verify syntax highlighting works for Python/JavaScript, code is readable, and copy button appears

### Implementation for User Story 3

- [X] T024 [P] [US3] Configure Prism syntax highlighting themes in website/docusaurus.config.js
- [X] T025 [P] [US3] Enable additional language support (Python, JavaScript, TypeScript, Bash) in Prism config
- [X] T026 [US3] Configure code block features (line numbers, copy button, title) in website/docusaurus.config.js
- [X] T027 [US3] Test syntax highlighting with sample code blocks in multiple languages
- [X] T028 [US3] Optimize code block styling for readability in website/src/css/custom.css
- [X] T029 [US3] Verify code blocks are horizontally scrollable on mobile (no overflow issues)

**Checkpoint**: At this point, code examples should be clear, highlighted, and easy to copy

---

## Phase 6: User Story 4 - Markdown Content Authoring (Priority: P4)

**Goal**: Enable content creators to write chapters in Markdown without worrying about formatting

**Independent Test**: Create a new chapter using Markdown, verify frontmatter is parsed correctly, content renders properly, and chapter appears in sidebar

### Implementation for User Story 4

- [X] T030 [P] [US4] Create chapter template with frontmatter schema in website/docs/_template.md
- [X] T031 [P] [US4] Create Introduction chapter (intro.md) with frontmatter and placeholder content
- [X] T032 [P] [US4] Create Chapter 1: Foundations (chapter-01/index.md) with frontmatter
- [X] T033 [P] [US4] Create Chapter 2: Sensors & Perception (chapter-02/index.md) with frontmatter
- [X] T034 [P] [US4] Create Chapter 3: Actuation & Control (chapter-03/index.md) with frontmatter
- [X] T035 [P] [US4] Create Chapter 4: Learning & Intelligence (chapter-04/index.md) with frontmatter
- [X] T036 [P] [US4] Create Chapter 5: Integration & Systems (chapter-05/index.md) with frontmatter
- [X] T037 [P] [US4] Create Chapter 6: Future & Ethics (chapter-06/index.md) with frontmatter
- [X] T038 [US4] Verify all chapters render correctly with proper frontmatter parsing
- [X] T039 [US4] Add placeholder images to website/static/img/ for each chapter
- [X] T040 [US4] Document Markdown authoring guidelines in website/docs/_template.md

**Checkpoint**: All chapters should be created with proper structure and ready for content writing

---

## Phase 7: Content Writing (Depends on US4)

**Purpose**: Write actual chapter content following the data model specifications

- [X] T041 [P] Write Introduction chapter content (5 min reading time, ~1000 words) in website/docs/intro.md
- [X] T042 [P] Write Chapter 1 content: Foundations (7 min, ~1200 words) in website/docs/chapter-01/index.md
- [X] T043 [P] Write Chapter 2 content: Sensors & Perception (7 min, ~1200 words) in website/docs/chapter-02/index.md
- [X] T044 [P] Write Chapter 3 content: Actuation & Control (7 min, ~1200 words) in website/docs/chapter-03/index.md
- [X] T045 [P] Write Chapter 4 content: Learning & Intelligence (8 min, ~1400 words) in website/docs/chapter-04/index.md
- [X] T046 [P] Write Chapter 5 content: Integration & Systems (7 min, ~1200 words) in website/docs/chapter-05/index.md
- [X] T047 [P] Write Chapter 6 content: Future & Ethics (6 min, ~1000 words) in website/docs/chapter-06/index.md
- [X] T048 Add code examples to relevant chapters (2-3 examples per chapter)
- [X] T049 [P] Create and optimize diagrams for each chapter (1-2 per chapter, <100KB each) in website/static/img/
- [X] T050 Verify total reading time is <45 minutes across all chapters

**Checkpoint**: All content should be written, formatted, and ready for review

---

## Phase 8: Performance Optimization

**Purpose**: Ensure site meets performance requirements (<3s load, >90 Lighthouse score)

- [X] T051 Run production build and verify bundle size (<200KB initial JS)
- [X] T052 [P] Optimize images to WebP format and ensure <100KB per image
- [X] T053 [P] Configure image lazy loading in website/docusaurus.config.js
- [X] T054 Run Lighthouse audit and verify performance score >90
- [X] T055 Test initial page load time on 3G connection (should be <3s)
- [X] T056 Test navigation speed between chapters (should be <1s)
- [X] T057 [P] Minimize custom CSS and remove unused styles in website/src/css/custom.css
- [X] T058 Verify Time to Interactive (TTI) is <200ms

**Checkpoint**: Site should meet all performance requirements

---

## Phase 9: Deployment & Validation

**Purpose**: Deploy to Vercel and validate all acceptance criteria

**Note**: These tasks require user action (connecting GitHub to Vercel). See DEPLOYMENT.md for detailed instructions.

- [ ] T059 Connect GitHub repository to Vercel (requires user account)
- [ ] T060 Configure Vercel project settings (build command: npm run build, output: build/)
- [ ] T061 Deploy to Vercel and verify live URL is accessible
- [ ] T062 Verify HTTPS is enabled on Vercel deployment
- [ ] T063 Test deployed site on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] T064 Test deployed site on real mobile devices (iOS, Android)
- [ ] T065 Verify all chapters are accessible and navigation works on production
- [ ] T066 Run Lighthouse audit on production URL (verify >90 score)
- [ ] T067 Verify page load time <3s on production with 3G throttling
- [ ] T068 Test mobile responsiveness on production deployment

**Checkpoint**: Site should be fully deployed and validated on Vercel

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [X] T069 [P] Add SEO metadata to all chapters (description, keywords in frontmatter)
- [X] T070 [P] Configure Open Graph tags for social sharing in website/docusaurus.config.js
- [X] T071 [P] Add favicon and logo to website/static/img/
- [X] T072 [P] Create README.md in website/ directory with setup instructions
- [X] T073 [P] Verify accessibility (WCAG AA compliance, color contrast, alt text on images)
- [X] T074 [P] Add analytics configuration (optional) in website/docusaurus.config.js
- [X] T075 Run final validation against all acceptance criteria from spec.md
- [X] T076 Document deployment process in specs/master/quickstart.md (if not already done)
- [ ] T077 Create demo video or screenshots for documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Mobile): Can start after Foundational
  - US2 (Navigation): Can start after Foundational
  - US3 (Code Examples): Can start after Foundational
  - US4 (Content Authoring): Can start after Foundational
- **Content Writing (Phase 7)**: Depends on US4 completion
- **Performance (Phase 8)**: Depends on Content Writing completion
- **Deployment (Phase 9)**: Depends on Performance completion
- **Polish (Phase 10)**: Depends on Deployment completion

### User Story Dependencies

- **User Story 1 (Mobile - P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Navigation - P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (Code Examples - P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2
- **User Story 4 (Content Authoring - P4)**: Can start after Foundational (Phase 2) - Independent of US1/US2/US3

### Within Each User Story

- All tasks within a user story can proceed sequentially
- Tasks marked [P] within a story can run in parallel
- Each story should be independently testable

### Parallel Opportunities

- **Phase 1 (Setup)**: Tasks T003, T004, T005 can run in parallel after T001-T002
- **Phase 2 (Foundational)**: Tasks T007, T008, T010, T011, T012 can run in parallel after T006
- **Phase 3 (US1)**: Tasks T013, T014 can run in parallel
- **Phase 4 (US2)**: Tasks T018, T019 can run in parallel
- **Phase 5 (US3)**: Tasks T024, T025 can run in parallel
- **Phase 6 (US4)**: Tasks T030-T037 (chapter creation) can all run in parallel
- **Phase 7 (Content)**: Tasks T041-T047 (content writing) can all run in parallel
- **Phase 8 (Performance)**: Tasks T052, T053, T057 can run in parallel
- **Phase 10 (Polish)**: Tasks T069-T074 can all run in parallel
- **User Stories**: Once Foundational is complete, US1, US2, US3, US4 can all be worked on in parallel

---

## Parallel Example: User Story 4 (Content Authoring)

```bash
# Launch all chapter creation tasks together:
Task: "Create Introduction chapter (intro.md) with frontmatter and placeholder content"
Task: "Create Chapter 1: Foundations (chapter-01/index.md) with frontmatter"
Task: "Create Chapter 2: Sensors & Perception (chapter-02/index.md) with frontmatter"
Task: "Create Chapter 3: Actuation & Control (chapter-03/index.md) with frontmatter"
Task: "Create Chapter 4: Learning & Intelligence (chapter-04/index.md) with frontmatter"
Task: "Create Chapter 5: Integration & Systems (chapter-05/index.md) with frontmatter"
Task: "Create Chapter 6: Future & Ethics (chapter-06/index.md) with frontmatter"

# Then launch all content writing tasks together:
Task: "Write Introduction chapter content (5 min reading time, ~1000 words)"
Task: "Write Chapter 1 content: Foundations (7 min, ~1200 words)"
Task: "Write Chapter 2 content: Sensors & Perception (7 min, ~1200 words)"
Task: "Write Chapter 3 content: Actuation & Control (7 min, ~1200 words)"
Task: "Write Chapter 4 content: Learning & Intelligence (8 min, ~1400 words)"
Task: "Write Chapter 5 content: Integration & Systems (7 min, ~1200 words)"
Task: "Write Chapter 6 content: Future & Ethics (6 min, ~1000 words)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Mobile Reading)
4. **STOP and VALIDATE**: Test mobile reading experience independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Mobile) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Navigation) → Test independently → Deploy/Demo
4. Add User Story 3 (Code Examples) → Test independently → Deploy/Demo
5. Add User Story 4 (Content Authoring) → Test independently → Deploy/Demo
6. Add Content Writing → Test independently → Deploy/Demo
7. Each phase adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Mobile)
   - Developer B: User Story 2 (Navigation)
   - Developer C: User Story 3 (Code Examples)
   - Developer D: User Story 4 (Content Authoring)
3. Once US4 is done, all developers can write content in parallel (Phase 7)
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 77 tasks
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 7 tasks
- Phase 3 (US1 - Mobile): 5 tasks
- Phase 4 (US2 - Navigation): 6 tasks
- Phase 5 (US3 - Code Examples): 6 tasks
- Phase 6 (US4 - Content Authoring): 11 tasks
- Phase 7 (Content Writing): 10 tasks
- Phase 8 (Performance): 8 tasks
- Phase 9 (Deployment): 10 tasks
- Phase 10 (Polish): 9 tasks

**Parallel Opportunities**: 42 tasks marked [P] can run in parallel within their phases

**Independent Test Criteria**:
- US1: Mobile reading works smoothly on all devices
- US2: Navigation is fast and intuitive
- US3: Code examples are clear with syntax highlighting
- US4: Content creators can write in Markdown easily

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) = 17 tasks

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included (not requested in spec.md)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are relative to repository root (D:\book\)
