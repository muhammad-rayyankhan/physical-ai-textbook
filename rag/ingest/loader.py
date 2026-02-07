"""
Markdown Loader

Loads and parses markdown files from the textbook documentation.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import re
import logging

logger = logging.getLogger(__name__)


class Chapter:
    """Represents a single chapter from the textbook."""

    def __init__(
        self,
        chapter_id: str,
        chapter_number: int,
        title: str,
        content: str,
        metadata: Dict[str, Any]
    ):
        self.chapter_id = chapter_id
        self.chapter_number = chapter_number
        self.title = title
        self.content = content
        self.metadata = metadata

    def __repr__(self):
        return f"<Chapter(id={self.chapter_id}, title={self.title})>"


def parse_frontmatter(content: str) -> tuple[Dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown content.

    Args:
        content: Raw markdown content

    Returns:
        Tuple of (metadata dict, content without frontmatter)
    """
    metadata = {}

    # Check for frontmatter (--- at start)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            content = parts[2].strip()

            # Parse simple YAML (key: value pairs)
            for line in frontmatter.split("\n"):
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value

    return metadata, content


def load_chapter(file_path: Path) -> Chapter:
    """
    Load a single chapter from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Chapter object
    """
    logger.info(f"Loading chapter from: {file_path}")

    # Read file content
    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # Parse frontmatter
    metadata, content = parse_frontmatter(raw_content)

    # Extract chapter info from path (e.g., chapter-01/index.md)
    chapter_dir = file_path.parent.name
    if chapter_dir.startswith("chapter-"):
        chapter_id = chapter_dir
        chapter_number = int(chapter_dir.split("-")[1])
    else:
        # Fallback for non-standard paths
        chapter_id = file_path.stem
        chapter_number = 0

    # Get title from metadata or extract from first heading
    title = metadata.get("title", "")
    if not title:
        # Try to find first # heading
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
        else:
            title = f"Chapter {chapter_number}"

    logger.info(f"Loaded chapter: {chapter_id} - {title}")

    return Chapter(
        chapter_id=chapter_id,
        chapter_number=chapter_number,
        title=title,
        content=content,
        metadata=metadata
    )


def load_all_chapters(docs_dir: str) -> List[Chapter]:
    """
    Load all chapters from the documentation directory.

    Args:
        docs_dir: Path to the docs directory (e.g., "website/docs")

    Returns:
        List of Chapter objects, sorted by chapter number
    """
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Documentation directory not found: {docs_dir}")

    logger.info(f"Loading chapters from: {docs_dir}")

    chapters = []

    # Find all chapter directories (chapter-01, chapter-02, etc.)
    chapter_dirs = sorted([d for d in docs_path.iterdir() if d.is_dir() and d.name.startswith("chapter-")])

    for chapter_dir in chapter_dirs:
        # Look for index.md in each chapter directory
        index_file = chapter_dir / "index.md"

        if index_file.exists():
            try:
                chapter = load_chapter(index_file)
                chapters.append(chapter)
            except Exception as e:
                logger.error(f"Failed to load chapter from {index_file}: {str(e)}")
                continue
        else:
            logger.warning(f"No index.md found in {chapter_dir}")

    # Sort by chapter number
    chapters.sort(key=lambda c: c.chapter_number)

    logger.info(f"Loaded {len(chapters)} chapters")

    return chapters
