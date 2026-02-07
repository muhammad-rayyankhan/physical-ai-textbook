# Feature Specification: RAG Chatbot

**Feature**: RAG Chatbot for Textbook Q&A
**Branch**: `feature/rag-chatbot`
**Date**: 2026-01-31
**Status**: Planning

## Overview

Build a fully functional RAG (Retrieval-Augmented Generation) chatbot that answers questions ONLY from the Physical AI & Humanoid Robotics textbook. The chatbot must provide accurate, cited, and grounded answers based on the textbook content.

## Functional Requirements

### FR1: Document Ingestion & Vectorization
- **FR1.1**: Ingest all 6 textbook chapters from Markdown files
- **FR1.2**: Chunk documents into optimal sizes for retrieval (target: 500-1000 tokens per chunk)
- **FR1.3**: Generate embeddings using MiniLM model (sentence-transformers/all-MiniLM-L6-v2)
- **FR1.4**: Store embeddings in Qdrant vector database
- **FR1.5**: Include metadata with each chunk (chapter, section, page reference)

### FR2: Question Answering
- **FR2.1**: Accept user questions via API endpoint
- **FR2.2**: Retrieve top-k relevant chunks from Qdrant (k=3-5)
- **FR2.3**: Generate answers using retrieved context only
- **FR2.4**: Provide citations with chapter and section references
- **FR2.5**: Return "I don't know" if answer not found in textbook

### FR3: Answer Grounding
- **FR3.1**: All answers must be grounded in retrieved textbook content
- **FR3.2**: Include source citations for every answer
- **FR3.3**: Highlight relevant text snippets from source
- **FR3.4**: Prevent hallucination by constraining to retrieved context

### FR4: API Endpoints
- **FR4.1**: `POST /api/chat/ask` - Submit question and get answer
- **FR4.2**: `GET /api/chat/history` - Retrieve conversation history
- **FR4.3**: `POST /api/ingest` - Trigger document re-ingestion (admin only)
- **FR4.4**: `GET /api/health` - Health check endpoint

### FR5: Frontend Integration
- **FR5.1**: Chat widget embedded in Docusaurus site
- **FR5.2**: Real-time streaming responses
- **FR5.3**: Display citations with clickable chapter links
- **FR5.4**: Conversation history persistence

## Non-Functional Requirements

### NFR1: Performance
- Query response time: <2 seconds (p95)
- Embedding generation: <500ms per chunk
- Vector search: <100ms
- Support 100 concurrent users

### NFR2: Accuracy
- Answer relevance: >90% (based on user feedback)
- Citation accuracy: 100% (all citations must be valid)
- Hallucination rate: <5%

### NFR3: Scalability
- Handle 10,000+ chunks in vector database
- Support growing textbook content
- Efficient incremental updates

### NFR4: Cost
- Use Qdrant free tier (1GB storage, 100K vectors)
- Use Neon free tier for metadata storage
- Optimize token usage for LLM calls

## User Stories

**US1**: As a learner, I want to ask questions about textbook content so I can clarify concepts I don't understand.

**US2**: As a learner, I want to see citations for answers so I can verify information and read more in the textbook.

**US3**: As a learner, I want accurate answers that don't make up information so I can trust the chatbot.

**US4**: As an admin, I want to re-ingest textbook content when chapters are updated so the chatbot stays current.

## Acceptance Criteria

- [ ] All 6 textbook chapters ingested and vectorized
- [ ] Chatbot answers questions accurately with citations
- [ ] Response time <2 seconds for 95% of queries
- [ ] Citations link back to correct textbook sections
- [ ] Chatbot refuses to answer questions outside textbook scope
- [ ] Chat widget integrated into Docusaurus frontend
- [ ] Conversation history persists across sessions
- [ ] Backend deployed to Railway
- [ ] Qdrant vector database configured and accessible
- [ ] Health checks and logging implemented

## Out of Scope

- Multi-turn conversations with context (Phase 1: single-turn only)
- User authentication (separate feature)
- Personalization (separate feature)
- Urdu translation (separate feature)
- Voice input/output

## Dependencies

- Textbook content (completed in Feature 1)
- Qdrant vector database (free tier)
- Neon PostgreSQL database (free tier)
- Railway deployment platform
- OpenAI API or similar LLM (for answer generation)

## Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Vector DB**: Qdrant (cloud free tier)
- **Database**: Neon PostgreSQL (metadata, chat history)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: OpenAI GPT-3.5-turbo or GPT-4 (for answer generation)

### Frontend
- **Integration**: React component in Docusaurus
- **Styling**: Tailwind CSS or Docusaurus theme
- **State**: React hooks for chat state

## Architecture

```
┌─────────────────┐
│   Docusaurus    │
│   Frontend      │
│  (Chat Widget)  │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
│  (Railway)      │
└────┬───────┬────┘
     │       │
     │       ▼
     │  ┌─────────┐
     │  │ Qdrant  │
     │  │ Vectors │
     │  └─────────┘
     │
     ▼
┌─────────┐
│  Neon   │
│   DB    │
└─────────┘
```

## Data Model

### Chunk (Qdrant)
```python
{
  "id": "chapter-01-section-02-chunk-001",
  "vector": [0.123, 0.456, ...],  # 384 dimensions (MiniLM)
  "payload": {
    "chapter_id": "chapter-01",
    "chapter_title": "Foundations of Physical AI",
    "section": "Historical Evolution",
    "text": "The journey began with...",
    "chunk_index": 1,
    "total_chunks": 5
  }
}
```

### ChatMessage (Neon)
```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY,
  session_id UUID NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  citations JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Risks

1. **Embedding quality**: MiniLM may not capture semantic meaning well
   - Mitigation: Test with sample questions, consider upgrading to larger model if needed

2. **Token costs**: LLM API calls can be expensive
   - Mitigation: Use GPT-3.5-turbo, implement caching, limit context size

3. **Hallucination**: LLM may generate answers not in textbook
   - Mitigation: Strict prompt engineering, validate against retrieved chunks

4. **Qdrant free tier limits**: 1GB storage, 100K vectors
   - Mitigation: Optimize chunk size, monitor usage

## Success Metrics

- Answer accuracy: >90% (user feedback)
- Response time: <2s (p95)
- Citation accuracy: 100%
- User satisfaction: >4/5 stars
- Daily active users: Track engagement

## References

- Constitution: `.specify/memory/constitution.md`
- Textbook spec: `specs/master/spec.md`
- Qdrant docs: https://qdrant.tech/documentation/
- LangChain RAG: https://python.langchain.com/docs/use_cases/question_answering/
