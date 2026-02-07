"""
Vector Store Service

Manages Qdrant Cloud vector database operations for document storage and retrieval.
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from src.core.config import settings
import logging
import uuid

logger = logging.getLogger(__name__)


class SearchResult:
    """Represents a single search result from the vector store."""

    def __init__(self, id: str, text: str, metadata: Dict[str, Any], score: float):
        self.id = id
        self.text = text
        self.metadata = metadata
        self.similarity_score = score  # Qdrant returns similarity directly

    def __repr__(self):
        return f"<SearchResult(id={self.id}, score={self.similarity_score:.3f})>"


class VectorStoreService:
    """
    Service for managing vector database operations with Qdrant Cloud.

    Handles document storage, retrieval, and similarity search.
    """

    def __init__(self):
        """Initialize Qdrant client with cloud connection."""
        logger.info(f"Initializing Qdrant client: {settings.QDRANT_URL}")

        # Create Qdrant client
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
            timeout=30
        )

        self.collection_name = settings.QDRANT_COLLECTION

        # Create collection if it doesn't exist
        self._ensure_collection()

        logger.info(f"Collection '{self.collection_name}' ready")

    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")

                # Get embedding dimension from service
                from src.services.embeddings import embedding_service
                vector_size = embedding_service.get_embedding_dimension()

                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Collection created with vector size: {vector_size}")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection: {e}")
            raise

    def add_chunks(
        self,
        ids: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]]
    ) -> None:
        """
        Add or update document chunks in the vector store.

        Args:
            ids: Unique identifiers for each chunk
            texts: Text content of each chunk
            embeddings: Embedding vectors for each chunk
            metadatas: Metadata dictionaries for each chunk
        """
        if not ids or len(ids) != len(texts) != len(embeddings) != len(metadatas):
            raise ValueError("All input lists must have the same non-zero length")

        logger.info(f"Adding {len(ids)} chunks to vector store")

        # Prepare points for Qdrant
        points = []
        for i, (chunk_id, text, embedding, metadata) in enumerate(zip(ids, texts, embeddings, metadatas)):
            # Add text to metadata for retrieval
            # Store original string ID in metadata for reference
            payload = {**metadata, "text": text, "original_id": chunk_id}

            # Convert string ID to UUID (deterministic using uuid5)
            # This ensures the same string always generates the same UUID
            point_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))

            point = PointStruct(
                id=point_uuid,
                vector=embedding,
                payload=payload
            )
            points.append(point)

        # Upsert points (batch operation)
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Successfully added {len(ids)} chunks")
        except Exception as e:
            logger.error(f"Error adding chunks: {e}")
            raise

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for similar documents using vector similarity.

        Args:
            query_embedding: Query vector to search for
            top_k: Number of results to return (default: 5)
            filter_metadata: Optional metadata filters (e.g., {"chapter_id": "chapter-01"})

        Returns:
            List of SearchResult objects ordered by similarity
        """
        logger.info(f"Searching for top {top_k} similar documents")

        # Build filter if provided
        query_filter = None
        if filter_metadata:
            conditions = []
            for key, value in filter_metadata.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            query_filter = Filter(must=conditions)

        # Execute search
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=query_filter
            )

            # Parse results
            search_results = []
            for result in results:
                search_result = SearchResult(
                    id=str(result.id),
                    text=result.payload.get("text", ""),
                    metadata={k: v for k, v in result.payload.items() if k != "text"},
                    score=result.score
                )
                search_results.append(search_result)

            logger.info(f"Found {len(search_results)} results")
            return search_results
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise

    def delete_collection(self) -> None:
        """
        Delete the entire collection (use for re-ingestion).

        Warning: This will remove all stored documents!
        """
        logger.warning(f"Deleting collection '{self.collection_name}'")
        try:
            self.client.delete_collection(collection_name=self.collection_name)

            # Recreate empty collection
            self._ensure_collection()
            logger.info("Collection deleted and recreated")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_count(self) -> int:
        """Get the total number of documents in the collection."""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return info.points_count
        except Exception as e:
            logger.error(f"Error getting count: {e}")
            return 0

    def get_by_ids(self, ids: List[str]) -> Dict[str, Any]:
        """
        Retrieve specific documents by their IDs.

        Args:
            ids: List of document IDs to retrieve

        Returns:
            Dictionary with documents, metadatas, and ids
        """
        try:
            results = self.client.retrieve(
                collection_name=self.collection_name,
                ids=ids
            )

            return {
                "ids": [str(r.id) for r in results],
                "documents": [r.payload.get("text", "") for r in results],
                "metadatas": [{k: v for k, v in r.payload.items() if k != "text"} for r in results]
            }
        except Exception as e:
            logger.error(f"Error retrieving by IDs: {e}")
            raise


# Global service instance
vector_store_service = VectorStoreService()
