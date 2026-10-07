from ..models.accident import Accident

class PersistenceService:
    @staticmethod
    def build_event(video_id, event, evidence_path=None):
        return Accident(video_id=video_id, confidence=event.confidence, detected_at_seconds=event.timestamp, evidence_path=evidence_path, description=", ".join(event.reasons))
