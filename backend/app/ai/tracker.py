from collections import deque
from dataclasses import dataclass
from typing import Any

VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck", "bicycle"}

@dataclass(frozen=True)
class TrackState:
    track_id: int
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float
    center_x: float
    center_y: float
    frame_number: int
    timestamp: float

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return (self.x1, self.y1, self.x2, self.y2)

class VehicleTracker:
    """YOLO multi-object tracking adapter with ByteTrack/BoT-SORT support."""
    SUPPORTED_TRACKERS = {"bytetrack.yaml", "botsort.yaml"}

    def __init__(self, model_path: str | None = None, confidence: float = 0.35,
                 device: str = "auto", tracker_config: str = "bytetrack.yaml",
                 image_size: int = 640, history_size: int = 100):
        if tracker_config not in self.SUPPORTED_TRACKERS:
            raise ValueError(f"Unsupported tracker: {tracker_config}")
        if history_size < 1:
            raise ValueError("history_size must be at least 1")
        self.model_path = model_path
        self.confidence = confidence
        self.device = device
        self.tracker_config = tracker_config
        self.image_size = image_size
        self.history_size = history_size
        self._model: Any = None
        self._history: dict[int, deque[TrackState]] = {}

    def load(self) -> None:
        if not self.model_path:
            raise RuntimeError("No tracker model path configured")
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("Ultralytics is not installed") from exc
        self._model = YOLO(self.model_path)

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def update(self, frame: Any, frame_number: int, timestamp: float) -> list[TrackState]:
        if not self.is_loaded:
            raise RuntimeError("Tracker model is not loaded")
        results = self._model.track(
            source=frame, persist=True, tracker=self.tracker_config,
            conf=self.confidence,
            device=None if self.device == "auto" else self.device,
            imgsz=self.image_size, verbose=False,
        )
        if not results:
            return []
        result = results[0]
        boxes = getattr(result, "boxes", None)
        names = getattr(result, "names", {})
        if boxes is None or getattr(boxes, "id", None) is None:
            return []

        tracks: list[TrackState] = []
        for index, track_id_value in enumerate(boxes.id.tolist()):
            track_id = int(track_id_value)
            cls_id = int(boxes.cls[index].item())
            confidence = float(boxes.conf[index].item())
            class_name = str(names.get(cls_id, cls_id)).lower()
            if class_name not in VEHICLE_CLASSES:
                continue
            x1, y1, x2, y2 = (float(v) for v in boxes.xyxy[index].tolist())
            state = TrackState(
                track_id=track_id, class_id=cls_id, class_name=class_name,
                confidence=confidence, x1=x1, y1=y1, x2=x2, y2=y2,
                center_x=(x1 + x2) / 2, center_y=(y1 + y2) / 2,
                frame_number=frame_number, timestamp=timestamp,
            )
            self._history.setdefault(track_id, deque(maxlen=self.history_size)).append(state)
            tracks.append(state)
        return tracks

    def get_trajectory(self, track_id: int) -> list[TrackState]:
        return list(self._history.get(track_id, ()))

    def reset(self) -> None:
        self._history.clear()
