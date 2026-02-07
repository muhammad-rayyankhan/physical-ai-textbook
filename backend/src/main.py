from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# Create FastAPI application
app = FastAPI(
    title="RAG Chatbot API",
    description="API for Physical AI & Humanoid Robotics textbook Q&A chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "RAG Chatbot API for Physical AI & Humanoid Robotics Textbook",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


# Initialize database on startup
from src.core.database import init_db

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    init_db()

# Include routers
from src.api.routes import health, chat, auth
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api", tags=["authentication"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
