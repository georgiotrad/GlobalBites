"""Lightweight repeated health observation for Week 5 evidence.

Usage:
    python scripts/monitor.py https://your-live-url [checks] [interval_seconds]

Example:
    python scripts/monitor.py https://globalbites.example 6 10
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

base = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000").rstrip("/")
checks = int(sys.argv[2]) if len(sys.argv) > 2 else 6
interval = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0

failures = 0
for index in range(checks):
    stamp = datetime.now(timezone.utc).isoformat()
    try:
        with urlopen(base + "/api/health", timeout=15) as response:
            payload = json.loads(response.read().decode())
            ok = response.status == 200 and payload.get("status") == "healthy"
            print(
                f"{stamp} check={index + 1}/{checks} http={response.status} "
                f"status={payload.get('status')} release={payload.get('release')}"
            )
            if not ok:
                failures += 1
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        failures += 1
        print(f"{stamp} check={index + 1}/{checks} ERROR {exc}")
    if index + 1 < checks:
        time.sleep(interval)

if failures:
    print(f"MONITOR: FAIL ({failures}/{checks} unhealthy observations)")
    raise SystemExit(1)
print(f"MONITOR: PASS ({checks}/{checks} healthy observations)")
