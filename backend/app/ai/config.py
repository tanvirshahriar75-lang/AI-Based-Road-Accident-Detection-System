from typing import Literal

from pydantic import BaseModel, Field


class DetectorConfig(BaseModel):
    model_path: str | None = None
    confidence: float = Field(default=0.35, ge=0.0, le=1.0)
    device: str = "auto"
    image_size: int = Field(default=640, ge=32)


class TrackerConfig(BaseModel):
    model_path: str | None = None
    confidence: float = Field(default=0.35, ge=0.0, le=1.0)
    device: str = "auto"
    tracker: Literal["bytetrack.yaml", "botsort.yaml"] = "bytetrack.yaml"
    image_size: int = Field(default=640, ge=32)
    history_size: int = Field(default=100, ge=1, le=10000)
