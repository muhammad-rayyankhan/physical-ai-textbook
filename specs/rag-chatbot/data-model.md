# Data Model: RAG Chatbot

**Feature**: RAG Chatbot
**Date**: 2026-01-31
**Phase**: Phase 1 - Data Model & Structure

## Overview

This document defines the data structures, entities, and relationships for the RAG chatbot system. The system uses two storage layers: Qdrant for vector embeddings and Neon PostgreSQL for metadata and chat history.

---

## Storage Architecture

### Qdrant (Vector Database)
- **Purpose**: Store document chunk embeddings for semantic search
- **Collection**: `textbook_chunks`
- **Vector dimension**: 384 (MiniLM)
- **Distance metric**: Cosine similarity

### Neon PostgreSQL (Relational Database)
- **Purpose**: Store chat sessions, message history, and metadata
- **Tables**: `chat_sessions`, `chat_messages`

---

## Entity 1: Chunk (Qdrant)

### Description
Represents a chunk of textbook content with its vector embedding.

### Attributes
```python
{
  "id": str,                    # Unique identifier (e.g., "chapter-01-chunk-001")
  "vector": List[float],        # 384-dimensional embedding
  "payload": {
    "chapter_id": str,          # Chapter identifier (e.g., "chapter-01")
    "chapter_title": str,       # Chapter title
    "section": str,             # Section name
    "text": str,                # Original text content
    "chunk_index": int,         # Index within chapter
    "total_chunks": int,        # Total chunks in chapter
    "metadata": dict            # Additional metadata
  }
}
```

### Validation Rules
- `id`: Must be unique, format: `{chapter_id}-chunk-{index:03d}`
- `vector`: Must be exactly 384 dimensions
- `chapter_id`: Must match existing chapter
- `text`: 500-1500 characters
- `chunk_index`: 0-based index
- `total_chunks`: Positive integer

### Example
```json
{
  "id": "chapter-01-chunk-001",
  "vector": [0.123, 0.456, ...],
  "payload": {
    "chapter_id": "chapter-01",
    "chapter_title": "Foundations of Physical AI",
    "section": "What is Physical AI?",
    "text": "Physical AI refers to artificial intelligence systems...",
    "chunk_index": 0,
    "total_chunks": 12,
    "metadata": {
      "reading_time": 7,
      "keywords": ["physical ai", "robotics"]
    }
  }
}
```

---

## Entity 2: ChatSession (Neon PostgreSQL)

### Description
Represents a conversation session between a user and the chatbot.

### Schema
```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,                           -- Optional: for authenticated users
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb      -- Flexible metadata storage
);

CREATE INDEX idx_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_sessions_created ON chat_sessions(created_at DESC);
```

### Attributes
- `id`: UUID, primary key
- `user_id`: UUID, nullable (for future auth integration)
- `created_at`: Timestamp, auto-generated
- `updated_at`: Timestamp, auto-updated
- `metadata`: JSONB, flexible storage for session info

### Validation Rules
- `id`: Auto-generated UUID v4
- `user_id`: Valid UUID or NULL
- `created_at`: Cannot be in future
- `updated_at`: Must be >= created_at

### State Transitions
```
Created → Active → Inactive → Archived
```

- **Created**: Session initialized
- **Active**: User actively chatting (last message < 30 min ago)
- **Inactive**: No activity for 30+ minutes
- **Archived**: Session older than 30 days (soft delete)

---

## Entity 3: ChatMessage (Neon PostgreSQL)

### Description
Represents a single question-answer exchange in a chat session.

### Schema
```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    citations JSONB NOT NULL DEFAULT '[]'::jsonb,
    sources JSONB NOT NULL DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_created ON chat_messages(created_at DESC);
```

### Attributes
- `id`: UUID, primary key
- `session_id`: UUID, foreign key to chat_sessions
- `question`: TEXT, user's question
- `answer`: TEXT, chatbot's answer
- `citations`: JSONB, array of citation objects
- `sources`: JSONB, array of source chunk IDs
- `metadata`: JSONB, additional info (response time, token count, etc.)
- `created_at`: Timestamp, auto-generated

### Validation Rules
- `question`: 1-500 characters, non-empty
- `answer`: 1-2000 characters, non-empty
- `citations`: Valid JSON array
- `sources`: Valid JSON array of chunk IDs
- `session_id`: Must reference existing session

### Citation Structure
```json
{
  "citations": [
    {
      "chapter_id": "chapter-01",
      "chapter_title": "Foundations of Physical AI",
      "section": "What is Physical AI?",
      "text_snippet": "Physical AI refers to...",
      "relevance_score": 0.92
    }
  ]
}
```

