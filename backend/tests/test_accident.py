from app.ai.accident import AccidentAnalyzer
from app.ai.tracker import TrackState

def state(track_id, cx, cy, timestamp, frame):
    return TrackState(track_id, 0, "car", 0.9, cx-10, cy-10, cx+10, cy+10, cx, cy, frame, timestamp)

def test_no_event_without_tracks():
    assert AccidentAnalyzer().analyze([]) is None

def test_sudden_deceleration_creates_candidate_event():
    history = {1: [state(1, 0, 0, 0.0, 1), state(1, 100, 0, 1.0, 2), state(1, 105, 0, 2.0, 3)]}
    event = AccidentAnalyzer(min_speed_change=50).analyze([history[1][-1]], history)
    assert event is not None
    assert event.track_ids == (1,)
    assert "sudden_deceleration" in event.reasons

def test_close_vehicle_interaction_creates_candidate_event():
    tracks = [state(1, 100, 100, 2.0, 2), state(2, 150, 100, 2.0, 2)]
    event = AccidentAnalyzer(proximity_threshold=60).analyze(tracks)
    assert event is not None
    assert event.track_ids == (1, 2)

def test_event_cooldown_suppresses_duplicate_events():
    tracks = [state(1, 100, 100, 2.0, 2), state(2, 150, 100, 2.0, 2)]
    analyzer = AccidentAnalyzer(proximity_threshold=60, cooldown_seconds=3)
    assert analyzer.analyze(tracks) is not None
    assert analyzer.analyze(tracks) is None

def test_no_event_when_vehicles_are_far_apart():
    tracks = [state(1, 0, 0, 2.0, 2), state(2, 500, 500, 2.0, 2)]
    assert AccidentAnalyzer(proximity_threshold=60).analyze(tracks) is None
