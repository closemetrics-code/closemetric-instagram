# Weekly Carousel GitHub Action — Setup

## What it does

Every Monday 09:00 UTC (edit the cron in `.github/workflows/weekly-carousel.yml`
to change this), GitHub Actions automatically:

1. Generates this week's carousel copy with Gemini (`generate_weekly_content.py`),
   rotating through CloseMetric's 4 content pillars.
2. Renders it into branded PNG slides with Playwright (`render_carousel.py`).
3. Commits the PNGs into `docs/posts/` and pushes.
4. Prints the public GitHub Pages URL for each image.

You (or a Make scenario) then take those URLs and schedule the post in Metricool
for review — the workflow does NOT auto-publish to Instagram. That step stays
a deliberate call to `createScheduledPostForReview` so nothing goes live
without your approval.

## One-time setup

1. **Push this folder to a GitHub repo.**
   ```bash
   git init
   git add .
   git commit -m "Initial CloseMetric IG pipeline"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**, serving from the `docs/` folder:
   Repo → Settings → Pages → Source: "Deploy from a branch" → Branch: `main`,
   folder: `/docs`. Your images will be public at:
   `https://<you>.github.io/<repo>/posts/<filename>.png`

3. **Add your Gemini API key as a repo secret:**
   Repo → Settings → Secrets and variables → Actions → New repository secret
   → Name: `GEMINI_API_KEY`, Value: your key from https://aistudio.google.com/apikey

4. **Test it manually** before waiting for Monday:
   Repo → Actions tab → "Weekly CloseMetric Carousel" → Run workflow.

## After it runs

Check the Actions run log for the printed image URLs, then either:
- Paste them into Metricool manually to schedule for review, or
- Extend the workflow (or a Make scenario watching the repo) to call
  Metricool's `createScheduledPostForReview` automatically with those URLs.

## Notes

- `content/slides-<run-id>.json` is also committed, so you have a record of
  what copy was generated each week — delete old ones periodically to keep
  the repo tidy.
- If Gemini returns malformed JSON occasionally, the workflow run will fail
  at the generate step — just check the Actions log and re-run.
- Free tier: GitHub Actions minutes are free on your student Pro plan;
  Gemini API calls are free tier; GitHub Pages hosting is free.
