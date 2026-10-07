from fastapi import FastAPI
from .config import settings
from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.video import router as video_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="0.2.0",
    description="AI-based road accident detection platform.",
)
app.include_router(auth_router)
app.include_router(video_router)

@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}
