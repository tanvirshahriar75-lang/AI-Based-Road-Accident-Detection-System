# System Architecture

## Pipeline

1. Ingest uploaded or camera video.
2. Extract frames.
3. Detect vehicles with a YOLO-based detector.
4. Track vehicle identities across frames.
5. Analyze proximity, motion, and interactions.
6. Confirm candidate accidents over a temporal window.
7. Calculate an event confidence score.
8. Save evidence frames/clips and an accident event.
9. Expose events through the API and dashboard.

## Design principle

The detection pipeline is separated into detector, tracker, analysis, and persistence services so individual research components can be evaluated independently.
