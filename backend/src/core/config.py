from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration (PostgreSQL)
    DATABASE_URL: str

    # Qdrant Cloud Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION: str = "textbook_chunks"

    # Groq Configuration (free, fast LLM inference)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-70b-versatile"

    # Hugging Face Configuration (free embeddings)
    HUGGINGFACE_API_KEY: str = ""

    # OpenAI Configuration (optional - only needed if USE_OPENAI_* flags are true)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Feature Flags
    USE_OPENAI_EMBEDDINGS: bool = False
    USE_OPENAI_LLM: bool = False

    # Authentication
    AUTH_SECRET: str
    AUTH_URL: str = "http://localhost:8000"

    # Legacy Local Configuration (for backward compatibility)
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    CHROMA_COLLECTION_LEGACY: str = "textbook_chunks"

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: str = "development"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        # Look for .env file in the backend directory
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        case_sensitive = True


# Global settings instance
settings = Settings()
