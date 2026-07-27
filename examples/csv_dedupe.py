#!/usr/bin/env python3
"""Small dependency-free CSV deduplicator used as a buyer-verifiable example."""

import argparse
import csv
from pathlib import Path


def deduplicate(rows, keys, keep="first"):
    """Return rows deduplicated by ``keys`` while preserving stable order."""
    materialized = list(rows)
    if keep == "last":
        materialized.reverse()

    seen = set()
    kept = []
    for row in materialized:
        identity = tuple(row[key] for key in keys)
        if identity not in seen:
            seen.add(identity)
            kept.append(row)

    if keep == "last":
        kept.reverse()
    return kept


def run(source, destination, keys, keep="first"):
    with Path(source).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV must contain a header row")
        missing = [key for key in keys if key not in reader.fieldnames]
        if missing:
            raise ValueError(f"unknown key columns: {', '.join(missing)}")
        fieldnames = reader.fieldnames
        rows = list(reader)

    kept = deduplicate(rows, keys, keep)
    with Path(destination).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept)

    return {"input_rows": len(rows), "output_rows": len(kept)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--keys", required=True, help="comma-separated column names")
    parser.add_argument("--keep", choices=("first", "last"), default="first")
    args = parser.parse_args()
    result = run(
        args.source,
        args.destination,
        [key.strip() for key in args.keys.split(",") if key.strip()],
        args.keep,
    )
    print(f"{result['input_rows']} rows -> {result['output_rows']} rows")


if __name__ == "__main__":
    main()

