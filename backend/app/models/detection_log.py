from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class DetectionLog(Base):
    __tablename__ = "detection_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    video_id: Mapped[int | None] = mapped_column(ForeignKey("videos.id"), nullable=True, index=True)
    track_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    class_name: Mapped[str] = mapped_column(String(80), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    frame_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    detected_at_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
