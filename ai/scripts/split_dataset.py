#!/usr/bin/env python3
"""Create deterministic, source-group-safe train/val/test CSV manifests."""

from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path


def split_rows(rows: list[dict[str, str]], seed: int) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        group = (row.get("source_group") or "").strip() or row["video_id"]
        groups[group].append(row)

    keys = sorted(groups)
    random.Random(seed).shuffle(keys)
    total = len(keys)
    train_end = round(total * 0.70)
    val_end = train_end + round(total * 0.15)
    # Ensure each split is non-empty when at least three groups exist.
    if total >= 3:
        train_end = max(1, min(train_end, total - 2))
        val_end = max(train_end + 1, min(val_end, total - 1))

    assigned = {"train": keys[:train_end], "val": keys[train_end:val_end], "test": keys[val_end:]}
    return {
        split: [row for key in group_keys for row in groups[key]]
        for split, group_keys in assigned.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="CSV with video_id,label and optional source_group")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    with args.input.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"video_id", "label"}.issubset(reader.fieldnames):
            raise SystemExit("Input CSV must contain video_id,label columns")
        rows = list(reader)

    if not rows:
        raise SystemExit("Input CSV has no data rows")
    if any(not row.get("video_id", "").strip() for row in rows):
        raise SystemExit("Every row must have a non-empty video_id")
    if len({row["video_id"] for row in rows}) != len(rows):
        raise SystemExit("Each video_id must appear only once in the manifest")

    splits = split_rows(rows, args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, split_rows_ in splits.items():
        output = args.output_dir / f"{name}.csv"
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(split_rows_)

    print(f"Created manifests in {args.output_dir} (seed={args.seed})")
    for name, items in splits.items():
        print(f"{name}: {len(items)} videos")


if __name__ == "__main__":
    main()
