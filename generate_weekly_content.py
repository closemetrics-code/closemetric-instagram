"""
Generate one week's carousel content (copy only) using the Gemini API,
in the same JSON shape render_carousel.py expects.

Setup:
    pip install google-genai --break-system-packages
    export GEMINI_API_KEY="your-key-here"

Usage:
    python generate_weekly_content.py content/slides.json
"""

import json
import os
import sys
from google import genai

PILLARS = [
    "a specific, tactical outbound/cold-email tip",
    "a proof/results story about affiliate marketing or email marketing for B2B",
    "a contrarian take on agency retainers vs performance-based marketing",
    "a process breakdown of how CloseMetric builds a revenue system",
]

SYSTEM_PROMPT = """You write Instagram carousel copy for CloseMetric, a full-stack sales
and marketing company ("The Selling Machine") that builds affiliate programs, paid ads,
email sequences, and sales funnels for high-ticket B2B businesses (SaaS, consulting,
coaches, agencies). Voice: direct, confident, no fluff, data-driven, slightly contrarian
about traditional agencies. Never use emojis in slide text. Keep sentences short.

Return ONLY valid JSON: an array of 4-5 slide objects, each with "kicker" (short
uppercase label), "headline" (one punchy sentence, under 60 characters), and "body"
(one or two sentences, under 140 characters). The last slide should be a soft
CTA to follow for more. No markdown, no commentary, just the JSON array."""


def generate_week(out_path: str, pillar_index: int | None = None):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)

    import datetime
    idx = pillar_index if pillar_index is not None else (datetime.date.today().isocalendar()[1] % len(PILLARS))
    pillar = PILLARS[idx]

    prompt = f"{SYSTEM_PROMPT}\n\nThis week's angle: {pillar}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
    )

    text = response.text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    slides = json.loads(text)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(slides, f, indent=2)

    print(f"Wrote {len(slides)} slides to {out_path} (pillar: {pillar})")
    return out_path


if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "content/slides.json"
    generate_week(out_path)
