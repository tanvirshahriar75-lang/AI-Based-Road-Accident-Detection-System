from dataclasses import dataclass
from typing import Any

VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck", "bicycle"}

@dataclass(frozen=True)
class Detection:
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float

class VehicleDetector:
    """YOLO-compatible detector boundary. Model weights are loaded only when supplied."""
    def __init__(self, model_path: str | None = None, confidence: float = 0.35, device: str = "auto"):
        self.model_path = model_path
        self.confidence = confidence
        self.device = device
        self._model: Any = None

    def load(self) -> None:
        if not self.model_path:
            raise RuntimeError("No detector model path configured")
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("Ultralytics is not installed") from exc
        self._model = YOLO(self.model_path)

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, frame: Any) -> list[Detection]:
        if not self.is_loaded:
            raise RuntimeError("Detector model is not loaded")
        results = self._model.predict(source=frame, conf=self.confidence, device=None if self.device == "auto" else self.device, verbose=False)
        detections: list[Detection] = []
        names = getattr(results[0], "names", {}) if results else {}
        boxes = getattr(results[0], "boxes", None) if results else None
        if boxes is None:
            return detections
        for box in boxes:
            cls_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            name = str(names.get(cls_id, cls_id)).lower()
            if name not in VEHICLE_CLASSES:
                continue
            coords = [float(v) for v in box.xyxy[0].tolist()]
            detections.append(Detection(cls_id, name, confidence, *coords))
        return detections
