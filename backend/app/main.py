from fastapi import FastAPI
from .config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI-based road accident detection platform.",
)

@app.get("/api/health", tags=["system"])
def health():
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}
