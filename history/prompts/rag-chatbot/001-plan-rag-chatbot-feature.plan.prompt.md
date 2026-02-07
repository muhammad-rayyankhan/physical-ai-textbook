---
id: 001
title: Plan RAG Chatbot Feature
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: rag-chatbot
branch: feature/rag-chatbot
user: user
command: /sp.plan rag-chatbot
labels: ["planning", "rag", "chatbot", "fastapi", "qdrant", "langchain"]
links:
  spec: specs/rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/rag-chatbot/spec.md
  - specs/rag-chatbot/plan.md
  - specs/rag-chatbot/research.md
  - specs/rag-chatbot/data-model.md
  - specs/rag-chatbot/contracts/api.yaml
  - specs/rag-chatbot/quickstart.md
tests:
  - null
---

## Prompt

rag-chatbot

## Response snapshot

Executed the `/sp.plan` workflow for the RAG Chatbot feature (Core Deliverable #2 from constitution):

**Setup Phase:**
- Created feature specification in specs/rag-chatbot/spec.md
- Manually set up planning structure (setup-plan.ps1 detected master branch)
- Created plan.md with technical context and constitution check

**Constitution Check - ✅ ALL PASSED:**
- Mission alignment: Delivers Core Deliverable #2 (RAG chatbot)
- Architecture: FastAPI backend, Qdrant vectors, Neon database (matches constitution)
- Folder structure: /backend, /rag, /website (follows constitution)
- Free tiers: Qdrant + Neon free tiers
- Constraints: All requirements met

**Phase 0: Research & Technology Decisions:**
Generated comprehensive research.md with 9 key decisions:
1. Document chunking: Recursive character-based, 800-1000 chars, 200 overlap
2. Embeddings: sentence-transformers/all-MiniLM-L6-v2 (384 dims, free, fast)
3. Vector DB: Qdrant Cloud free tier with cosine similarity
4. RAG pipeline: LangChain with custom retrieval chain
5. LLM: OpenAI GPT-3.5-turbo ($0.0013/query estimated)
6. Backend: FastAPI with async/await
7. Database: Neon PostgreSQL for chat history
8. Deployment: Railway (constitution requirement)
9. Frontend: React chat widget in Docusaurus

**Phase 1: Design Artifacts:**
1. **data-model.md**: 3 entities defined
   - Chunk (Qdrant): Vector embeddings with metadata
   - ChatSession (Neon): Conversation tracking
   - ChatMessage (Neon): Q&A pairs with citations
   - Relationships, validation rules, performance optimizations

2. **contracts/api.yaml**: OpenAPI 3.0 spec with 4 endpoints
   - POST /api/chat/ask: Submit questions, get answers with citations
   - GET /api/chat/history: Retrieve conversation history
   - POST /api/ingest: Trigger document ingestion (admin)
   - GET /api/health: Health check
   - Complete request/response schemas, error handling

3. **quickstart.md**: Comprehensive developer guide
   - Prerequisites and setup (Python 3.11+, Qdrant, Neon, OpenAI)
   - Backend development with FastAPI
   - Database setup (Qdrant collection, PostgreSQL tables)
   - Document ingestion pipeline
   - Frontend integration (React chat widget)
   - Testing and deployment to Railway
   - Troubleshooting and optimization tips

**Agent Context:**
- Updated CLAUDE.md with new technologies (attempted, but parsed placeholder values from master plan)

**Key Architectural Decisions:**
- Backend: FastAPI + LangChain + sentence-transformers
- Storage: Qdrant (vectors) + Neon (metadata/history)
- RAG flow: Question → Embed → Search (top-5) → LLM → Citations
- Performance: <2s response time, <100ms vector search
- Cost: ~$0.0013 per query (GPT-3.5-turbo)

**Project Structure:**
```
backend/          # NEW: FastAPI backend
  src/
    api/routes/   # Chat, ingest, health endpoints
    services/     # Embeddings, vector store, RAG, LLM
    models/       # Pydantic + SQLAlchemy models
    core/         # Config, database
  tests/          # Unit, integration, contract tests

rag/              # NEW: RAG utilities
  ingest/         # Chunking, loading, pipeline
  scripts/        # CLI ingestion script

website/          # EXISTS: Add chat widget
  src/components/ChatWidget/  # NEW
```

## Outcome

- ✅ Impact: Complete implementation plan for RAG chatbot (Core Deliverable #2)
- 🧪 Tests: No tests yet (planning phase)
- 📁 Files: 6 files created (spec, plan, research, data-model, contracts, quickstart)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks, then `/sp.implement`
- 🧠 Reflection: Planning complete for Feature 2. All Phase 0 and Phase 1 artifacts generated. Constitution requirements fully aligned. Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: setup-plan.ps1 doesn't support -Feature parameter, manually created structure
- Graders run and results (PASS/FAIL): PASS - All constitution checks passed, comprehensive planning artifacts
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Generate tasks with /sp.tasks, then implement RAG system
