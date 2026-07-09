Tanqo landing site (tanqo.co)

Static HTML site deployed via GitHub Pages.

Quick start:
  npm run build    # regenerate SEO pages + sync sitemaps
  npm run preview  # local server on http://localhost:8080

Pages:
  index.html       # main landing page
  sep.html         # SEP resources page
  */index.html     # 31 SEO pages matching sitemap.xml

Deploy:
  Push to main triggers .github/workflows/deploy-pages.yml
  Custom domain: tanqo.co (CNAME file)
