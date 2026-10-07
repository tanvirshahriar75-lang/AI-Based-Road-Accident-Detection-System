# AI Pipeline

The staged computer-vision pipeline is:

1. Video/frame input
2. YOLO-compatible vehicle detection
3. Multi-object tracking
4. Temporal motion and interaction analysis
5. Accident-event confirmation
6. Evidence generation

VehicleTracker provides persistent track IDs and bounded trajectories using ByteTrack or BoT-SORT through Ultralytics.

AccidentAnalyzer is an explainable baseline using trajectory-derived sudden deceleration and close-vehicle interaction signals. It emits involved track IDs, confidence, timestamp, and reasons, with a cooldown to reduce duplicate events.

This is not a trained accident classifier. No accident-detection accuracy, precision, recall, F1, mAP, FPS, latency, or other performance result is claimed until documented real-video evaluation is completed.
