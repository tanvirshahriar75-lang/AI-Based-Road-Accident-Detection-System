#!/usr/bin/env python3
"""Evaluate predicted accident events against ground truth using time tolerance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(item.get("video_id"), str) or not item["video_id"]:
                raise ValueError(f"{path}:{line_number}: video_id must be a non-empty string")
            if not isinstance(item.get("timestamp_sec"), (int, float)) or item["timestamp_sec"] < 0:
                raise ValueError(f"{path}:{line_number}: timestamp_sec must be a non-negative number")
            events.append(item)
    return events


def evaluate(ground_truth: list[dict[str, Any]], predictions: list[dict[str, Any]], tolerance: float) -> dict[str, float | int]:
    unmatched = set(range(len(ground_truth)))
    true_positive = 0

    # Match each prediction to the nearest still-unmatched GT event in the same video.
    for prediction in sorted(predictions, key=lambda e: (e["video_id"], e["timestamp_sec"])):
        candidates = [
            (abs(float(prediction["timestamp_sec"]) - float(ground_truth[i]["timestamp_sec"])), i)
            for i in unmatched
            if ground_truth[i]["video_id"] == prediction["video_id"]
            and (
                "event_type" not in prediction
                or "event_type" not in ground_truth[i]
                or prediction["event_type"] == ground_truth[i]["event_type"]
            )
        ]
        if not candidates:
            continue
        distance, index = min(candidates)
        if distance <= tolerance:
            unmatched.remove(index)
            true_positive += 1

    false_positive = len(predictions) - true_positive
    false_negative = len(ground_truth) - true_positive
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tolerance_seconds": tolerance,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", required=True, type=Path)
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--tolerance", type=float, default=2.0, help="Maximum event timestamp difference in seconds")
    args = parser.parse_args()
    if args.tolerance < 0:
        raise SystemExit("--tolerance must be >= 0")

    metrics = evaluate(load_jsonl(args.ground_truth), load_jsonl(args.predictions), args.tolerance)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
