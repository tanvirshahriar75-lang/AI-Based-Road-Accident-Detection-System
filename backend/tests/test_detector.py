import pytest
from app.ai.detector import VehicleDetector, VEHICLE_CLASSES


def test_vehicle_classes_are_defined():
    assert {"car", "motorcycle", "bus", "truck", "bicycle"}.issubset(VEHICLE_CLASSES)


def test_detector_requires_model_before_prediction():
    detector = VehicleDetector()
    assert not detector.is_loaded
    with pytest.raises(RuntimeError, match="model is not loaded"):
        detector.predict(None)


def test_detector_load_requires_model_path():
    with pytest.raises(RuntimeError, match="model path"):
        VehicleDetector().load()
