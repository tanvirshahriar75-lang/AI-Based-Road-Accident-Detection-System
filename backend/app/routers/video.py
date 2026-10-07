from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models.user import User
from ..models.video import Video, VideoStatus
from ..schemas.video import VideoListResponse, VideoResponse
from ..services.auth import decode_access_token
from ..services.video import save_upload

router = APIRouter(prefix="/api/v1/videos", tags=["videos"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "data" / "uploads"


def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id = decode_access_token(token)
    user = db.get(User, user_id) if user_id else None
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

@router.post("/upload", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...), user: User = Depends(current_user), db: Session = Depends(get_db)):
    try:
        storage_path, _ = await save_upload(file, UPLOAD_DIR)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    video = Video(owner_id=user.id, filename=file.filename or "uploaded_video", storage_path=storage_path, content_type=file.content_type or "application/octet-stream", status=VideoStatus.uploaded)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

@router.get("", response_model=VideoListResponse)
def list_videos(user: User = Depends(current_user), db: Session = Depends(get_db)):
    items = list(db.scalars(select(Video).where(Video.owner_id == user.id).order_by(Video.created_at.desc())))
    return VideoListResponse(items=items, total=len(items))

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    video = db.scalar(select(Video).where(Video.id == video_id, Video.owner_id == user.id))
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    video = db.scalar(select(Video).where(Video.id == video_id, Video.owner_id == user.id))
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    Path(video.storage_path).unlink(missing_ok=True)
    db.delete(video)
    db.commit()

@router.post("/{video_id}/process", response_model=VideoResponse)
def process_video(video_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    video = db.scalar(select(Video).where(Video.id == video_id, Video.owner_id == user.id))
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    if not Path(video.storage_path).is_file():
        raise HTTPException(status_code=409, detail="Stored video file is missing")
    if video.status in {VideoStatus.queued, VideoStatus.processing}:
        raise HTTPException(status_code=409, detail="Video is already being processed")
    video.status = VideoStatus.queued
    db.commit()
    db.refresh(video)
    return video
