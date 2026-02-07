"""
Demo LLM Service

Returns pre-written answers instantly for demonstration purposes.
Use this when Ollama is too slow.
"""

from typing import List, Dict, Any
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
            "chunk_index": chunk_index
        }


# Pre-written demo answers
DEMO_ANSWERS = {
    "physical ai": """Physical AI refers to artificial intelligence systems that interact with and operate in the physical world through embodied agents like robots. Unlike traditional AI that exists purely in software, Physical AI combines perception, reasoning, and action to enable machines to understand and manipulate their environment.

According to Chapter 1, Physical AI systems integrate sensors for perception, actuators for movement, and intelligent control systems to achieve autonomous behavior in real-world settings. This field is crucial for developing humanoid robots and other embodied AI systems.""",

    "sensor": """Sensors are devices that enable robots to perceive their environment by converting physical phenomena into electrical signals. Chapter 2 explains that robots use various types of sensors including cameras for vision, LIDAR for distance measurement, IMUs for orientation, and tactile sensors for touch.

These sensors provide the raw data that robots need to understand their surroundings, detect obstacles, recognize objects, and navigate safely. Sensor fusion techniques combine data from multiple sensors to create a more complete and accurate understanding of the environment.""",

    "actuator": """Actuators are the components that enable robots to move and interact with the physical world. As described in Chapter 3, actuators convert electrical energy into mechanical motion, allowing robots to walk, grasp objects, and perform tasks.

Common types include electric motors (DC, servo, stepper), hydraulic actuators for high-force applications, and pneumatic actuators for compliant movements. The choice of actuator depends on factors like required force, speed, precision, and the robot's size and application.""",

    "learning": """Robot learning refers to techniques that enable robots to improve their performance through experience. Chapter 4 covers various approaches including reinforcement learning, where robots learn through trial and error, imitation learning where they learn from demonstrations, and supervised learning for pattern recognition tasks.

Modern approaches often combine deep learning with traditional robotics to enable robots to learn complex behaviors like manipulation, navigation, and human-robot interaction. This is essential for creating adaptive robots that can handle diverse and unpredictable environments.""",

    "default": """Based on the textbook content, Physical AI and Humanoid Robotics is an interdisciplinary field that combines artificial intelligence, mechanical engineering, and control systems to create intelligent machines that can operate in the physical world.

The textbook covers key topics including sensors and perception (Chapter 2), actuation and control (Chapter 3), learning and intelligence (Chapter 4), system integration (Chapter 5), and future directions and ethical considerations (Chapter 6). For more specific information, please ask about a particular topic like sensors, actuators, learning, or ethics."""
}


class LLMService:
    """
    Demo LLM Service that returns pre-written answers instantly.

    Use this for demonstrations when Ollama is too slow.
    """

    def __init__(self):
        """Initialize demo service."""
        logger.info("Initialized DEMO LLM service (instant responses)")

    def generate_answer(
        self,
        question: str,
        context: str,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> str:
        """
        Return a pre-written demo answer based on the question.

        Args:
            question: User's question
            context: Retrieved context (not used in demo mode)
            temperature: Not used in demo mode
            max_tokens: Not used in demo mode

        Returns:
            Pre-written demo answer
        """
        logger.info(f"Generating DEMO answer for question: {question[:100]}...")

        # Match question to demo answer
        question_lower = question.lower()

        for keyword, answer in DEMO_ANSWERS.items():
            if keyword in question_lower:
                logger.info(f"Matched keyword: {keyword}")
                return answer

        # Default answer
        logger.info("Using default demo answer")
        return DEMO_ANSWERS["default"]

    def extract_citations(
        self,
        answer: str,
        sources: List[Dict[str, Any]]
    ) -> List[Citation]:
        """Extract citations from sources."""
        citations = []
        seen_chapters = set()

        for source in sources[:3]:
            chapter_id = source.get("chapter_id", "")
            if chapter_id not in seen_chapters:
                citation = Citation(
                    chapter_id=chapter_id,
                    chapter_title=source.get("chapter_title", ""),
                    section=source.get("section", ""),
                    chunk_index=source.get("chunk_index", 0)
                )
                citations.append(citation)
                seen_chapters.add(chapter_id)

        logger.info(f"Extracted {len(citations)} citations")
        return citations

    def check_health(self) -> bool:
        """Demo service is always healthy."""
        return True


# Global service instance
llm_service = LLMService()
