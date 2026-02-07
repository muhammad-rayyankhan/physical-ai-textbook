"""
Chat API Routes

Endpoints for chatbot question-answering and chat history.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4
import logging

from src.models.chat import (
    QuestionRequest,
    AnswerResponse,
    Citation,
    ChatHistoryResponse,
    ChatMessageResponse
)
from src.models.database import ChatSession, ChatMessage
from src.core.database import get_db
from src.services.rag import rag_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    """
    Ask a question about the textbook content.

    The RAG pipeline will:
    1. Embed the question
    2. Search for relevant chunks
    3. Generate an answer using LLM
    4. Return answer with citations

    Args:
        request: Question request with message and optional session_id
        db: Database session

    Returns:
        Answer with citations and sources
    """
    try:
        logger.info(f"Received question: {request.question[:100]}...")

        # Get or create session
        session_id = request.session_id
        if session_id:
            # Verify session exists
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not session:
                logger.warning(f"Session {session_id} not found, creating new session")
                session = ChatSession(id=session_id)
                db.add(session)
                db.commit()
        else:
            # Create new session
            session = ChatSession()
            db.add(session)
            db.commit()
            session_id = str(session.id)

        logger.info(f"Using session: {session_id}")

        # Run RAG pipeline
        try:
            rag_response = rag_service.answer_question(
                question=request.question,
                chapter_context=None,  # Could be extracted from request if needed
                top_k=5
            )
        except Exception as e:
            logger.error(f"RAG pipeline failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate answer: {str(e)}"
            )

        # Convert RAG response to API response format
        citations = [
            Citation(
                chapter_id=c["chapter_id"],
                chapter_title=c["chapter_title"],
                section=c["section"],
                text_snippet=c.get("text_snippet", ""),
                relevance_score=c.get("similarity_score", 0.0)
            )
            for c in rag_response.citations
        ]

        # Store message in database
        chat_message = ChatMessage(
            session_id=session.id,
            question=request.question,
            answer=rag_response.answer,
            citations=[c.dict() for c in citations],
            sources=rag_response.sources,
            metadata={"confidence": rag_response.confidence}
        )
        db.add(chat_message)
        db.commit()

        logger.info(f"Stored message in database: {chat_message.id}")

        # Build response
        response = AnswerResponse(
            answer=rag_response.answer,
            citations=citations,
            sources=[s["chapter_id"] for s in rag_response.sources],
            session_id=session_id
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in ask_question")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a session.

    Args:
        session_id: Optional session ID to filter by
        limit: Maximum number of messages to return (default: 50)
        db: Database session

    Returns:
        Chat history with messages
    """
    try:
        if session_id:
            # Get specific session
            session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")

            # Get messages for this session
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.desc())
                .limit(limit)
                .all()
            )

        else:
            # Get latest session
            session = (
                db.query(ChatSession)
                .order_by(ChatSession.created_at.desc())
                .first()
            )

            if not session:
                # No sessions exist, return empty
                return ChatHistoryResponse(
                    session_id=str(uuid4()),
                    messages=[],
                    message_count=0,
                    created_at=""
                )

            # Get messages for latest session
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session.id)
                .order_by(ChatMessage.created_at.desc())
                .limit(limit)
                .all()
            )

        # Convert to response format
        message_responses = []
        for msg in reversed(messages):  # Reverse to get chronological order
            citations = [
                Citation(**c) if isinstance(c, dict) else c
                for c in msg.citations
            ]

            message_responses.append(
                ChatMessageResponse(
                    id=msg.id,
                    question=msg.question,
                    answer=msg.answer,
                    citations=citations,
                    created_at=msg.created_at.isoformat()
                )
            )

        response = ChatHistoryResponse(
            session_id=str(session.id),
            messages=message_responses,
            message_count=len(message_responses),
            created_at=session.created_at.isoformat()
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in get_chat_history")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/sessions")
async def list_sessions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    List recent chat sessions.

    Args:
        limit: Maximum number of sessions to return (default: 10)
        db: Database session

    Returns:
        List of session summaries
    """
    try:
        sessions = (
            db.query(ChatSession)
            .order_by(ChatSession.created_at.desc())
            .limit(limit)
            .all()
        )

        session_summaries = []
        for session in sessions:
            # Get message count
            message_count = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session.id)
                .count()
            )

            # Get first message for preview
            first_message = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session.id)
                .order_by(ChatMessage.created_at.asc())
                .first()
            )

            preview = first_message.question[:100] if first_message else "Empty session"

            session_summaries.append({
                "session_id": str(session.id),
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
                "message_count": message_count,
                "preview": preview
            })

        return {"sessions": session_summaries}

    except Exception as e:
        logger.exception("Unexpected error in list_sessions")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
