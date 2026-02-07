# Research: RAG Chatbot for Textbook Q&A

**Feature**: RAG Chatbot
**Date**: 2026-01-31
**Phase**: Phase 0 - Technology Research & Decisions

## Overview

This document captures research findings and technology decisions for building a RAG (Retrieval-Augmented Generation) chatbot that answers questions from the Physical AI & Humanoid Robotics textbook.

---

## Decision 1: Document Chunking Strategy

### Decision
Use **recursive character-based chunking** with 800-1000 character chunks and 200 character overlap.

### Rationale
1. **Semantic coherence**: Recursive splitting respects paragraph and sentence boundaries
2. **Optimal retrieval**: 800-1000 chars (~150-200 tokens) balances context vs precision
3. **Overlap**: 200 char overlap ensures concepts spanning chunk boundaries aren't lost
4. **LLM context**: Multiple chunks fit within LLM context window (4K-8K tokens)

### Alternatives Considered
- **Fixed-size chunking**: Rejected - can split sentences mid-word, loses semantic meaning
- **Sentence-based chunking**: Rejected - too granular, loses context
- **Section-based chunking**: Rejected - sections too large (>2000 tokens), reduces retrieval precision

### Implementation
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len
)
```

### Best Practices
1. Preserve markdown structure (headings, code blocks)
2. Include chapter/section metadata with each chunk
3. Test with sample questions to validate chunk size
4. Monitor retrieval quality and adjust if needed

---

## Decision 2: Embedding Model Selection

### Decision
Use **sentence-transformers/all-MiniLM-L6-v2** for embeddings.

### Rationale
1. **Performance**: 384 dimensions, fast inference (<50ms per chunk)
2. **Quality**: 68.06 on STSB benchmark, good for semantic search
3. **Size**: 80MB model, runs on CPU efficiently
4. **Cost**: Free, no API calls required
5. **Proven**: Widely used in production RAG systems

### Alternatives Considered
- **OpenAI text-embedding-ada-002**: Rejected - costs $0.0001/1K tokens, adds latency
- **all-mpnet-base-v2**: Rejected - larger (420MB), slower, marginal quality gain
- **BGE-small-en-v1.5**: Considered - similar performance, less community support

### Implementation
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)
```

### Performance Metrics
- Embedding generation: ~30ms per chunk (CPU)
- Batch processing: 100 chunks in ~1 second
- Memory usage: ~200MB loaded

---

## Decision 3: Vector Database Configuration (Qdrant)

### Decision
Use **Qdrant Cloud free tier** with cosine similarity and HNSW indexing.

### Rationale
1. **Free tier**: 1GB storage, 100K vectors (sufficient for 10K+ chunks)
2. **Performance**: <50ms search latency, HNSW for fast ANN search
3. **Features**: Metadata filtering, payload storage, REST + gRPC APIs
4. **Scalability**: Easy upgrade path if needed

### Configuration
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

client.create_collection(
    collection_name="textbook_chunks",
    vectors_config=VectorParams(
        size=384,  # MiniLM dimension
        distance=Distance.COSINE
    )
)
```

### Indexing Strategy
- **Collection**: Single collection "textbook_chunks"
- **Distance metric**: Cosine similarity (best for normalized embeddings)
- **HNSW parameters**: Default (m=16, ef_construct=100)
- **Payload**: Store chapter_id, section, text, chunk_index

### Best Practices
1. Batch upsert for ingestion (100 chunks at a time)
2. Use payload filtering for chapter-specific queries
3. Monitor collection size vs free tier limits
4. Implement incremental updates (upsert by ID)

---

## Decision 4: RAG Pipeline Architecture

### Decision
Use **LangChain** with custom retrieval chain and prompt engineering.

### Rationale
1. **Proven framework**: Battle-tested RAG patterns
2. **Flexibility**: Easy to customize retrieval and generation
3. **Integrations**: Works with Qdrant, OpenAI, FastAPI
4. **Observability**: Built-in callbacks for logging

### Pipeline Flow
```
User Question
    ↓
Embed Question (MiniLM)
    ↓
Vector Search (Qdrant, top-k=5)
    ↓
Rerank Results (optional)
    ↓
Build Prompt (question + context + instructions)
    ↓
LLM Generation (GPT-3.5-turbo)
    ↓
Extract Citations
    ↓
Return Answer + Citations
```

### Implementation
```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import OpenAI

# Setup
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant(client=qdrant_client, collection_name="textbook_chunks", embeddings=embeddings)

# RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(model="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",  # Stuff all context into prompt
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)
```

### Prompt Engineering
```python
PROMPT_TEMPLATE = """You are a helpful assistant answering questions about Physical AI and Humanoid Robotics.

Use ONLY the following context from the textbook to answer the question. If the answer is not in the context, say "I don't know based on the textbook content."

Context:
{context}

Question: {question}

Answer with citations (mention the chapter/section):"""
```

---

## Decision 5: LLM Selection for Answer Generation

### Decision
Use **OpenAI GPT-3.5-turbo** for answer generation.

### Rationale
1. **Cost**: $0.0015/1K input tokens, $0.002/1K output tokens (affordable)
2. **Quality**: Good instruction following, accurate answers
3. **Speed**: ~1-2s response time
4. **Context**: 4K token context window (sufficient for 5 chunks)

### Alternatives Considered
- **GPT-4**: Rejected - 10x more expensive, overkill for this use case
- **Claude**: Considered - similar quality, but OpenAI has better LangChain integration
- **Open-source (Llama 2)**: Rejected - requires GPU hosting, adds complexity

### Token Optimization
- Average question: 20 tokens
- Average chunk: 150 tokens
- 5 chunks: 750 tokens
- Prompt overhead: 100 tokens
- **Total input**: ~870 tokens per query
- **Estimated cost**: $0.0013 per query

### Best Practices
1. Set temperature=0 for consistent answers
2. Use system message to enforce grounding
3. Implement token counting to prevent overruns
4. Cache common questions (future optimization)

---

## Decision 6: Backend Framework (FastAPI)

### Decision
Use **FastAPI** with async/await for all endpoints.

### Rationale
1. **Performance**: Async support for concurrent requests
2. **Developer experience**: Auto-generated OpenAPI docs, type hints
3. **Modern**: Built on Starlette + Pydantic
4. **Ecosystem**: Great integrations with LangChain, Qdrant

### API Structure
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="RAG Chatbot API")

class QuestionRequest(BaseModel):
    question: str
    session_id: str | None = None

class AnswerResponse(BaseModel):
    answer: str
    citations: list[dict]
    sources: list[str]

@app.post("/api/chat/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    # RAG pipeline
    result = await rag_service.answer(request.question)
    return AnswerResponse(**result)
```

### Best Practices
1. Use dependency injection for services
2. Implement proper error handling
3. Add request validation with Pydantic
4. Enable CORS for frontend integration
5. Add rate limiting (future)

---

## Decision 7: Database for Metadata (Neon PostgreSQL)

### Decision
Use **Neon PostgreSQL free tier** for chat history and metadata.

### Rationale
1. **Free tier**: 0.5GB storage, 100 hours compute/month
2. **Serverless**: Auto-scaling, pay-per-use
3. **PostgreSQL**: Full SQL support, JSONB for flexible schema
4. **Integrations**: Works with SQLAlchemy, asyncpg

### Schema Design
```sql
-- Chat sessions
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chat messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    citations JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_created ON chat_messages(created_at DESC);
```

### Best Practices
1. Use UUIDs for IDs (distributed-friendly)
2. Store citations as JSONB for flexibility
3. Add indexes for common queries
4. Implement soft deletes (future)

---

## Decision 8: Deployment Platform (Railway)

### Decision
Deploy backend to **Railway** with automatic deployments from GitHub.

### Rationale
1. **Constitution requirement**: Backend → Railway
2. **Free tier**: $5 credit/month, sufficient for development
3. **Developer experience**: Zero-config deployments, auto-scaling
4. **Integrations**: GitHub, environment variables, logs

### Configuration
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn src.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### Environment Variables
- `QDRANT_URL`: Qdrant cloud URL
- `QDRANT_API_KEY`: Qdrant API key
- `DATABASE_URL`: Neon PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key
- `CORS_ORIGINS`: Allowed frontend origins

---

## Decision 9: Frontend Integration

### Decision
Build **React chat widget** integrated into Docusaurus site.

### Rationale
1. **Seamless UX**: Embedded in existing textbook UI
2. **React**: Docusaurus is React-based, easy integration
3. **Responsive**: Works on mobile and desktop
4. **Minimal**: Follows constitution's "simple, beautiful" principle

### Component Structure
```tsx
// ChatWidget.tsx - Main container
// ChatMessage.tsx - Individual message display
// ChatInput.tsx - Question input field
// chatApi.ts - API client for backend
```

### Features
- Floating chat button (bottom-right)
- Expandable chat panel
- Message history
- Citation links to textbook chapters
- Loading states
- Error handling

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| Backend Framework | FastAPI | 0.109+ | Async, modern, auto-docs |
| Embeddings | sentence-transformers | 2.3+ | Fast, free, quality |
| Vector DB | Qdrant Cloud | Latest | Free tier, performant |
| Database | Neon PostgreSQL | 15+ | Serverless, free tier |
| RAG Framework | LangChain | 0.1+ | Proven patterns |
| LLM | OpenAI GPT-3.5-turbo | Latest | Cost-effective, quality |
| Deployment | Railway | - | Constitution requirement |
| Frontend | React + TypeScript | 18+ | Docusaurus integration |

---

## Risk Mitigation

### Risk 1: Qdrant Free Tier Limits
- **Mitigation**: Monitor collection size, optimize chunk count, implement cleanup
- **Fallback**: Upgrade to paid tier ($25/month) if needed

### Risk 2: OpenAI API Costs
- **Mitigation**: Implement caching, optimize context size, monitor usage
- **Fallback**: Switch to GPT-3.5-turbo-16k or open-source model

### Risk 3: Retrieval Quality
- **Mitigation**: Test with diverse questions, tune chunk size, implement reranking
- **Fallback**: Hybrid search (vector + keyword), query expansion

### Risk 4: Railway Free Tier Limits
- **Mitigation**: Optimize cold starts, monitor usage, implement health checks
- **Fallback**: Upgrade to paid tier or switch to Render/Fly.io

---

## Next Steps (Phase 1)

1. ✅ Research complete - all technology decisions documented
2. → Generate `data-model.md` (entities, relationships, validation)
3. → Generate `contracts/` (OpenAPI specs for all endpoints)
4. → Generate `quickstart.md` (developer setup guide)
5. → Re-evaluate Constitution Check post-design

---

## References

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/async/)
- [Sentence Transformers](https://www.sbert.net/)
- [Railway Deployment](https://docs.railway.app/)
