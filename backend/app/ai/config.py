from pydantic import BaseModel, Field

class DetectorConfig(BaseModel):
    model_path: str | None = None
    confidence: float = Field(default=0.35, ge=0.0, le=1.0)
    device: str = "auto"
    image_size: int = Field(default=640, ge=32)
