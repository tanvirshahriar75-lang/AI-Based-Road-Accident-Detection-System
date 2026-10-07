# AI Pipeline

The staged computer-vision pipeline is:

1. Video/frame input
2. YOLO-compatible vehicle detection
3. Multi-object tracking
4. Temporal motion and interaction analysis
5. Accident-event confirmation
6. Evidence generation

## Vehicle detection

VehicleDetector provides a YOLO boundary. Real model weights are loaded only when a model path is configured. Road-relevant classes are filtered to car, motorcycle, bus, truck, and bicycle.

## Vehicle tracking

VehicleTracker provides an Ultralytics tracking adapter with ByteTrack and BoT-SORT support. Tracking calls use persistent state so track IDs can remain stable across sequential frames. The service also keeps bounded per-vehicle trajectories.

Each TrackState contains track ID, class, confidence, bounding box, center point, frame number, and timestamp. This is the temporal input required by the future accident analyzer.

No tracking accuracy, IDF1, MOTA, FPS, latency, or other performance result is claimed until the project runs a documented evaluation on real video data.
