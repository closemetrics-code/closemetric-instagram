# CloseMetric Instagram Content Pipeline

End-to-end flow: research → copy → image generation → scheduling → review → publish.

## Pieces

| Step | Tool | File |
|---|---|---|
| Research | vidIQ (via Claude/Make) | — |
| Copywriting | Gemini / Azure OpenAI (via Make) | — |
| AI hook images | Gemini 2.5 Flash Image | `generate_ai_image.py` |
| Branded carousel slides | Playwright + HTML | `render_carousel.py`, `templates/slide.html` |
| Image hosting | GitHub Pages / Azure Blob | — |
| Scheduling + approval | Metricool | Make module / MCP tool |
| Publishing | Metricool → Instagram | automatic after approval |

## One-time setup

```bash
pip install google-genai playwright --break-system-packages
playwright install chromium
export GEMINI_API_KEY="your-key"   # https://aistudio.google.com/apikey, free, no card
```

## Test the carousel renderer locally

```bash
python render_carousel.py example_slides.json output/test_post
```

This produces `output/test_post_01.png` ... `_04.png`. Open them to check the
look before wiring this into Make.

## Test AI image generation

```bash
python generate_ai_image.py "minimal abstract gradient, deep navy to cyan, fintech brand feel" output/hook_01.png
```

## Hosting the images so Metricool can fetch them

Metricool needs a **public URL** per image, not a local file. Cheapest free option:
push rendered PNGs to a public GitHub repo with GitHub Pages enabled (free on your
student Pro account), e.g.:

```bash
cp output/test_post_*.png docs/
git add docs/ && git commit -m "add carousel" && git push
# now public at https://<you>.github.io/<repo>/test_post_01.png
```

Or upload to Azure Blob Storage (public container) using your $100 student credit.

## Wiring into Make

Make scenario, weekly trigger:

1. **HTTP/LLM module** — generate 3-5 content angles + caption + per-slide text
   (output as JSON matching `example_slides.json`'s shape).
2. **HTTP module** — call a small render endpoint (you can wrap `render_carousel.py`
   in a tiny Flask/FastAPI app on an Azure VM) that returns the hosted image URLs.
   Alternative: run this script as a scheduled GitHub Action instead of a live
   endpoint — simpler, no server to maintain.
3. **Metricool module** (`createScheduledPostForReview`):
   - `blogId`: your CloseMetric brand id
   - `date`: next optimal slot (or pull from `getBestTimeToPostByNetwork`)
   - `info.media`: the hosted PNG URLs, in order
   - `info.providers`: `[{"network":"instagram"}]`
   - `info.instagramData.type`: `"POST"` (carousel is inferred from multiple media)
   - `reviewers`: your email
4. You get an email, review/edit in Metricool, it auto-publishes once approved.

## Recommended first step

Don't wire the full Make scenario on day one. Run `render_carousel.py` by hand for
your first 9 posts, host them manually, and schedule them yourself in Metricool.
Once the format and voice are dialed in, automate steps 1-3 in Make.
