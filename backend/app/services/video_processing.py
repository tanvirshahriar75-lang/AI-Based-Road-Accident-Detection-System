from sqlalchemy.orm import Session
from ..models.video import Video, VideoStatus

class VideoProcessingService:
    """Coordinates processing without coupling the API to the future AI pipeline."""

    def queue(self, db: Session, video: Video) -> Video:
        video.status = VideoStatus.queued
        db.add(video)
        db.commit()
        db.refresh(video)
        return video
