"""
LLM Service

Interfaces with Ollama (local LLM) for answer generation.
"""

from typing import List, Dict, Any
import requests
from src.core.config import settings
import logging
import re

logger = logging.getLogger(__name__)


class Citation:
    """Represents a citation extracted from the answer."""

    def __init__(self, chapter_id: str, chapter_title: str, section: str, chunk_index: int):
        self.chapter_id = chapter_id
        self.chapter_title = chapter_title
        self.section = section
        self.chunk_index = chunk_index

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chapter_id": self.chapter_id,
            "chapter_title": self.chapter_title,
            "section": self.section,
            "chunk_index": self.chunk_index
        }


class LLMService:
    """
    Service for generating answers using Ollama (local LLM).

    Handles prompt construction, answer generation, and citation extraction.
    """

    def __init__(self):
        """Initialize Ollama client."""
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        logger.info(f"Initialized LLM service with Ollama model: {self.model} at {self.base_url}")

    def generate_answer(
        self,
        question: str,
        context: str,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> str:
        """
        Generate an answer to the question based on the provided context.

        Args:
            question: User's question
            context: Retrieved context from textbook
            temperature: Sampling temperature (0.0-1.0, lower = more deterministic)
            max_tokens: Maximum tokens in response

        Returns:
            Generated answer text
        """
        # Build the prompt
        system_prompt = (
            "You are a helpful assistant for a Physical AI and Humanoid Robotics textbook. "
            "Answer questions ONLY based on the provided context from the textbook. "
            "If the answer is not in the context, say 'I don't have enough information to answer that.' "
            "Cite specific sections when possible. Keep answers concise (2-3 paragraphs max)."
        )

        user_prompt = f"""Context from textbook:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the context above
- Cite specific sections when possible (e.g., "According to Chapter 1...")
- If unsure, say so
- Keep answers concise (2-3 paragraphs max)

Answer:"""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        logger.info(f"Generating answer for question: {question[:100]}...")

        try:
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=300
            )

            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "").strip()

            logger.info(f"Generated answer of length {len(answer)} characters")
            return answer

        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise RuntimeError(f"Failed to generate answer: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise RuntimeError(f"Failed to generate answer: {str(e)}")

    def extract_citations(
        self,
        answer: str,
        sources: List[Dict[str, Any]]
    ) -> List[Citation]:
        """
        Extract citations from the answer based on available sources.

        This is a simple implementation that matches chapter mentions in the answer
        to the provided sources.

        Args:
            answer: Generated answer text
            sources: List of source metadata dictionaries

        Returns:
            List of Citation objects
        """
        citations = []
        seen_chapters = set()

        # Extract chapter mentions from answer (e.g., "Chapter 1", "chapter-01")
        chapter_patterns = [
            r"Chapter\s+(\d+)",
            r"chapter\s+(\d+)",
            r"chapter-(\d+)"
        ]

        for source in sources:
            chapter_id = source.get("chapter_id", "")
            chapter_title = source.get("chapter_title", "")
            section = source.get("section", "")
            chunk_index = source.get("chunk_index", 0)

            # Check if this chapter is mentioned in the answer
            chapter_num = chapter_id.replace("chapter-", "")

            # Check if chapter is referenced in answer
            is_mentioned = False
            for pattern in chapter_patterns:
                if re.search(pattern.replace(r"(\d+)", chapter_num), answer, re.IGNORECASE):
                    is_mentioned = True
                    break

            # Always include the first source, or if mentioned
            if not citations or is_mentioned:
                if chapter_id not in seen_chapters:
                    citation = Citation(
                        chapter_id=chapter_id,
                        chapter_title=chapter_title,
                        section=section,
                        chunk_index=chunk_index
                    )
                    citations.append(citation)
                    seen_chapters.add(chapter_id)

        # If no citations found, use all sources (up to 3)
        if not citations:
            for source in sources[:3]:
                citation = Citation(
                    chapter_id=source.get("chapter_id", ""),
                    chapter_title=source.get("chapter_title", ""),
                    section=source.get("section", ""),
                    chunk_index=source.get("chunk_index", 0)
                )
                citations.append(citation)

        logger.info(f"Extracted {len(citations)} citations from answer")
        return citations

    def check_health(self) -> bool:
        """
        Check if Ollama service is available.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            logger.info("Ollama health check passed")
            return True

        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False


# Global service instance
llm_service = LLMService()
