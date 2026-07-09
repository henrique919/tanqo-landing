#!/usr/bin/env python3
"""Regenerate sitemap-0.xml and sitemap-index.xml from sitemap.xml."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"
SITEMAP_0 = ROOT / "sitemap-0.xml"
SITEMAP_INDEX = ROOT / "sitemap-index.xml"
SITE = "https://tanqo.co"


def read_urls() -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    return re.findall(r"<loc>(https://tanqo\.co/[^<]*)</loc>", text)


def write_sitemap_0(urls: list[str]) -> None:
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    urlset = ET.Element(f"{{{ns}}}urlset")
    for loc in urls:
        url_el = ET.SubElement(urlset, f"{{{ns}}}url")
        loc_el = ET.SubElement(url_el, f"{{{ns}}}loc")
        loc_el.text = loc
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="")
    body = ET.tostring(urlset, encoding="unicode", xml_declaration=False)
    SITEMAP_0.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
        'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">'
        + body.replace(f'<{{{ns}}}urlset>', "").replace(f"</{{{ns}}}urlset>", "")
        + "</urlset>",
        encoding="utf-8",
    )


def write_sitemap_index() -> None:
    SITEMAP_INDEX.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<sitemap><loc>{SITE}/sitemap-0.xml</loc></sitemap>"
        f"<sitemap><loc>{SITE}/sitemap.xml</loc></sitemap>"
        "</sitemapindex>",
        encoding="utf-8",
    )


def main() -> None:
    urls = read_urls()
    if not urls:
        raise SystemExit("No URLs found in sitemap.xml")
    write_sitemap_0(urls)
    write_sitemap_index()
    print(f"Synced {len(urls)} URLs to sitemap-0.xml and sitemap-index.xml")


if __name__ == "__main__":
    main()
