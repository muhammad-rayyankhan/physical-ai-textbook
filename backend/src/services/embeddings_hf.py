"""
Embeddings Service using Hugging Face Inference API

Free embeddings using Hugging Face's serverless inference API.
"""

from typing import List
from huggingface_hub import InferenceClient
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using Hugging Face Inference API.

    Uses the free serverless inference API via InferenceClient.
    Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
    """

    def __init__(self):
        """Initialize Hugging Face Inference Client."""
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.model = "sentence-transformers/all-MiniLM-L6-v2"
        self.client = InferenceClient(token=self.api_key)
        self.dimension = 384
        logger.info(f"Initialized embedding service with Hugging Face model: {self.model}")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector (384 dimensions)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            embedding = self.client.feature_extraction(text, model=self.model)

            # Handle response format (can be nested list)
            if isinstance(embedding, list) and len(embedding) > 0:
                if isinstance(embedding[0], list):
                    embedding = embedding[0]

            return embedding

        except Exception as e:
            logger.error(f"Hugging Face API error: {str(e)}")
            raise RuntimeError(f"Failed to generate embedding: {str(e)}")

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts to embed
            batch_size: Not used (kept for compatibility)

        Returns:
            List of embedding vectors, one per input text
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Filter out empty texts
        valid_texts = [t for t in texts if t and t.strip()]
        if len(valid_texts) != len(texts):
            logger.warning(f"Filtered out {len(texts) - len(valid_texts)} empty texts")

        if not valid_texts:
            raise ValueError("No valid texts to embed")

        logger.info(f"Embedding {len(valid_texts)} texts")

        try:
            # Process texts one by one (InferenceClient doesn't support batch well)
            embeddings = []
            for text in valid_texts:
                embedding = self.client.feature_extraction(text, model=self.model)
                if isinstance(embedding, list) and len(embedding) > 0:
                    if isinstance(embedding[0], list):
                        embedding = embedding[0]
                embeddings.append(embedding)

            return embeddings

        except Exception as e:
            logger.error(f"Hugging Face batch embedding failed: {str(e)}")
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")

    def get_embedding_dimension(self) -> int:
        """
        Get the dimensionality of the embedding vectors.

        Returns:
            384 (dimension of all-MiniLM-L6-v2)
        """
        return self.dimension


# Global singleton instance
embedding_service = EmbeddingService()
