# Dataset Preparation Guide

This project separates **vehicle detection data** from **accident-event evaluation data**. Do not treat ordinary vehicle labels as accident labels.

## 1. Suggested dataset layout

Keep downloaded datasets outside Git unless the license explicitly permits redistribution.

```text
datasets/
  vehicle_detection/
    images/
      train/
      val/
      test/
    labels/
      train/
      val/
      test/
    data.yaml
  accident_events/
    videos/
    annotations/
      ground_truth.jsonl
      predictions.jsonl
    splits/
      videos.csv
```

The repository's `datasets/` directory is intended for local data and should not contain private, licensed, or very large raw videos.

## 2. Dataset selection and licensing

Before using any dataset, record:
- dataset name, publisher, version, download/source URL and access date;
- license and whether academic use, modification, and redistribution are allowed;
- number of videos, duration, resolution, frame rate and camera/viewpoint characteristics;
- annotation classes, annotation method and known limitations.

Use publicly available, appropriately licensed traffic/accident data. Do not scrape private CCTV, publish identifiable people/vehicle plates, or redistribute datasets without permission. Blur faces and license plates when sharing sample evidence where feasible.

## 3. Avoid data leakage

Split by **original video or recording source**, not by individual frames. Adjacent frames from one recording must never appear in both training and test sets. Keep a final test split untouched until model selection is complete. Record the random seed and split manifest.

Use `python ai/scripts/split_dataset.py --input videos.csv --output-dir datasets/accident_events/splits` to create a reproducible group-level split. CSV columns: `video_id,label`; optional `source_group` keeps recordings from the same camera/session together.

## 4. Vehicle detection annotations

For Ultralytics YOLO detection, each image has a matching text file. Each row is:

```text
class_id x_center y_center width height
```

Coordinates are normalized to [0, 1]. The class order must be identical to `data.yaml`. Example classes can include car, motorcycle, bus and truck; document any class mapping from the source dataset.

## 5. Accident-event annotations

Use JSON Lines (one JSON object per line), following `annotations.schema.json`. Required fields:
- `video_id`: stable ID matching the video manifest;
- `timestamp_sec`: event time in seconds from video start;
- `event_type`: for example `collision`, `near_miss`, or `unknown`;
- `involved_track_ids`: optional list of tracker IDs when available;
- `annotator` and `notes`: provenance and ambiguity notes.

Have two annotators independently label a subset, resolve disagreements, and document the event definition and matching tolerance before evaluation.

## 6. Reporting

Report dataset counts by split and class, annotation protocol, event definition, matching tolerance, and limitations. For event detection, report precision, recall and F1 with the chosen temporal tolerance. For vehicle detection, report the detector's standard mAP/precision/recall from its training/evaluation tool. Never mix metrics from different datasets or splits.

No dataset is bundled with this repository and no model performance is claimed by these templates.
