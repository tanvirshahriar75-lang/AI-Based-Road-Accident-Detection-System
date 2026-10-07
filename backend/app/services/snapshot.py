from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2] / "data" / "evidence"

class SnapshotStore:
    def __init__(self, root: Path = ROOT):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, frame, video_id: int, timestamp: float) -> str:
        import cv2
        path = self.root / f"video-{video_id}-{timestamp:.3f}-{uuid4().hex}.jpg"
        if not cv2.imwrite(str(path), frame):
            raise RuntimeError("Unable to write snapshot")
        return str(path)

    def resolve(self, stored_path: str | None) -> Path | None:
        if not stored_path:
            return None
        root = self.root.resolve()
        path = Path(stored_path).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return None
        return path
