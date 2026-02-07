# RAG Chatbot Backend

Backend API for the Physical AI & Humanoid Robotics textbook chatbot using RAG (Retrieval-Augmented Generation).

## Architecture

- **Vector Database**: Chroma (local, persistent)
- **Database**: SQLite (file-based)
- **LLM**: Ollama with Llama 3.2 or Mistral (local)
- **Framework**: FastAPI
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

After installation, pull a model:

```bash
# Option 1: Llama 3.2 (3B, faster)
ollama pull llama3.2

# Option 2: Mistral (7B, better quality)
ollama pull mistral
```

Verify installation:

```bash
ollama run llama3.2 "Hello"
```

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

The `.env` file has been created with default settings:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Chroma Configuration
CHROMA_PERSIST_DIR=./data/chroma
CHROMA_COLLECTION=textbook_chunks

# SQLite Configuration
DATABASE_URL=sqlite:///./data/chat_history.db

# Embeddings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

You can modify these settings if needed.

## Setup

### 1. Create Data Directory

```bash
mkdir -p data/chroma
```

### 2. Run Document Ingestion

Ingest the textbook chapters into the vector database:

```bash
cd backend
python -m rag.scripts.ingest_textbook --clear
```

This will:
- Load all chapters from `website/docs/`
- Split them into ~800 character chunks
- Generate embeddings
- Store in Chroma vector database

Expected output: ~60-80 chunks from 6 chapters

### 3. Start the API Server

```bash
cd backend
python -m src.main
```

Or with uvicorn directly:

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check

```bash
GET /api/health
```

Returns the health status of all services (database, vector store, LLM).

### Ask Question

```bash
POST /api/chat/ask
Content-Type: application/json

{
  "question": "What is Physical AI?",
  "session_id": "optional-session-id"
}
```

Response:

```json
{
  "answer": "Physical AI refers to...",
  "citations": [
    {
      "chapter_id": "chapter-01",
      "chapter_title": "Foundations of Physical AI",
      "section": "What is Physical AI?",
      "text_snippet": "...",
      "relevance_score": 0.95
    }
  ],
  "sources": ["chapter-01"],
  "session_id": "uuid"
}
```

### Get Chat History

```bash
GET /api/chat/history?session_id={id}&limit=50
```

Returns chat history for a session.

### List Sessions

```bash
GET /api/chat/sessions?limit=10
```

Returns recent chat sessions.

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
