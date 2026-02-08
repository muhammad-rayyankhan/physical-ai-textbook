---
title: Physical AI Textbook Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Physical AI & Humanoid Robotics Textbook - Backend API

RAG-powered chatbot backend for the Physical AI & Humanoid Robotics textbook.

## Architecture

- **Vector Database**: Qdrant Cloud (managed)
- **Database**: Neon PostgreSQL (managed)
- **LLM**: Groq (free, fast inference)
- **Framework**: FastAPI
- **Embeddings**: Hugging Face sentence-transformers

## Features

- **FastAPI Backend**: High-performance async API
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate answers
- **Qdrant Vector Database**: Semantic search over textbook content
- **Groq LLM**: Fast, free language model inference (llama-3.3-70b-versatile)
- **PostgreSQL**: User authentication and session management
- **Hugging Face Embeddings**: Free text embeddings

## Prerequisites

- Python 3.10+
- API keys (all free, no credit card):
  - Qdrant Cloud account
  - Neon PostgreSQL database
  - Groq API key
  - Hugging Face API key

## Configuration

Create a `.env` file with the following variables:

```env
QDRANT_URL=<your-qdrant-cluster-url>
QDRANT_API_KEY=<your-qdrant-api-key>
QDRANT_COLLECTION=textbook_chunks
DATABASE_URL=<your-neon-postgres-url>
GROQ_API_KEY=<your-groq-api-key>
GROQ_MODEL=llama-3.3-70b-versatile
HUGGINGFACE_API_KEY=<your-hf-api-key>
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://website-seven-eta-74.vercel.app,http://localhost:3000
AUTH_SECRET=<your-secret-key>
ENVIRONMENT=production
USE_OPENAI_EMBEDDINGS=false
USE_OPENAI_LLM=false
```

For Hugging Face Spaces deployment, set these as **Repository secrets** in your Space settings.

## Local Development

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your API keys.

### 3. Run Document Ingestion

Ingest the textbook chapters into Qdrant:

```bash
python -m rag.scripts.ingest_textbook --docs-dir ../website/docs --verbose
```

Expected output: ~60-80 chunks from 6 chapters

### 4. Start the API Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment to Hugging Face Spaces

This backend is configured for deployment on Hugging Face Spaces using Docker.

### Quick Deploy

1. Create a new Space at https://huggingface.co/new-space
2. Choose **Docker** as SDK
3. Clone this repository to your Space
4. Set environment variables in Space settings (Repository secrets)
5. Space will automatically build and deploy

See `HUGGINGFACE-DEPLOYMENT.md` for detailed instructions.

## API Endpoints

### Root

```bash
GET /
```

Returns API information and available endpoints.

### Health Check

```bash
GET /api/health
```

Returns the health status of all services (database, vector store, LLM).

### Chat Query

```bash
POST /api/chat/query
Content-Type: application/json

{
  "query": "What is Physical AI?",
  "user_id": "optional-user-id"
}
```

Response:

```json
{
  "answer": "Physical AI refers to...",
  "sources": [
    {
      "content": "...",
      "metadata": {
        "chapter": "chapter-01",
        "title": "Foundations of Physical AI"
      },
      "score": 0.95
    }
  ]
}
```

### Authentication

```bash
POST /api/auth/register
POST /api/auth/login
```

User registration and authentication endpoints.

### Interactive Documentation

Visit `/docs` for Swagger UI or `/redoc` for ReDoc documentation.

## Testing

### Manual API Testing

1. **Health Check**:

```bash
curl http://localhost:8000/api/health
```

2. **Ask a Question**:

```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}'
```

3. **Check Chat History**:

```bash
curl http://localhost:8000/api/chat/history
```

### Expected Behavior

- Response time: 3-10 seconds (local LLM is slower than cloud)
- Answers should be grounded in textbook content
- Citations should reference specific chapters/sections
- Confidence scores should be 0.7-0.95 for good matches

## Project Structure

```
backend/
├── src/
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py          # Chat endpoints
│   │       └── health.py        # Health check
│   ├── core/
│   │   ├── config.py            # Settings
│   │   └── database.py          # Database setup
│   ├── models/
│   │   ├── chat.py              # Pydantic models
│   │   └── database.py          # SQLAlchemy models
│   ├── services/
│   │   ├── embeddings.py        # Embedding generation
│   │   ├── vector_store.py      # Chroma operations
│   │   ├── llm.py               # Ollama integration
│   │   └── rag.py               # RAG pipeline
│   └── main.py                  # FastAPI app
├── rag/
│   ├── ingest/
│   │   ├── loader.py            # Markdown loader
│   │   ├── chunker.py           # Text chunking
│   │   └── pipeline.py          # Ingestion orchestration
│   └── scripts/
│       └── ingest_textbook.py   # CLI script
├── data/                        # Created at runtime
│   ├── chroma/                  # Vector database
│   └── chat_history.db          # SQLite database
├── requirements.txt
├── .env
└── README.md
```

## Troubleshooting

### Ollama Connection Error

**Error**: `Failed to connect to Ollama`

**Solution**:
1. Check if Ollama is running: `ollama list`
2. Verify the model is installed: `ollama pull llama3.2`
3. Check the base URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### Slow Response Times

**Issue**: Responses take 10+ seconds

**Solutions**:
- Use a smaller model: `llama3.2` (3B) instead of `mistral` (7B)
- Reduce `top_k` in RAG pipeline (default: 5)
- Consider using a cloud LLM for production (OpenAI, Anthropic)

### Empty Vector Store

**Error**: `No relevant chunks found`

**Solution**:
1. Run ingestion: `python -m rag.scripts.ingest_textbook --clear`
2. Verify chunks were created: Check logs for "Stored X documents"
3. Check data directory exists: `ls -la data/chroma`

### Database Errors

**Error**: `No such table: chat_sessions`

**Solution**:
- The database is auto-initialized on startup
- If issues persist, delete `data/chat_history.db` and restart the server

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
- Run commands from the `backend/` directory
- Use `python -m` syntax: `python -m src.main`

## Performance Optimization

### For Development

- Use `llama3.2` (3B model) for faster responses
- Set `batch_size=16` for ingestion (faster on CPU)
- Reduce `chunk_size=600` for fewer chunks

### For Production

- Use `mistral` (7B model) for better quality
- Deploy on GPU-enabled server
- Consider switching to cloud LLM (OpenAI GPT-3.5/4)
- Add Redis caching for frequent queries

## Next Steps

1. **Test the API**: Use curl or the interactive docs at `/docs`
2. **Integrate Frontend**: The React chat widget is ready in `website/src/components/ChatWidget/`
3. **Deploy**: See `DEPLOYMENT.md` for deployment instructions
4. **Improve Quality**: Iterate on prompts and chunking strategy

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/ rag/

# Lint
flake8 src/ rag/

# Type checking
mypy src/ rag/
```

## License

See main project LICENSE file.
