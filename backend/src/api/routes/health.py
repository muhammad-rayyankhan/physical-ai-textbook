from fastapi import APIRouter
from src.models.chat import HealthResponse
from datetime import datetime

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns the health status of the API and its dependencies.
    """
    # TODO: Add actual health checks for Qdrant, Neon, OpenAI when services are implemented
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        services={
            "database": "unknown",  # Will check after database connection is configured
            "vector_db": "unknown",  # Will check after Qdrant is configured
            "llm": "unknown"  # Will check after OpenAI is configured
        },
        version="1.0.0"
    )
