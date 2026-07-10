#!/usr/bin/env python3
"""Submit all sitemap URLs to IndexNow (https://www.indexnow.org/).

IndexNow lets a site push instant "this URL changed" notifications to
participating search engines (Bing, Yandex, and others sharing the same
endpoint) instead of waiting for the next crawl.

Usage:
    python scripts/submit_indexnow.py
    python scripts/submit_indexnow.py --sitemap sitemap-0.xml
    python scripts/submit_indexnow.py --url https://tanqo.co/pricing/ --url https://tanqo.co/

Requires the IndexNow key file to already be published at the site root,
e.g. https://tanqo.co/<key>.txt containing just the key string, before
search engines will trust submissions for this host.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "tanqo.co"
KEY = "bdfb516d0f1a36e81ef03ea07075439a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def read_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    text = sitemap_path.read_text(encoding="utf-8")
    return re.findall(rf"<loc>(https://{re.escape(HOST)}/[^<]*)</loc>", text)


def submit(url_list: list[str], host: str = HOST, key: str = KEY, key_location: str = KEY_LOCATION) -> tuple[int, str]:
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow.")
    parser.add_argument(
        "--sitemap",
        default="sitemap.xml",
        help="Sitemap file (relative to repo root) to read URLs from. Default: sitemap.xml",
    )
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        help="Submit specific URL(s) instead of reading from a sitemap. Can be repeated.",
    )
    args = parser.parse_args()

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

    print(f"Submitting {len(url_list)} URL(s) to {ENDPOINT}")
    print(f"host={HOST} key={KEY} keyLocation={KEY_LOCATION}")

    status, body = submit(url_list)

    print(f"HTTP {status}")
    print(body if body else "(empty response body)")

    if status == 200:
        print("IndexNow submission succeeded.")
        return 0
    if status == 202:
        print("IndexNow submission accepted (key not yet verified).")
        return 0

    print("IndexNow submission failed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
