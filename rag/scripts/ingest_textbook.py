"""
Ingestion CLI Script

Command-line interface for running the textbook ingestion pipeline.

Usage:
    python -m rag.scripts.ingest_textbook [--clear] [--docs-dir PATH]
"""

import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from rag.ingest.pipeline import ingest_textbook


def main():
    """Main entry point for the ingestion script."""
    parser = argparse.ArgumentParser(
        description="Ingest textbook chapters into vector database"
    )

    parser.add_argument(
        "--docs-dir",
        type=str,
        default="website/docs",
        help="Path to documentation directory (default: website/docs)"
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before ingestion"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for embedding generation (default: 32)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    # Print configuration
    print("\n" + "=" * 60)
    print("Textbook Ingestion Script")
    print("=" * 60)
    print(f"Documentation directory: {args.docs_dir}")
    print(f"Clear existing data: {args.clear}")
    print(f"Batch size: {args.batch_size}")
    print("=" * 60 + "\n")

    # Run ingestion
    try:
        stats = ingest_textbook(
            docs_dir=args.docs_dir,
            clear_existing=args.clear,
            batch_size=args.batch_size
        )

        # Check for errors
        if stats["errors"]:
            print("\n⚠️  Ingestion completed with errors:")
            for error in stats["errors"]:
                print(f"  - {error}")
            return 1

        print("\n✅ Ingestion completed successfully!")
        print(f"\nStatistics:")
        print(f"  - Chapters loaded: {stats['chapters_loaded']}")
        print(f"  - Chunks created: {stats['chunks_created']}")
        print(f"  - Embeddings generated: {stats['embeddings_generated']}")
        print(f"  - Documents stored: {stats['documents_stored']}")
        print()

        return 0

    except Exception as e:
        logger.exception("Ingestion failed")
        print(f"\n❌ Ingestion failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
