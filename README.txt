Tanqo landing site (tanqo.co)

Static HTML site deployed via GitHub Pages.

Quick start:
  npm run build              # regenerate SEO pages + sync sitemaps
  npm run preview            # local server on http://localhost:8080
  npm run submit-indexnow    # notify search engines of all sitemap URLs via IndexNow

Pages:
  index.html       # main landing page
  sep.html         # SEP resources page
  */index.html     # 31 SEO pages matching sitemap.xml

Deploy:
  Push to main triggers .github/workflows/deploy-pages.yml
  Custom domain: tanqo.co (CNAME file)
  NOTE: tanqo.co is actually served by a Render web service, not GitHub
  Pages. The Pages workflow still runs, but the live site requires a
  manual "Deploy" trigger in the Render dashboard to pick up new commits
  (including this repo's IndexNow key file).

IndexNow (https://www.indexnow.org/):
  Key file: bdfb516d0f1a36e81ef03ea07075439a.txt (repo root, served at
  https://tanqo.co/bdfb516d0f1a36e81ef03ea07075439a.txt) proves ownership
  of tanqo.co to IndexNow-participating search engines (Bing, Yandex, etc).
  Run `npm run submit-indexnow` (or `python scripts/submit_indexnow.py`)
  after deploying changes to push updated URLs from sitemap.xml instantly
  instead of waiting for normal crawl discovery. Also wired into
  .github/workflows/indexnow.yml, which submits automatically on push to
  main (manual trigger also available via workflow_dispatch).
