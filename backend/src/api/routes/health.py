from fastapi import APIRouter
from src.models.chat import HealthResponse
from src.services.rag import rag_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns the health status of the API and its dependencies.
    """
    try:
        # Check all RAG pipeline components
        service_health = rag_service.check_health()

        # Determine overall status
        all_healthy = all("up" in status for status in service_health.values())
        overall_status = "healthy" if all_healthy else "degraded"

        return HealthResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat() + "Z",
            services={
                "database": "up",  # Assuming DB is up if we can respond
                "vector_store": service_health.get("vector_store", "unknown"),
                "llm": service_health.get("llm", "unknown"),
                "embeddings": service_health.get("embeddings", "unknown")
            },
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat() + "Z",
            services={
                "database": "unknown",
                "vector_store": "unknown",
                "llm": "unknown",
                "embeddings": "unknown"
            },
            version="1.0.0"
        )
