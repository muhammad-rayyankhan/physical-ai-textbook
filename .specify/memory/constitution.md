
# Project Constitution: AI-Native Textbook for Physical AI and Humanoid Robotics

## 1. Mission
Build a fully AI-native, interactive, intelligent textbook that teaches the Physical AI & Humanoid Robotics course. The product must be fast, simple, beautiful and feel like a REAL AI-powered education platform -- not just a book.

## 2. Core Deliverables
1. A Docusaurus-based interactive textbook with 6-8 short, clean, modern chapters.
2. A fully functional RAG chatbot answering questions ONLY from the book.
3. User authentication (signup/login) using Better-Auth.
4. Personalized chapter content based on user-background.
5. One-click Urdu translation for every chapter.
6. Auto-generated summaries, quizzes, and learning boosters.

## 3. Success Criteria
- Clean UI, fast loading, mobile friendly.
- Book readable in < 45 minutes total.
- RAG answers accurate, cited and grounded.
- Personalization visibly improves text.
- Urdu translation high-quality and fast.
- Fully deployed:
  - Frontend -> Vercel
  - Backend -> Railway
  - Vectors -> Qdrant
  - Database -> Neon

## 4. Non-Goals
- No extra animation beyond minimal useful motion.
- No overly long chapters (short + clear only).
- No complex robotics code -- only education content.

## 5. Architecture Principles
- Keep frontend extremely simple, readable.
- Keep backend modular (FastAPI + services + routes).
- All data must be stored cleanly in Neon + Qdrant.
- Use clean folder structure:
  - `/backend`
  - `/website`
  - `/rag`
  - `/agents`
- Use reusable agent skill for bonus scoring.

## 6. User Stories (Prioritized)
1. As a learner, I want to read the textbook smoothly.
2. As a learner, I want to ask the chatbot questions.
3. As a learner, I want personalized content based on my background.
4. As a learner, I want Urdu translation.
5. As a learner, I want summaries + quizzes.
6. As an admin, I want clean architecture and deployment.

## 7. Constraints
- Must work on free tiers (Qdrant + Neon).
- Must deploy within 90 seconds demo recording.
- Must support low-end devices (users reading on phones).
- Must avoid complexity and heavy dependencies.

## 8. Risks and Mitigations
- **RAG low accuracy** -> use chunking + MiniLM embeddings.
- **Token usage high** -> implement in phases.
- **User confusion** -> keep UI minimal and clean.
- **Backend errors** -> add health checks + logging.

## 9. Definition of Done
- All chapters visible and readable.
- Chatbot fully functional with grounded answers.
- Auth + personalization + translation working.
- Quizzes + summaries per chapter generated.
- Fully deployed URLs live and stable.
- 90-second demo recorded.

## 10. Development Phases

### Phase 1: Foundation (Week 1)
- Set up project structure (`/backend`, `/website`, `/rag`, `/agents`)
- Initialize Docusaurus for textbook
- Set up FastAPI backend with health checks
- Configure Neon database and Qdrant vector store
- Implement Better-Auth authentication (signup/login)
- Deploy basic infrastructure to Vercel + Railway

**Exit Criteria**: Auth working, empty textbook deployed, backend health endpoint live

### Phase 2: Core Content (Week 2)
- Write 6-8 short chapters on Physical AI & Humanoid Robotics
- Each chapter: 5-7 minutes reading time, clear structure
- Implement chapter navigation and reading experience
- Add mobile-responsive design
- Test readability and loading speed

**Exit Criteria**: All chapters readable, < 45 min total reading time, mobile-friendly

### Phase 3: RAG Intelligence (Week 3)
- Chunk textbook content for embeddings
- Generate embeddings using MiniLM
- Store vectors in Qdrant
- Build RAG chatbot with FastAPI endpoint
- Implement citation and grounding mechanism
- Add chatbot UI component in Docusaurus

**Exit Criteria**: Chatbot answers questions accurately with citations from book

### Phase 4: Personalization (Week 4)
- Collect user background during signup
- Implement content adaptation logic
- Generate personalized chapter introductions
- A/B test personalization effectiveness
- Store user preferences in Neon

**Exit Criteria**: Personalization visibly improves content relevance

### Phase 5: Translation & Enhancements (Week 5)
- Implement one-click Urdu translation per chapter
- Generate auto-summaries for each chapter
- Create quiz generation system
- Add learning booster features
- Test translation quality and speed

**Exit Criteria**: Urdu translation fast and accurate, quizzes functional

### Phase 6: Polish & Deploy (Week 6)
- Performance optimization (loading, caching)
- Security hardening (input validation, rate limiting)
- Final UI polish and accessibility checks
- Complete deployment to production
- Record 90-second demo video
- Documentation and handoff

**Exit Criteria**: All features live, demo recorded, URLs stable

## 11. Technical Standards

