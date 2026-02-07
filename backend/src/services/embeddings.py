"""
Embeddings Service

Generates embeddings using either OpenAI API or local sentence-transformers.
Supports feature flag to switch between cloud and local embeddings.
"""

from typing import List, Optional
from sentence_transformers import SentenceTransformer
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings.

    Supports two modes:
    - OpenAI API (1536 dimensions, text-embedding-3-small)
    - Local sentence-transformers (384 dimensions, all-MiniLM-L6-v2)

    Uses a singleton pattern to cache models in memory for efficiency.
    """

    _instance = None
    _model = None
    _openai_client = None

    def __new__(cls):
        """Singleton pattern to ensure only one model instance."""
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the embedding model based on configuration."""
        if self._model is None and self._openai_client is None:
            self.use_openai = settings.USE_OPENAI_EMBEDDINGS

            if self.use_openai:
                # Initialize OpenAI client
                try:
                    from openai import OpenAI
                    self._openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                    self.model_name = settings.OPENAI_EMBEDDING_MODEL
                    logger.info(f"Using OpenAI embeddings: {self.model_name}")
                except ImportError:
                    logger.error("OpenAI package not installed. Install with: pip install openai")
                    raise
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI client: {e}")
                    raise
            else:
                # Initialize local sentence-transformers model
                logger.info(f"Loading local embedding model: {settings.EMBEDDING_MODEL}")
                self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
                logger.info("Local embedding model loaded successfully")

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector
            - 1536 dimensions for OpenAI
            - 384 dimensions for local model
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        if self.use_openai:
            try:
                response = self._openai_client.embeddings.create(
                    input=text,
                    model=self.model_name
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"OpenAI embedding failed: {e}")
                raise RuntimeError(f"Failed to generate OpenAI embedding: {e}")
        else:
            embedding = self._model.encode(text, convert_to_numpy=True)
            return embedding.tolist()

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts efficiently.

        Args:
            texts: List of input texts to embed
            batch_size: Number of texts to process at once
                       - OpenAI: up to 2048 per request
                       - Local: 32 recommended

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

        if self.use_openai:
            try:
                embeddings = []
                # OpenAI supports up to 2048 texts per request
                for i in range(0, len(valid_texts), batch_size):
                    batch = valid_texts[i:i + batch_size]
                    response = self._openai_client.embeddings.create(
                        input=batch,
                        model=self.model_name
                    )
                    embeddings.extend([item.embedding for item in response.data])
                return embeddings
            except Exception as e:
                logger.error(f"OpenAI batch embedding failed: {e}")
                raise RuntimeError(f"Failed to generate OpenAI embeddings: {e}")
        else:
            embeddings = self._model.encode(
                valid_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embeddings.tolist()

    def get_embedding_dimension(self) -> int:
        """
        Get the dimensionality of the embedding vectors.

        Returns:
            Embedding dimension:
            - 1536 for OpenAI text-embedding-3-small
            - 384 for local all-MiniLM-L6-v2
        """
        if self.use_openai:
            return 1536  # text-embedding-3-small dimension
        else:
            return self._model.get_sentence_embedding_dimension()


# Global singleton instance
embedding_service = EmbeddingService()
