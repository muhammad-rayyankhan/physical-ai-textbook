"""
Embeddings Service using Local Sentence Transformers

Fast, reliable embeddings using locally-run sentence-transformers models.
No API calls required - runs entirely on your machine.
"""

from typing import List
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using local sentence-transformers.

    Uses sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
    Model is downloaded once and cached locally.
    """

    def __init__(self):
        """Initialize local sentence transformer model."""
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        logger.info(f"Loading local embedding model: {self.model_name}")

        # Load model (will download on first run, then cache)
        self.model = SentenceTransformer(self.model_name)
        self.dimension = 384

        logger.info(f"Local embedding model loaded successfully (dim={self.dimension})")

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
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()

        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise RuntimeError(f"Failed to generate embedding: {str(e)}")

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts to embed
            batch_size: Batch size for processing (default: 32)

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

        logger.info(f"Embedding {len(valid_texts)} texts in batches of {batch_size}")

        try:
            # Generate embeddings in batches
            embeddings = self.model.encode(
                valid_texts,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )

            return embeddings.tolist()

        except Exception as e:
            logger.error(f"Batch embedding failed: {str(e)}")
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
