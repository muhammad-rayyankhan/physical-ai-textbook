"""
Ingestion Pipeline

Orchestrates the full document ingestion process:
1. Load chapters from markdown files
2. Chunk chapters into smaller pieces
3. Generate embeddings for each chunk
4. Store chunks and embeddings in vector database
"""

from typing import List, Optional
from pathlib import Path
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from rag.ingest.loader import load_all_chapters
from rag.ingest.chunker import chunk_all_chapters
from src.services.embeddings import embedding_service
from src.services.vector_store import vector_store_service

logger = logging.getLogger(__name__)


def ingest_textbook(
    docs_dir: str = "website/docs",
    clear_existing: bool = False,
    batch_size: int = 32
) -> dict:
    """
    Run the full ingestion pipeline.

    Args:
        docs_dir: Path to documentation directory
        clear_existing: Whether to clear existing data before ingestion
        batch_size: Batch size for embedding generation

    Returns:
        Dictionary with ingestion statistics
    """
    logger.info("=" * 60)
    logger.info("Starting textbook ingestion pipeline")
    logger.info("=" * 60)

    stats = {
        "chapters_loaded": 0,
        "chunks_created": 0,
        "embeddings_generated": 0,
        "documents_stored": 0,
        "errors": []
    }

    try:
        # Step 1: Clear existing data if requested
        if clear_existing:
            logger.info("Clearing existing vector store data...")
            vector_store_service.delete_collection()
            logger.info("Vector store cleared")

        # Step 2: Load all chapters
        logger.info(f"Loading chapters from: {docs_dir}")
        chapters = load_all_chapters(docs_dir)
        stats["chapters_loaded"] = len(chapters)

        if not chapters:
            logger.error("No chapters found!")
            return stats

        logger.info(f"Loaded {len(chapters)} chapters")

        # Step 3: Chunk all chapters
        logger.info("Chunking chapters...")
        chunks = chunk_all_chapters(chapters)
        stats["chunks_created"] = len(chunks)

        if not chunks:
            logger.error("No chunks created!")
            return stats

        logger.info(f"Created {len(chunks)} chunks")

        # Step 4: Generate embeddings
        logger.info(f"Generating embeddings (batch size: {batch_size})...")
        texts = [chunk.text for chunk in chunks]

        try:
            embeddings = embedding_service.embed_batch(texts, batch_size=batch_size)
            stats["embeddings_generated"] = len(embeddings)
            logger.info(f"Generated {len(embeddings)} embeddings")
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            stats["errors"].append(f"Embedding generation failed: {str(e)}")
            return stats

        # Step 5: Store in vector database
        logger.info("Storing chunks in vector database...")

        # Prepare data for vector store
        ids = [chunk.id for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        try:
            vector_store_service.add_chunks(
                ids=ids,
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )
            stats["documents_stored"] = len(ids)
            logger.info(f"Stored {len(ids)} documents in vector database")
        except Exception as e:
            logger.error(f"Failed to store documents: {str(e)}")
            stats["errors"].append(f"Vector store failed: {str(e)}")
            return stats

        # Step 6: Verify storage
        total_docs = vector_store_service.get_count()
        logger.info(f"Vector store now contains {total_docs} documents")

        logger.info("=" * 60)
        logger.info("Ingestion pipeline completed successfully!")
        logger.info("=" * 60)
        logger.info(f"Summary:")
        logger.info(f"  - Chapters loaded: {stats['chapters_loaded']}")
        logger.info(f"  - Chunks created: {stats['chunks_created']}")
        logger.info(f"  - Embeddings generated: {stats['embeddings_generated']}")
        logger.info(f"  - Documents stored: {stats['documents_stored']}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Ingestion pipeline failed: {str(e)}")
        stats["errors"].append(f"Pipeline error: {str(e)}")
        raise

    return stats


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Run ingestion
    try:
        stats = ingest_textbook(clear_existing=True)

        if stats["errors"]:
            print("\n⚠️  Ingestion completed with errors:")
            for error in stats["errors"]:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("\n✅ Ingestion completed successfully!")
            sys.exit(0)

    except Exception as e:
        print(f"\n❌ Ingestion failed: {str(e)}")
        sys.exit(1)
