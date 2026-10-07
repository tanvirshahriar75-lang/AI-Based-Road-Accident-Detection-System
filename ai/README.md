# AI Pipeline

The staged computer-vision pipeline is:

1. Video/frame input
2. YOLO-compatible vehicle detection
3. Multi-object tracking
4. Temporal motion and interaction analysis
5. Accident-event confirmation
6. Evidence generation

Vehicle detection is implemented behind `VehicleDetector` in the backend AI layer. Ultralytics YOLO weights are loaded only when a real model path is configured. Road-relevant classes are filtered to car, motorcycle, bus, truck, and bicycle.

No model accuracy, mAP, precision, recall, or other performance result is claimed until the project runs a documented evaluation on a real dataset.