### Code Quality
- **Python (Backend)**: Follow PEP 8, use type hints, max function length 50 lines
- **TypeScript/JavaScript (Frontend)**: Use ESLint, Prettier, strict TypeScript
- **File Organization**: Group by feature, not by type
- **Naming**: Clear, descriptive names; avoid abbreviations
- **Comments**: Only for "why", not "what"; code should be self-documenting

### Testing Requirements
- **Unit Tests**: 80% coverage minimum for backend services
- **Integration Tests**: All API endpoints must have integration tests
- **E2E Tests**: Critical user flows (signup, login, chat, read chapter)
- **Performance Tests**: Page load < 2s, API response < 500ms
- **Test Data**: Use fixtures, never production data

### Security Standards
- **Authentication**: JWT tokens, secure httpOnly cookies
- **Input Validation**: Validate all user inputs, sanitize for XSS
- **Rate Limiting**: 100 requests/minute per user
- **Secrets Management**: Use environment variables, never commit secrets
- **HTTPS Only**: All production traffic encrypted
- **SQL Injection**: Use parameterized queries only
- **CORS**: Whitelist frontend domain only

### Performance Benchmarks
- **Frontend**: First Contentful Paint < 1.5s, Time to Interactive < 3s
- **Backend**: API p95 latency < 500ms, p99 < 1s
- **Database**: Query time < 100ms for reads, < 200ms for writes
- **RAG**: Embedding generation < 2s, similarity search < 500ms
- **Translation**: Urdu translation < 3s per chapter

### Accessibility Requirements
- **WCAG 2.1 Level AA** compliance minimum
- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Readers**: Proper ARIA labels and semantic HTML
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Mobile**: Touch targets minimum 44x44px

## 12. Quality Gates

### Pre-Commit
- Linting passes (ESLint, Pylint)
- Type checking passes (TypeScript, mypy)
- Unit tests pass
- No secrets in code

### Pre-Merge
- All tests pass (unit, integration)
- Code review approved
- No security vulnerabilities (Snyk scan)
- Documentation updated

### Pre-Deploy
- E2E tests pass
- Performance benchmarks met
- Security scan clean
- Smoke tests on staging pass
- Rollback plan documented

## 13. Technology Stack

### Frontend
- **Framework**: Docusaurus 3.x
- **Language**: TypeScript 5.x
- **Styling**: Tailwind CSS
- **State**: React Context API
- **Deployment**: Vercel

### Backend
- **Framework**: FastAPI 0.110+
- **Language**: Python 3.11+
- **Database**: Neon (PostgreSQL)
- **Vector Store**: Qdrant Cloud (free tier)
- **Auth**: Better-Auth
- **Deployment**: Railway

### AI/ML
- **Embeddings**: sentence-transformers (MiniLM)
- **LLM**: OpenAI GPT-4 (for personalization, translation, summaries)
- **RAG**: LangChain or custom implementation
- **Translation**: OpenAI GPT-4 with prompt engineering

### DevOps
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Monitoring**: Railway logs + Vercel Analytics
- **Error Tracking**: Sentry (optional)

## 14. Documentation Requirements

### Code Documentation
- README.md in each major directory (`/backend`, `/website`, `/rag`)
- API documentation using FastAPI auto-docs (Swagger)
- Inline comments for complex logic only
- Type hints for all functions

### User Documentation
- Quick start guide in main README
- Deployment instructions (DEPLOYMENT.md)
- Environment variables documentation
- Troubleshooting guide

### Architecture Documentation
- System architecture diagram
- Data flow diagrams
- API contracts and schemas
- Database schema documentation

## 15. Monitoring and Observability

### Logging
- **Levels**: DEBUG (dev), INFO (prod), ERROR (always)
- **Format**: Structured JSON logs
- **Content**: Request ID, user ID, timestamp, action, result
- **Retention**: 30 days minimum

### Metrics
- **Frontend**: Page views, load times, error rates
- **Backend**: Request count, latency, error rates
- **RAG**: Query count, accuracy, response time
- **Database**: Connection pool, query time, error rate

### Alerts
- **Critical**: API down, database unreachable, auth failure spike
- **Warning**: High latency (>1s), error rate >5%, disk space <20%
- **Info**: Deployment complete, backup complete

## 16. Rollback and Recovery

### Rollback Strategy
- **Frontend**: Instant rollback via Vercel dashboard
- **Backend**: Railway rollback to previous deployment
- **Database**: Point-in-time recovery (Neon feature)
- **Vectors**: Re-index from source if corrupted

### Backup Policy
- **Database**: Daily automated backups (Neon)
- **Vectors**: Weekly snapshots (Qdrant)
- **Code**: Git repository (GitHub)
- **Retention**: 30 days for all backups

### Disaster Recovery
- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 24 hours
- **Runbook**: Documented recovery procedures
- **Testing**: Quarterly disaster recovery drills

## Governance
- This constitution supersedes all other practices.
- All development decisions must align with these principles.
- Changes to this constitution require explicit documentation and approval.
- Constitution reviews occur at phase boundaries.
- All architectural decisions must be documented as ADRs.

**Version**: 2.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-02-06
