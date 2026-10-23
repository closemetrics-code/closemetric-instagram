"""
Generate an AI image using Gemini 2.5 Flash Image ("Nano Banana").
Used for hook/background images — not for text-heavy carousel slides
(use render_carousel.py for those instead).

Setup:
    pip install google-genai --break-system-packages
    export GEMINI_API_KEY="your-key-here"   # from https://aistudio.google.com/apikey

Usage:
    python generate_ai_image.py "a minimal abstract gradient, deep blue to teal, for a fintech brand" output/hook_01.png
"""

import os
import sys
from google import genai
from google.genai import types


def generate_image(prompt: str, out_path: str, aspect_ratio: str = "1:1") -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Get a free key at https://aistudio.google.com/apikey "
            "and export it as an environment variable — never hardcode it here."
        )

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            with open(out_path, "wb") as f:
                f.write(part.inline_data.data)
            print(f"Saved image to {out_path}")
            return out_path

    raise RuntimeError("No image was returned by the API. Try adjusting the prompt.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_ai_image.py \"<prompt>\" <output_path> [aspect_ratio]")
        sys.exit(1)

    prompt = sys.argv[1]
    out_path = sys.argv[2]
    aspect = sys.argv[3] if len(sys.argv) > 3 else "1:1"

    generate_image(prompt, out_path, aspect)