### Example
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "question": "What is Physical AI?",
  "answer": "Physical AI refers to artificial intelligence systems that interact with and operate in the physical world through embodied agents like robots. According to Chapter 1, it combines embodied systems with intelligent algorithms.",
  "citations": [
    {
      "chapter_id": "chapter-01",
      "chapter_title": "Foundations of Physical AI",
      "section": "What is Physical AI?",
      "text_snippet": "Physical AI refers to artificial intelligence systems...",
      "relevance_score": 0.95
    }
  ],
  "sources": ["chapter-01-chunk-001", "chapter-01-chunk-002"],
  "metadata": {
    "response_time_ms": 1850,
    "tokens_used": 450,
    "model": "gpt-3.5-turbo"
  },
  "created_at": "2026-01-31T10:30:00Z"
}
```

---

## Relationships

### ChatSession ↔ ChatMessage
- **Type**: One-to-Many
- **Relationship**: One session contains many messages
- **Cascade**: Delete messages when session is deleted
- **Constraint**: session_id must reference valid session

### Chunk ↔ ChatMessage
- **Type**: Many-to-Many (implicit)
- **Relationship**: Multiple chunks can be cited in one message, one chunk can be cited in multiple messages
- **Implementation**: Stored as array of chunk IDs in `sources` field

---

## Pydantic Models (API Layer)

### QuestionRequest
```python
from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is Physical AI?",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
```

### Citation
```python
class Citation(BaseModel):
    chapter_id: str
    chapter_title: str
    section: str
    text_snippet: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
```

### AnswerResponse
```python
class AnswerResponse(BaseModel):
    answer: str
    citations: list[Citation]
    sources: list[str]
    session_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Physical AI refers to...",
                "citations": [...],
                "sources": ["chapter-01-chunk-001"],
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
```

### ChatHistory
```python
class ChatHistory(BaseModel):
    session_id: str
    messages: list[dict]
    created_at: str
    message_count: int
```

---

## Data Flow

### Ingestion Flow
```
Markdown Files
    ↓
Load & Parse
    ↓
Chunk Text (800-1000 chars)
    ↓
Generate Embeddings (MiniLM)
    ↓
Store in Qdrant (with metadata)
```

### Query Flow
```
User Question
    ↓
Embed Question (MiniLM)
    ↓
Search Qdrant (top-k=5)
    ↓
Retrieve Chunks
    ↓
Generate Answer (LLM)
    ↓
Extract Citations
    ↓
Store in Neon (chat_messages)
    ↓
Return to User
```

---

## Performance Considerations

### Qdrant Optimization
- **Batch upsert**: Insert 100 chunks at a time
- **Payload indexing**: Index chapter_id for filtering
- **HNSW parameters**: Default (m=16, ef_construct=100)
- **Memory**: ~4KB per chunk (384 floats + payload)

### PostgreSQL Optimization
- **Indexes**: session_id, created_at for fast queries
- **JSONB**: Use GIN indexes for citation searches (future)
- **Partitioning**: Partition by created_at for old data (future)
- **Connection pooling**: Use asyncpg with pool

### Estimated Storage
- **Chunks**: 10,000 chunks × 4KB = 40MB (Qdrant)
- **Messages**: 10,000 messages × 2KB = 20MB (Neon)
- **Total**: ~60MB (well within free tiers)

---

## Validation & Constraints

### Business Rules
1. **Answer grounding**: All answers must cite at least one source
2. **Citation accuracy**: Citations must reference actual chunks
3. **Session timeout**: Sessions inactive for 30+ days are archived
4. **Rate limiting**: Max 100 questions per session per hour (future)

### Data Integrity
1. **Foreign keys**: Enforce session_id references
2. **Cascading deletes**: Delete messages when session deleted
3. **Non-null constraints**: question, answer, citations required
4. **Check constraints**: question length 1-500 chars

---

## Migration Strategy

### Initial Setup
```sql
-- Create tables
CREATE TABLE chat_sessions (...);
CREATE TABLE chat_messages (...);

-- Create indexes
CREATE INDEX idx_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_messages_session ON chat_messages(session_id);

-- Create Qdrant collection
client.create_collection(
    collection_name="textbook_chunks",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
```

### Future Migrations
- Add user authentication (user_id foreign key)
- Add message ratings (thumbs up/down)
- Add conversation branching
- Add multi-turn context

---

## Summary

This data model defines:
1. ✅ Chunk entity for vector storage (Qdrant)
2. ✅ ChatSession entity for conversation tracking (Neon)
3. ✅ ChatMessage entity for Q&A pairs (Neon)
4. ✅ Relationships and constraints
5. ✅ Validation rules and business logic
6. ✅ Performance optimizations
7. ✅ Migration strategy

**Next Steps**:
- Generate API contracts in `/contracts/` directory
- Generate `quickstart.md` for developer setup
- Re-evaluate Constitution Check
