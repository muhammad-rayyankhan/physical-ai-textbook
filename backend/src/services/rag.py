"""
RAG Pipeline Service

Orchestrates the full Retrieval-Augmented Generation pipeline.
"""

from typing import List, Dict, Any, Optional
from src.services.embeddings import embedding_service
from src.services.vector_store import vector_store_service
# Switch between demo and real LLM
# from src.services.llm import llm_service  # Real Ollama (slow)
from src.services.llm_demo import llm_service  # Demo mode (instant)
import logging

logger = logging.getLogger(__name__)


class AnswerResponse:
    """Response object containing answer, sources, and confidence."""

    def __init__(
        self,
        answer: str,
        sources: List[Dict[str, Any]],
        confidence: float,
        citations: List[Dict[str, Any]]
    ):
        self.answer = answer
        self.sources = sources
        self.confidence = confidence
        self.citations = citations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "sources": self.sources,
            "confidence": round(self.confidence, 2),
            "citations": self.citations
        }


class RAGService:
    """
    Service that orchestrates the full RAG pipeline.

    Flow:
    1. Embed the user's question
    2. Search vector store for relevant chunks
    3. Build context from retrieved chunks
    4. Generate answer using LLM
    5. Extract citations
    6. Calculate confidence score
    """

    def __init__(self):
        """Initialize RAG service with all sub-services."""
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service
        self.llm_service = llm_service
        logger.info("RAG service initialized")

    def answer_question(
        self,
        question: str,
        chapter_context: Optional[str] = None,
        top_k: int = 5
    ) -> AnswerResponse:
        """
        Answer a question using the RAG pipeline.

        Args:
            question: User's question
            chapter_context: Optional chapter ID to filter results (e.g., "chapter-01")
            top_k: Number of chunks to retrieve (default: 5)

        Returns:
            AnswerResponse with answer, sources, citations, and confidence
        """
        logger.info(f"Processing question: {question[:100]}...")

        # Step 1: Embed the question
        try:
            question_embedding = self.embedding_service.embed_text(question)
            logger.info("Question embedded successfully")
        except Exception as e:
            logger.error(f"Failed to embed question: {str(e)}")
            raise RuntimeError(f"Failed to embed question: {str(e)}")

        # Step 2: Search vector store for relevant chunks
        try:
            filter_metadata = {"chapter_id": chapter_context} if chapter_context else None
            search_results = self.vector_store_service.search(
                query_embedding=question_embedding,
                top_k=top_k,
                filter_metadata=filter_metadata
            )

            if not search_results:
                logger.warning("No relevant chunks found in vector store")
                return AnswerResponse(
                    answer="I don't have enough information to answer that question. The textbook may not cover this topic.",
                    sources=[],
                    confidence=0.0,
                    citations=[]
                )

            logger.info(f"Retrieved {len(search_results)} relevant chunks")

        except Exception as e:
            logger.error(f"Failed to search vector store: {str(e)}")
            raise RuntimeError(f"Failed to search vector store: {str(e)}")

        # Step 3: Build context from retrieved chunks
        context_parts = []
        sources = []

        for i, result in enumerate(search_results):
            # Format: [Source N] Chapter Title - Section\nText
            source_label = f"[Source {i+1}]"
            chapter_title = result.metadata.get("chapter_title", "Unknown Chapter")
            section = result.metadata.get("section", "Unknown Section")
            text = result.text

            context_parts.append(f"{source_label} {chapter_title} - {section}\n{text}\n")

            # Store source metadata
            sources.append({
                "chapter_id": result.metadata.get("chapter_id", ""),
                "chapter_title": chapter_title,
                "section": section,
                "chunk_index": result.metadata.get("chunk_index", 0),
                "similarity_score": round(result.similarity_score, 3)
            })

        context = "\n".join(context_parts)
        logger.info(f"Built context of {len(context)} characters from {len(search_results)} chunks")

        # Step 4: Generate answer using LLM
        try:
            answer = self.llm_service.generate_answer(
                question=question,
                context=context
            )
            logger.info("Answer generated successfully")
        except Exception as e:
            logger.error(f"Failed to generate answer: {str(e)}")
            raise RuntimeError(f"Failed to generate answer: {str(e)}")

        # Step 5: Extract citations
        try:
            citations_objs = self.llm_service.extract_citations(
                answer=answer,
                sources=sources
            )
            citations = [c.to_dict() for c in citations_objs]
            logger.info(f"Extracted {len(citations)} citations")
        except Exception as e:
            logger.warning(f"Failed to extract citations: {str(e)}")
            citations = []

        # Step 6: Calculate confidence score
        # Based on average similarity of top-3 results
        top_scores = [r.similarity_score for r in search_results[:3]]
        confidence = sum(top_scores) / len(top_scores) if top_scores else 0.0

        logger.info(f"Calculated confidence: {confidence:.2f}")

        return AnswerResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            citations=citations
        )

    def check_health(self) -> Dict[str, str]:
        """
        Check health of all RAG pipeline components.

        Returns:
            Dictionary with status of each component
        """
        health = {}

        # Check vector store
        try:
            count = self.vector_store_service.get_count()
            health["vector_store"] = f"up ({count} documents)"
        except Exception as e:
            health["vector_store"] = f"down ({str(e)})"

        # Check LLM
        try:
            if self.llm_service.check_health():
                health["llm"] = "up"
            else:
                health["llm"] = "down (model not available)"
        except Exception as e:
            health["llm"] = f"down ({str(e)})"

        # Check embeddings
        try:
            dim = self.embedding_service.get_embedding_dimension()
            health["embeddings"] = f"up (dim={dim})"
        except Exception as e:
            health["embeddings"] = f"down ({str(e)})"

        return health


# Global service instance
rag_service = RAGService()
