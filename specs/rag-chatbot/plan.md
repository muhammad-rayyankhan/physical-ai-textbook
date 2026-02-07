# Implementation Plan: RAG Chatbot

**Branch**: `feature/rag-chatbot` | **Date**: 2026-01-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/rag-chatbot/spec.md`

## Summary

Build a fully functional RAG (Retrieval-Augmented Generation) chatbot that answers questions ONLY from the Physical AI & Humanoid Robotics textbook. The system will ingest textbook chapters, generate embeddings using MiniLM, store vectors in Qdrant, and provide accurate, cited answers through a FastAPI backend integrated with the Docusaurus frontend.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, LangChain, sentence-transformers, qdrant-client, psycopg2, openai
**Storage**: Qdrant (vector database), Neon PostgreSQL (metadata, chat history)
**Testing**: pytest, pytest-asyncio, httpx (for API testing)
**Target Platform**: Linux server (Railway deployment)
**Project Type**: Web application (backend API + frontend integration)
**Performance Goals**: <2s response time (p95), <100ms vector search, 100 concurrent users
**Constraints**: Qdrant free tier (1GB, 100K vectors), Neon free tier, optimize token usage
**Scale/Scope**: 10,000+ chunks, 6 textbook chapters, support growing content

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Mission Alignment
- **Requirement**: Build a fully AI-native, interactive, intelligent textbook with RAG chatbot
- **Status**: PASS - This feature delivers Core Deliverable #2 (RAG chatbot)

### ✅ Core Deliverables Alignment
- **Requirement**: A fully functional RAG chatbot answering questions ONLY from the book
- **Status**: PASS - Exact match to constitution requirement

### ✅ Success Criteria
- **RAG answers accurate, cited and grounded**: PASS - Spec includes grounding and citation requirements
- **Fully deployed (Backend → Railway, Vectors → Qdrant, Database → Neon)**: PASS - Architecture matches

### ✅ Architecture Principles
- **Keep backend modular (FastAPI + services + routes)**: PASS - FastAPI with service layer planned
- **All data stored cleanly in Neon + Qdrant**: PASS - Clear separation of concerns
- **Clean folder structure (/backend, /website, /rag)**: PASS - Following constitution structure

### ✅ Constraints
- **Must work on free tiers (Qdrant + Neon)**: PASS - Explicitly using free tiers
- **Must support low-end devices**: PASS - Backend API, frontend already optimized
- **Must avoid complexity**: PASS - Using proven libraries (LangChain, FastAPI)

### ✅ Risks and Mitigations
- **RAG low accuracy**: PASS - Using chunking + MiniLM embeddings as specified
- **Token usage high**: PASS - Implementing in phases, optimizing context size

**GATE STATUS**: ✅ ALL CHECKS PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/rag-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                          # FastAPI backend (NEW)
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   ├── ingest.py        # Document ingestion
│   │   │   └── health.py        # Health checks
│   │   └── dependencies.py      # FastAPI dependencies
│   ├── services/
│   │   ├── embeddings.py        # Embedding generation
│   │   ├── vector_store.py      # Qdrant operations
│   │   ├── rag.py               # RAG pipeline
│   │   └── llm.py               # LLM integration
│   ├── models/
│   │   ├── chat.py              # Pydantic models
│   │   └── database.py          # SQLAlchemy models
│   ├── core/
│   │   ├── config.py            # Configuration
│   │   └── database.py          # DB connection
│   └── main.py                  # FastAPI app
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
├── Dockerfile
└── railway.json

rag/                              # RAG utilities (NEW)
├── ingest/
│   ├── chunker.py               # Document chunking
│   ├── loader.py                # Markdown loader
│   └── pipeline.py              # Ingestion pipeline
└── scripts/
    └── ingest_textbook.py       # CLI for ingestion

website/                          # Docusaurus frontend (EXISTS)
├── src/
│   ├── components/
│   │   └── ChatWidget/          # NEW: Chat component
│   │       ├── ChatWidget.tsx
│   │       ├── ChatMessage.tsx
│   │       └── ChatInput.tsx
│   └── services/
│       └── chatApi.ts           # NEW: API client
└── (existing structure)
```

**Structure Decision**: Using Option 2 (Web application) with separate /backend and /rag directories as specified in constitution. Frontend integration adds chat widget to existing /website structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all requirements align with constitution.

---

## Phase 0: Research & Technology Decisions

**Status**: Pending - will generate research.md

**Key Research Areas**:
1. Optimal chunking strategy for textbook content
2. MiniLM vs other embedding models
3. Qdrant setup and configuration
4. LangChain RAG patterns
5. FastAPI + async best practices
6. Railway deployment configuration

---

## Phase 1: Design Artifacts

**Status**: Pending - will generate after research

**Artifacts to Generate**:
1. **data-model.md**: Entities (Chunk, ChatMessage, Session), relationships, validation
2. **contracts/**: OpenAPI spec for all API endpoints
3. **quickstart.md**: Developer setup guide for backend + RAG system

---

## Next Steps

1. Generate research.md (Phase 0)
2. Generate data-model.md, contracts/, quickstart.md (Phase 1)
3. Update agent context with new technologies
4. Run /sp.tasks to generate implementation tasks
5. Run /sp.implement to build the RAG system
