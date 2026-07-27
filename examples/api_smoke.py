#!/usr/bin/env python3
"""Dependency-free HTTP endpoint smoke check with machine-readable output."""

import argparse
import json
import time
import urllib.error
import urllib.request


def check(url, expected_status=200, timeout=10):
    started = time.monotonic()
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
            status = response.status
            content_type = response.headers.get("content-type", "")
        result = {
            "url": url,
            "status": status,
            "expected_status": expected_status,
            "ok": status == expected_status,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
            "bytes": len(body),
            "content_type": content_type,
        }
    except (urllib.error.URLError, TimeoutError) as error:
        result = {
            "url": url,
            "status": None,
            "expected_status": expected_status,
            "ok": False,
            "elapsed_ms": round((time.monotonic() - started) * 1000, 2),
            "error": str(error),
        }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--expected-status", type=int, default=200)
    parser.add_argument("--timeout", type=float, default=10)
    args = parser.parse_args()
    result = check(args.url, args.expected_status, args.timeout)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()

