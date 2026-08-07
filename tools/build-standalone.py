#!/usr/bin/env python3
"""
Bundles the site into ONE self-contained HTML file.

CSS, JavaScript and every image are inlined (images as data: URIs), so the
result runs with no network access at all — useful for emailing a preview,
opening from a USB stick, or hosting somewhere with a strict content policy.

The webfont <link> is dropped rather than left pointing at a CDN that a strict
host would block: a blocked font link fails silently and the page renders in a
fallback face with no warning. The stack in site.css falls back to Iowan Old
Style / Georgia deliberately.

Usage:  python3 tools/build-standalone.py [output.html]
Requires: Pillow  (pip install Pillow)
"""

import base64
import io
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "lomanikaya-standalone.html")

# Embedded copies are re-encoded smaller than the originals — the bundle is for
# preview and mail, not for print.
WIDTHS = {
    "hero-sunrise.jpg": 1800,
    "hero-sunrise-portrait.jpg": 900,
    "og-card.jpg": 1200,
}
DEFAULT_WIDTH = 1250
QUALITY = 76


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def data_uri(rel_path):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        raise SystemExit("missing asset: " + rel_path)

    if path.endswith(".svg"):
        raw = open(path, "rb").read()
        return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()

    img = Image.open(path).convert("RGB")
    target = WIDTHS.get(os.path.basename(path), DEFAULT_WIDTH)
    if img.width > target:
        img = img.resize((target, round(img.height * target / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    html = read("index.html")
    css = read("assets", "css", "site.css")
    js = read("assets", "js", "site.js")

    cache = {}

    def embed(rel):
        rel = rel.strip()
        if rel.startswith("data:"):
            return rel
        if rel not in cache:
            cache[rel] = data_uri(rel)
            print("  embedded", rel)
        return cache[rel]

    # CSS first: it carries url() references of its own.
    css = re.sub(r'url\(["\']?(assets/[^"\')]+)["\']?\)',
                 lambda m: 'url("%s")' % embed(m.group(1)), css)

    # <img src> and <source srcset> — relative asset paths only.
    html = re.sub(r'(<(?:img|source)\b[^>]*?\b(?:src|srcset)=")(assets/[^"]+)(")',
                  lambda m: m.group(1) + embed(m.group(2)) + m.group(3), html)

    # Strip everything that would reach for the network, plus the head/body
    # scaffolding the host supplies.
    drops = [
        r'<link rel="preconnect"[^>]*>\s*',
        r'<link href="https://fonts\.googleapis\.com[^>]*>\s*',
        r'<link rel="preload"[^>]*>\s*',
        r'<link rel="stylesheet" href="assets/css/site\.css">\s*',
        r'<script src="assets/js/site\.js" defer></script>\s*',
        r'<!DOCTYPE html>\s*', r'</?html[^>]*>\s*', r'</?head>\s*', r'</?body>\s*',
        r'<meta[^>]*>\s*', r'<link rel="(?:icon|apple-touch-icon|canonical)"[^>]*>\s*',
    ]
    for pattern in drops:
        html = re.sub(pattern, "", html, flags=re.I)

    title_match = re.search(r"<title>.*?</title>", html, re.S)
    title = title_match.group(0) if title_match else "<title>Lomanikaya</title>"
    html = html.replace(title, "")

    bundle = "\n".join([
        title,
        "<style>", css.strip(), "</style>",
        html.strip(),
        "<script>", js.strip(), "</script>",
        "",
    ])

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(bundle)

    print("\nwrote %s  (%.1f MB)" % (OUT, len(bundle.encode()) / 1048576))


if __name__ == "__main__":
    main()
