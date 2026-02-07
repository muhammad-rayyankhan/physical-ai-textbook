"""
LLM Service using Groq API

Fast, free LLM inference using Groq's API.
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
    Service for generating answers using Groq API.

    Groq provides fast, free LLM inference with models like Llama 3.
    """

    def __init__(self):
        """Initialize Groq client."""
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1"
        logger.info(f"Initialized LLM service with Groq model: {self.model}")

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

        logger.info(f"Generating answer for question: {question[:100]}...")

        try:
            # Call Groq API (OpenAI-compatible)
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=30
            )

            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()

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

        Args:
            answer: Generated answer text
            sources: List of source metadata dictionaries

        Returns:
            List of Citation objects
        """
        citations = []
        seen_chapters = set()

        # Extract chapter mentions from answer
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
        Check if Groq API is available.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5
            )
            response.raise_for_status()
            logger.info("Groq API health check passed")
            return True

        except Exception as e:
            logger.error(f"Groq API health check failed: {str(e)}")
            return False


# Global service instance
llm_service = LLMService()
