"""
Render a branded Instagram carousel (1080x1350 PNGs, one per slide)
from templates/slide.html using Playwright.

Setup:
    pip install playwright --break-system-packages
    playwright install chromium

Usage:
    python render_carousel.py slides.json output/my_post

Where slides.json looks like:
[
  {"kicker": "OUTBOUND TIP #1", "headline": "Stop pitching in your first email.", "body": "Lead with a specific, relevant observation about their business instead."},
  {"kicker": "OUTBOUND TIP #1", "headline": "Why it works", "body": "Specificity signals you did homework. Generic pitches get deleted in two seconds."},
  {"kicker": "OUTBOUND TIP #1", "headline": "Try this instead", "body": "\"Noticed you just launched in Saudi — curious how you're handling local payment rails.\""}
]

Each dict becomes one slide. Output files are named output/my_post_01.png, _02.png, etc.
Upload the resulting PNG URLs (host them on GitHub Pages, Azure Blob, or similar
public storage) and pass them as `media` to Metricool's createScheduledPost.
"""

import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

TEMPLATE_PATH = Path(__file__).parent / "templates" / "slide.html"


def render_slides(slides_json_path: str, output_prefix: str) -> list[str]:
    with open(slides_json_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    total = len(slides)
    out_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})

        for i, slide in enumerate(slides, start=1):
            html = (
                template
                .replace("{{KICKER}}", slide.get("kicker", ""))
                .replace("{{HEADLINE}}", slide.get("headline", ""))
                .replace("{{BODY}}", slide.get("body", ""))
                .replace("{{PAGE}}", str(i))
                .replace("{{TOTAL}}", str(total))
            )
            page.set_content(html)
            out_path = f"{output_prefix}_{i:02d}.png"
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            page.screenshot(path=out_path)
            out_paths.append(out_path)
            print(f"Rendered {out_path}")

        browser.close()

    return out_paths


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_carousel.py <slides.json> <output_prefix>")
        sys.exit(1)

    render_slides(sys.argv[1], sys.argv[2])
