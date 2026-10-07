from dataclasses import dataclass
from math import hypot
from typing import Sequence

from .tracker import TrackState

@dataclass(frozen=True)
class AccidentEvent:
    track_ids: tuple[int, ...]
    confidence: float
    timestamp: float
    reasons: tuple[str, ...]

class AccidentAnalyzer:
    """Explainable temporal baseline for potential accident events."""

    def __init__(self, min_speed_change: float = 20.0, proximity_threshold: float = 80.0,
                 min_confidence: float = 0.65, cooldown_seconds: float = 2.0):
        if not 0 <= min_confidence <= 1:
            raise ValueError("min_confidence must be between 0 and 1")
        if min_speed_change < 0 or proximity_threshold <= 0 or cooldown_seconds < 0:
            raise ValueError("accident thresholds must be non-negative")
        self.min_speed_change = min_speed_change
        self.proximity_threshold = proximity_threshold
        self.min_confidence = min_confidence
        self.cooldown_seconds = cooldown_seconds
        self._last_event_time: float | None = None

    @staticmethod
    def _speed(previous: TrackState, current: TrackState) -> float:
        dt = current.timestamp - previous.timestamp
        if dt <= 0:
            return 0.0
        return hypot(current.center_x - previous.center_x, current.center_y - previous.center_y) / dt

    def analyze(self, tracks: Sequence[TrackState],
                trajectories: dict[int, Sequence[TrackState]] | None = None) -> AccidentEvent | None:
        if not tracks:
            return None
        reasons: list[str] = []
        involved: set[int] = set()
        history = trajectories or {}

        for current in tracks:
            points = list(history.get(current.track_id, ()))
            if len(points) < 2:
                continue
            previous = points[-2]
            current_speed = self._speed(previous, current)
            prior_speed = self._speed(points[-3], previous) if len(points) >= 3 else 0.0
            if prior_speed - current_speed >= self.min_speed_change:
                involved.add(current.track_id)
                reasons.append("sudden_deceleration")

        for index, first in enumerate(tracks):
            for second in tracks[index + 1:]:
                distance = hypot(first.center_x - second.center_x, first.center_y - second.center_y)
                if distance <= self.proximity_threshold:
                    involved.update((first.track_id, second.track_id))
                    reasons.append("close_vehicle_interaction")

        if not reasons or not involved:
            return None

        unique_reasons = tuple(dict.fromkeys(reasons))
        score = min(1.0, 0.55 + 0.15 * len(unique_reasons) + 0.05 * min(len(involved), 4))
        timestamp = max(track.timestamp for track in tracks)
        if score < self.min_confidence:
            return None
        if self._last_event_time is not None and timestamp - self._last_event_time < self.cooldown_seconds:
            return None

        self._last_event_time = timestamp
        return AccidentEvent(tuple(sorted(involved)), score, timestamp, unique_reasons)

    def reset(self) -> None:
        self._last_event_time = None
