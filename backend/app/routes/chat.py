from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    chapter_context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: float

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatMessage):
    """
    RAG-powered chatbot endpoint.
    Answers questions ONLY from the textbook content.
    """
    # TODO: Implement RAG query logic
    # 1. Embed the question
    # 2. Query Qdrant for relevant chunks
    # 3. Generate answer with citations
    raise HTTPException(status_code=501, detail="RAG system not implemented yet")

@router.get("/history")
async def get_chat_history():
    """Get user's chat history"""
    # TODO: Implement chat history retrieval
    return {"messages": []}
