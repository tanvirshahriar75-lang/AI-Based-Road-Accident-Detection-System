import pytest

from app.ai.tracker import TrackState, VehicleTracker


class FakeValue:
    def __init__(self, value):
        self.value = value

    def item(self):
        return self.value

    def tolist(self):
        return self.value


class FakeBoxes:
    def __init__(self, track_ids, classes, confidences, coordinates):
        self.id = FakeValue(track_ids)
        self.cls = [FakeValue(v) for v in classes]
        self.conf = [FakeValue(v) for v in confidences]
        self.xyxy = [FakeValue(v) for v in coordinates]


class FakeResult:
    names = {0: "car", 1: "person"}

    def __init__(self, boxes):
        self.boxes = boxes


class FakeModel:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def track(self, **kwargs):
        self.calls.append(kwargs)
        return [self.results[len(self.calls) - 1]]


def test_tracker_requires_model_before_update():
    tracker = VehicleTracker()
    with pytest.raises(RuntimeError, match="model is not loaded"):
        tracker.update(None, 1, 0.0)


def test_tracker_rejects_unknown_backend():
    with pytest.raises(ValueError, match="Unsupported tracker"):
        VehicleTracker(tracker_config="unknown.yaml")


def test_track_state_center_is_calculated():
    state = TrackState(1, 0, "car", 0.9, 10, 20, 30, 60, 20, 40, 1, 0.1)
    assert state.bbox == (10, 20, 30, 60)
    assert (state.center_x, state.center_y) == (20, 40)


def test_tracker_preserves_id_and_accumulates_trajectory():
    first = FakeResult(FakeBoxes([7], [0], [0.91], [[10, 20, 30, 60]]))
    second = FakeResult(FakeBoxes([7], [0], [0.88], [[14, 24, 34, 64]]))
    model = FakeModel([first, second])

    tracker = VehicleTracker(history_size=3)
    tracker._model = model

    tracks1 = tracker.update("frame-1", 1, 0.1)
    tracks2 = tracker.update("frame-2", 2, 0.2)

    assert tracks1[0].track_id == 7
    assert tracks2[0].track_id == 7
    assert tracks2[0].center_x == 24
    trajectory = tracker.get_trajectory(7)
    assert len(trajectory) == 2
    assert [point.frame_number for point in trajectory] == [1, 2]
    assert model.calls[0]["tracker"] == "bytetrack.yaml"
    assert model.calls[0]["persist"] is True


def test_tracker_ignores_non_vehicle_classes():
    result = FakeResult(FakeBoxes([1], [1], [0.99], [[1, 2, 3, 4]]))
    tracker = VehicleTracker()
    tracker._model = FakeModel([result])
    assert tracker.update("frame", 1, 0.0) == []
    assert tracker.get_trajectory(1) == []


def test_tracker_history_is_bounded():
    results = [
        FakeResult(FakeBoxes([4], [0], [0.9], [[n, 0, n + 10, 10]]))
        for n in range(4)
    ]
    tracker = VehicleTracker(history_size=2)
    tracker._model = FakeModel(results)

    for frame_number in range(1, 5):
        tracker.update("frame", frame_number, frame_number / 10)

    assert [p.frame_number for p in tracker.get_trajectory(4)] == [3, 4]
