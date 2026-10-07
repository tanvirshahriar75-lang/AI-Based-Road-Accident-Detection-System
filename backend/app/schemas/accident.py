from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    video_id: int
    confidence: float
    detected_at_seconds: float | None
    evidence_path: str | None
    description: str | None
    created_at: datetime


class AccidentListResponse(BaseModel):
    items: list[AccidentResponse]
    total: int
