from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from ..config import settings
from .security import safe_filename

ALLOWED_VIDEO_TYPES = {"video/mp4", "video/avi", "video/x-msvideo", "video/quicktime", "video/webm", "video/mpeg"}
CHUNK_SIZE = 1024 * 1024

async def save_upload(upload: UploadFile, base_dir: Path) -> tuple[str, int]:
    if upload.content_type not in ALLOWED_VIDEO_TYPES:
        raise ValueError("Unsupported video type")
    base_dir.mkdir(parents=True, exist_ok=True)
    filename = safe_filename(upload.filename or "uploaded_video")
    destination = base_dir / f"{uuid4().hex}_{filename}"
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    total = 0
    try:
        with destination.open("wb") as output:
            while chunk := await upload.read(CHUNK_SIZE):
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("Video exceeds maximum upload size")
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await upload.close()
    return str(destination), total
