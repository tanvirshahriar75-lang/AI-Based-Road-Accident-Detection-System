from datetime import datetime
from pydantic import BaseModel, ConfigDict
from ..models.video import VideoStatus

class VideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    content_type: str
    status: VideoStatus
    created_at: datetime

class VideoListResponse(BaseModel):
    items: list[VideoResponse]
    total: int
