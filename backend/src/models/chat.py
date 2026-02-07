from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class Citation(BaseModel):
    """Citation from textbook source."""
    chapter_id: str = Field(..., description="Chapter identifier (e.g., 'chapter-01')")
    chapter_title: str = Field(..., description="Chapter title")
    section: str = Field(..., description="Section name within chapter")
    text_snippet: str = Field(..., description="Relevant text excerpt from source")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score from vector search")

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_id": "chapter-01",
                "chapter_title": "Foundations of Physical AI",
                "section": "What is Physical AI?",
                "text_snippet": "Physical AI refers to artificial intelligence systems...",
                "relevance_score": 0.95
            }
        }


class QuestionRequest(BaseModel):
    """Request model for asking a question."""
    question: str = Field(..., min_length=1, max_length=500, description="User's question about textbook content")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is Physical AI?",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class AnswerResponse(BaseModel):
    """Response model for chatbot answer."""
    answer: str = Field(..., description="Generated answer to the question")
    citations: List[Citation] = Field(..., description="List of citations supporting the answer")
    sources: List[str] = Field(..., description="List of source chunk IDs used")
    session_id: str = Field(..., description="Session ID for this conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Physical AI refers to artificial intelligence systems that interact with and operate in the physical world through embodied agents like robots.",
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
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class ChatMessageResponse(BaseModel):
    """Response model for a single chat message."""
    id: UUID
    question: str
    answer: str
    citations: List[Citation]
    created_at: str

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    session_id: UUID
    messages: List[ChatMessageResponse]
    message_count: int
    created_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "123e4567-e89b-12d3-a456-426614174000",
                "messages": [],
                "message_count": 0,
                "created_at": "2026-01-31T10:00:00Z"
            }
        }


class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    chapters: Optional[List[str]] = Field(None, description="Optional list of specific chapters to ingest")
    force: bool = Field(False, description="Force re-ingestion even if content hasn't changed")

    class Config:
        json_schema_extra = {
            "example": {
                "chapters": ["chapter-01", "chapter-02"],
                "force": False
            }
        }


class IngestResponse(BaseModel):
    """Response model for ingestion job."""
    status: str = Field(..., description="Ingestion job status")
    job_id: UUID = Field(..., description="Job ID for tracking")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "started",
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "estimated_duration": 120
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Overall service health status")
    timestamp: str = Field(..., description="Health check timestamp")
    services: Optional[dict] = Field(None, description="Status of individual services")
    version: str = Field("1.0.0", description="API version")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-31T10:00:00Z",
                "services": {
                    "database": "up",
                    "vector_db": "up",
                    "llm": "up"
                },
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "INVALID_REQUEST",
                "message": "Question must be between 1 and 500 characters",
                "details": {}
            }
        }
