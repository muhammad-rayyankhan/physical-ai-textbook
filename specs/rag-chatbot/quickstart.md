# Quickstart Guide: RAG Chatbot

**Feature**: RAG Chatbot for Textbook Q&A
**Date**: 2026-01-31
**Phase**: Phase 1 - Developer Setup

## Overview

This guide will help you set up the development environment for the RAG chatbot backend and integrate it with the Docusaurus frontend.

---

## Prerequisites

### Required Software
- **Python**: 3.11+ ([Download](https://www.python.org/downloads/))
- **Node.js**: 18+ (for frontend integration)
- **Git**: For version control
- **Docker**: Optional, for local Qdrant instance

### Required Accounts
- **Qdrant Cloud**: Free tier account ([Sign up](https://cloud.qdrant.io/))
- **Neon**: Free tier PostgreSQL ([Sign up](https://neon.tech/))
- **OpenAI**: API key for GPT-3.5-turbo ([Get key](https://platform.openai.com/api-keys))
- **Railway**: For deployment ([Sign up](https://railway.app/))

### Verify Installation

```bash
python --version  # Should show 3.11+
node --version    # Should show 18+
git --version     # Should show 2.x+
```

---

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd book
```

### 2. Create Backend Directory Structure

```bash
mkdir -p backend/src/{api/routes,services,models,core}
mkdir -p backend/tests/{unit,integration,contract}
mkdir -p rag/{ingest,scripts}
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn[standard] langchain sentence-transformers qdrant-client psycopg2-binary sqlalchemy pydantic openai python-dotenv
```

### 4. Create requirements.txt

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
langchain==0.1.0
sentence-transformers==2.3.1
qdrant-client==1.7.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
pydantic==2.5.3
openai==1.10.0
python-dotenv==1.0.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

### 5. Configure Environment Variables

Create `backend/.env`:

```bash
# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=textbook_chunks

# Neon PostgreSQL
DATABASE_URL=postgresql://user:password@host/database

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,https://your-domain.vercel.app

# Admin API Key (for ingestion)
ADMIN_API_KEY=your-secure-admin-key
```

---

## Backend Development

### 1. Create FastAPI Application

Create `backend/src/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat, health, ingest
from src.core.config import settings

app = FastAPI(
    title="RAG Chatbot API",
    description="API for textbook Q&A chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
app.include_router(health.router, prefix="/api/health", tags=["health"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API", "version": "1.0.0"}
```

### 2. Start Development Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

**API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI.

---

## Database Setup

### 1. Create Qdrant Collection

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

### 2. Create PostgreSQL Tables

```sql
-- Connect to Neon database
psql $DATABASE_URL

-- Create tables
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

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

-- Create indexes
CREATE INDEX idx_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_sessions_created ON chat_sessions(created_at DESC);
CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_created ON chat_messages(created_at DESC);
```

---

## Document Ingestion

### 1. Create Ingestion Script

Create `rag/scripts/ingest_textbook.py`:

```python
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Load textbook chapters
docs_dir = Path("website/docs")
chapters = list(docs_dir.glob("chapter-*/index.md"))

# Initialize components
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Process each chapter
for chapter_file in chapters:
    with open(chapter_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from frontmatter
    # ... (parse YAML frontmatter)

    # Chunk content
    chunks = splitter.split_text(content)

    # Generate embeddings
    embeddings = model.encode(chunks)

    # Upsert to Qdrant
    # ... (batch upsert with metadata)

print("Ingestion complete!")
```

### 2. Run Ingestion

```bash
cd rag/scripts
python ingest_textbook.py
```

**Expected time**: 2-3 minutes for 6 chapters

---

## Frontend Integration

### 1. Create Chat Widget Component

Create `website/src/components/ChatWidget/ChatWidget.tsx`:

```tsx
import React, { useState } from 'react';
import './ChatWidget.css';

interface Message {
  question: string;
  answer: string;
  citations: any[];
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/chat/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });

      const data = await response.json();
      setMessages([...messages, {
        question: input,
        answer: data.answer,
        citations: data.citations
      }]);
      setInput('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-widget">
      {/* Chat UI implementation */}
    </div>
  );
}
```

### 2. Add to Docusaurus

Edit `website/src/theme/Root.tsx`:

```tsx
import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget/ChatWidget';

export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

---

## Testing

### 1. Run Unit Tests

```bash
cd backend
pytest tests/unit -v
```

### 2. Run Integration Tests

```bash
pytest tests/integration -v
```

### 3. Test API Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Ask question
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}'
```

---

## Deployment

### 1. Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

### 2. Configure Environment Variables

In Railway dashboard:
- Add all environment variables from `.env`
- Set `PORT` to Railway's dynamic port
- Configure health check path: `/api/health`

### 3. Verify Deployment

```bash
# Check health
curl https://your-app.railway.app/api/health

# Test question
curl -X POST https://your-app.railway.app/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}'
```

---

## Common Tasks

### Re-ingest Textbook Content

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "X-API-Key: your-admin-key"
```

### View Chat History

```bash
curl "http://localhost:8000/api/chat/history?session_id=<session-id>"
```

### Monitor Logs

```bash
# Local
tail -f backend/logs/app.log

# Railway
railway logs
```

---

## Troubleshooting

### Qdrant Connection Issues

```bash
# Test connection
python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='YOUR_URL', api_key='YOUR_KEY'); print(client.get_collections())"
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql $DATABASE_URL -c "SELECT version();"
```

### Embedding Model Download

```bash
# Pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### CORS Issues

- Verify `CORS_ORIGINS` includes your frontend URL
- Check browser console for CORS errors
- Ensure preflight requests are handled

---

## Performance Optimization

### 1. Enable Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding(text: str):
    return model.encode(text)
```

### 2. Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
```

### 3. Batch Processing

```python
# Batch embed multiple questions
embeddings = model.encode(questions, batch_size=32)
```

---

## Next Steps

After completing setup:

1. ✅ Verify backend API is running
2. ✅ Test document ingestion
3. ✅ Test question answering with sample questions
4. ✅ Integrate chat widget into frontend
5. ✅ Deploy to Railway
6. → Run `/sp.tasks` to generate implementation tasks
7. → Run `/sp.implement` to build the system

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Railway Deployment Guide](https://docs.railway.app/)
- [Sentence Transformers](https://www.sbert.net/)

---

**Estimated Setup Time**: 30-45 minutes
**Support**: See project README or constitution for contact info
