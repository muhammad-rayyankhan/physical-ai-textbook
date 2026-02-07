from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Textbook API"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://*.vercel.app"]

    # Database (Neon)
    DATABASE_URL: str

    # Qdrant Vector Store
    QDRANT_URL: str
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "textbook_embeddings"

    # Auth
    AUTH_SECRET: str

    # AI Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
