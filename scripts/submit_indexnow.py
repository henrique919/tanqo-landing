#!/usr/bin/env python3
"""Submit all sitemap URLs to IndexNow (https://www.indexnow.org/)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "tanqo.co"
KEY = "bdfb516d0f1a36e81ef03ea07075439a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
# Bing (api.indexnow.org) may return 403 until the site is verified in Bing Webmaster
# Tools; Yandex accepts the same payload and shares with the IndexNow network.
ENDPOINTS = (
    "https://yandex.com/indexnow",
    "https://api.indexnow.org/indexnow",
)


def read_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    text = sitemap_path.read_text(encoding="utf-8")
    return re.findall(rf"<loc>(https://{re.escape(HOST)}/[^<]*)</loc>", text)


def fetch_key_file(key_location: str = KEY_LOCATION, key: str = KEY) -> tuple[int, str]:
    req = urllib.request.Request(key_location, method="GET", headers={"User-Agent": "tanqo-indexnow/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def wait_for_key_live(
    key_location: str = KEY_LOCATION,
    key: str = KEY,
    *,
    timeout_sec: int = 600,
    interval_sec: int = 15,
) -> bool:
    deadline = time.monotonic() + timeout_sec
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        status, body = fetch_key_file(key_location, key)
        if status == 200 and body.strip() == key:
            print(f"IndexNow key file is live at {key_location} (attempt {attempt}).")
            return True
        print(
            f"Waiting for key file (attempt {attempt}): HTTP {status}, "
            f"body={body.strip()!r} (want {key!r})",
            file=sys.stderr,
        )
        time.sleep(interval_sec)
    return False


def submit(
    url_list: list[str],
    endpoint: str,
    host: str = HOST,
    key: str = KEY,
    key_location: str = KEY_LOCATION,
) -> tuple[int, str]:
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def submission_ok(status: int) -> bool:
    return status in (200, 202)


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow.")
    parser.add_argument(
        "--sitemap",
        default="sitemap.xml",
        help="Sitemap file (relative to repo root). Default: sitemap.xml",
    )
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="Submit specific URL(s) instead of reading from a sitemap.",
    )
    parser.add_argument(
        "--wait-for-live",
        action="store_true",
        help="Poll keyLocation until the key file returns HTTP 200 with the expected key.",
    )
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=600,
        help="Max seconds to wait when --wait-for-live is set (default: 600).",
    )
    args = parser.parse_args()

    if args.wait_for_live:
        if not wait_for_key_live(timeout_sec=args.wait_timeout):
            print("Timed out waiting for IndexNow key file to go live.", file=sys.stderr)
            return 1

    if args.urls:
        url_list = args.urls
    else:
        sitemap_path = ROOT / args.sitemap
        if not sitemap_path.exists():
            print(f"Sitemap not found: {sitemap_path}", file=sys.stderr)
            return 1
        url_list = read_urls_from_sitemap(sitemap_path)

    if not url_list:
        print("No URLs to submit.", file=sys.stderr)
        return 1

    print(f"Submitting {len(url_list)} URL(s)")
    print(f"host={HOST} key={KEY} keyLocation={KEY_LOCATION}")

    any_ok = False
    for endpoint in ENDPOINTS:
        print(f"\nPOST {endpoint}")
        status, body = submit(url_list, endpoint)
        print(f"HTTP {status}")
        print(body if body else "(empty response body)")
        if submission_ok(status):
            any_ok = True
            print("Accepted by this endpoint.")
        elif status == 403 and "UserForbiddedToAccessSite" in body:
            print(
                "Bing has not authorized this host yet (verify in Bing Webmaster Tools if needed).",
                file=sys.stderr,
            )

    if any_ok:
        print("\nIndexNow submission succeeded (at least one endpoint accepted).")
        return 0

    print("\nIndexNow submission failed on all endpoints.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
