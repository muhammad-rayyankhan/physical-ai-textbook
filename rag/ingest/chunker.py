"""
Text Chunker

Splits chapters into semantic chunks for vector storage and retrieval.
"""

from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import logging

logger = logging.getLogger(__name__)


class Chunk:
    """Represents a single text chunk from a chapter."""

    def __init__(
        self,
        id: str,
        text: str,
        metadata: Dict[str, Any]
    ):
        self.id = id
        self.text = text
        self.metadata = metadata

    def __repr__(self):
        return f"<Chunk(id={self.id}, length={len(self.text)})>"


def extract_section_from_text(text: str) -> str:
    """
    Extract the section name from a chunk of text.

    Looks for the first heading (## or ###) in the text.

    Args:
        text: Text chunk

    Returns:
        Section name or "General" if no heading found
    """
    # Look for markdown headings
    match = re.search(r"^#{2,3}\s+(.+)$", text, re.MULTILINE)
    if match:
        section = match.group(1).strip()
        # Remove any markdown formatting
        section = re.sub(r"[*_`]", "", section)
        return section

    return "General"


def chunk_chapter(
    chapter,
    chunk_size: int = 800,
    chunk_overlap: int = 200
) -> List[Chunk]:
    """
    Split a chapter into semantic chunks.

    Args:
        chapter: Chapter object to chunk
        chunk_size: Target size of each chunk in characters (default: 800)
        chunk_overlap: Overlap between chunks in characters (default: 200)

    Returns:
        List of Chunk objects
    """
    logger.info(f"Chunking chapter: {chapter.chapter_id} - {chapter.title}")

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],  # Preserve semantic boundaries
        is_separator_regex=False
    )

    # Split the content
    text_chunks = text_splitter.split_text(chapter.content)

    logger.info(f"Split chapter into {len(text_chunks)} chunks")

    # Create Chunk objects with metadata
    chunks = []
    for i, text in enumerate(text_chunks):
        # Extract section name from chunk
        section = extract_section_from_text(text)

        # Create chunk ID
        chunk_id = f"{chapter.chapter_id}-chunk-{i:03d}"

        # Build metadata
        metadata = {
            "chapter_id": chapter.chapter_id,
            "chapter_title": chapter.title,
            "chapter_number": chapter.chapter_number,
            "section": section,
            "chunk_index": i,
            "total_chunks": len(text_chunks),
            "text": text  # Store text in metadata for easy access
        }

        chunk = Chunk(
            id=chunk_id,
            text=text,
            metadata=metadata
        )
        chunks.append(chunk)

    logger.info(f"Created {len(chunks)} chunks for chapter {chapter.chapter_id}")

    return chunks


def chunk_all_chapters(chapters: List) -> List[Chunk]:
    """
    Chunk all chapters in the list.

    Args:
        chapters: List of Chapter objects

    Returns:
        List of all Chunk objects from all chapters
    """
    all_chunks = []

    for chapter in chapters:
        try:
            chunks = chunk_chapter(chapter)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Failed to chunk chapter {chapter.chapter_id}: {str(e)}")
            continue

    logger.info(f"Total chunks created: {len(all_chunks)}")

    return all_chunks
