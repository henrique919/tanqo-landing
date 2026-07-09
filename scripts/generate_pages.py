#!/usr/bin/env python3
"""Generate static SEO pages for every sitemap URL (except root and sep.html)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "sitemap.xml"

CSS = """
    :root {
      --navy: #061B2D;
      --blue: #145CFF;
      --cyan: #16C5F7;
      --slate: #67768A;
      --ink: #0B1624;
      --soft: #F7F7F5;
      --line: rgba(103,118,138,.22);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--soft);
      line-height: 1.6;
    }
    a { color: inherit; text-decoration: none; }
    .container { width: min(860px, calc(100% - 44px)); margin: 0 auto; }
    .nav-wrap {
      background: rgba(247,247,245,.92);
      border-bottom: 1px solid rgba(6,27,45,.08);
    }
    nav {
      height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }
    .brand { font-weight: 900; color: var(--navy); letter-spacing: -.02em; }
    .nav-links { display: flex; flex-wrap: wrap; gap: 14px 18px; font-size: 14px; font-weight: 700; color: var(--slate); }
    .nav-links a:hover, .nav-back:hover { color: var(--blue); }
    .nav-back { font-size: 14px; font-weight: 700; color: var(--blue); text-decoration: underline; text-underline-offset: 3px; }
    main { padding: 64px 0 48px; }
    .eyebrow {
      margin: 0 0 12px;
      color: var(--blue);
      font-size: 13px;
      font-weight: 900;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    h1 {
      font-size: clamp(34px, 4vw, 48px);
      line-height: 1.05;
      letter-spacing: -.045em;
      margin: 0 0 20px;
    }
    h2 {
      font-size: clamp(26px, 3vw, 34px);
      line-height: 1.1;
      letter-spacing: -.03em;
      margin: 48px 0 12px;
    }
    p { margin: 0 0 18px; color: #415268; font-size: 18px; }
    .muted { color: var(--slate); font-size: 16px; }
    .btn-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 48px;
      padding: 0 20px;
      border-radius: 14px;
      font-weight: 800;
      border: 1px solid transparent;
    }
    .btn-primary {
      color: white;
      background: linear-gradient(135deg, var(--blue), #1178ff 55%, var(--cyan));
      box-shadow: 0 16px 36px rgba(20,92,255,.28);
    }
    .btn-secondary {
      color: var(--navy);
      background: white;
      border-color: rgba(6,27,45,.12);
    }
    .card-grid {
      display: grid;
      gap: 14px;
      list-style: none;
      padding: 0;
      margin: 24px 0 0;
    }
    .card-grid li {
      padding: 18px 20px;
      border-radius: 16px;
      background: white;
      border: 1px solid var(--line);
      box-shadow: 0 10px 28px rgba(6,27,45,.05);
    }
    .card-grid a {
      color: var(--blue);
      font-weight: 800;
      text-decoration: underline;
      text-underline-offset: 3px;
    }
    .card-grid a:hover { color: #0E4FD4; }
    .card-grid .desc { display: block; margin-top: 6px; color: var(--slate); font-size: 15px; font-weight: 500; }
    ul.bullets { margin: 0 0 18px; padding-left: 1.2rem; color: #415268; font-size: 18px; }
    ul.bullets li { margin-bottom: 10px; }
    footer {
      padding: 30px 0;
      color: #536477;
      font-weight: 700;
    }
    .footer-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
      border-top: 1px solid var(--line);
      padding-top: 24px;
    }
    .footer-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px 18px;
      font-size: 13px;
    }
    .footer-links a {
      color: #536477;
      text-decoration: underline;
      text-underline-offset: 2px;
    }
    .footer-links a:hover { color: var(--blue); }
    @media (max-width: 720px) {
      .footer-inner { flex-direction: column; align-items: flex-start; }
      .nav-links { display: none; }
    }
"""

PAGES: dict[str, dict] = {
    "compare": {
        "title": "Compare Tanqo",
        "description": "Compare Tanqo with other construction quality and defect management tools.",
        "eyebrow": "Compare",
        "h1": "See how Tanqo compares",
        "paragraphs": [
            "Choosing the right waterproofing and closeout workflow matters for builders, site managers, and QA teams.",
            "These pages outline how Tanqo compares on photo evidence, subcontractor response, punch lists, and handover reporting.",
        ],
        "children": [
            ("Tanqo vs Aconex", "tanqo-vs-aconex", "Enterprise document control vs field-first defect closeout."),
            ("Tanqo vs Dashpivot", "tanqo-vs-dashpivot", "Forms and workflows vs photo-backed defect registers."),
            ("Tanqo vs DefectWise", "tanqo-vs-defectwise", "Defect tracking compared for site teams."),
            ("Tanqo vs Fieldwire", "tanqo-vs-fieldwire", "Task coordination vs waterproofing QA closeout."),
            ("Tanqo vs Procore", "tanqo-vs-procore", "Broad construction platform vs focused closeout workflow."),
            ("Tanqo vs Visibuild", "tanqo-vs-visibuild", "Quality management compared for Australian builders."),
        ],
    },
    "compare/tanqo-vs-aconex": {
        "title": "Tanqo vs Aconex",
        "description": "Compare Tanqo and Aconex for construction defect management and closeout workflows.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs Aconex",
        "paragraphs": [
            "Aconex excels at document control and correspondence across large projects. Tanqo focuses on waterproofing job management, photo proof, variations, and builder-ready closeout packs.",
            "Teams often use Tanqo where crews need a simple mobile workflow for QA, defects, and handover — without heavy enterprise setup.",
        ],
        "bullets": [
            "Tanqo: photo-first defect capture and subcontractor response from any phone",
            "Tanqo: waterproofing-specific QA templates and variation tracking",
            "Aconex: broad project correspondence and document registers",
        ],
    },
    "compare/tanqo-vs-dashpivot": {
        "title": "Tanqo vs Dashpivot",
        "description": "Compare Tanqo and Dashpivot for site quality, forms, and defect closeout.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs Dashpivot",
        "paragraphs": [
            "Dashpivot is strong for custom forms and workflow automation. Tanqo is built around the defect register — capture, assign, rectify, and close with linked photos.",
            "If your priority is a live punch list with proof at every step, Tanqo keeps the whole team on one register.",
        ],
    },
    "compare/tanqo-vs-defectwise": {
        "title": "Tanqo vs DefectWise",
        "description": "Compare Tanqo and DefectWise for construction defect tracking.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs DefectWise",
        "paragraphs": [
            "Both tools help teams track defects with accountability. Tanqo emphasises waterproofing workflows, crew scheduling context, and handover reporting for builders.",
        ],
    },
    "compare/tanqo-vs-fieldwire": {
        "title": "Tanqo vs Fieldwire",
        "description": "Compare Tanqo and Fieldwire for site coordination and defect closeout.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs Fieldwire",
        "paragraphs": [
            "Fieldwire covers tasks, drawings, and coordination. Tanqo narrows in on quality closeout — punch lists, photo evidence, subcontractor rectification, and QA sign-off.",
        ],
    },
    "compare/tanqo-vs-procore": {
        "title": "Tanqo vs Procore",
        "description": "Compare Tanqo and Procore for construction quality and closeout.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs Procore",
        "paragraphs": [
            "Procore spans financials, RFIs, and broad project management. Tanqo gives waterproofing and QA teams a focused app for defects, variations, and handover packs without platform overhead.",
        ],
    },
    "compare/tanqo-vs-visibuild": {
        "title": "Tanqo vs Visibuild",
        "description": "Compare Tanqo and Visibuild for construction quality management.",
        "eyebrow": "Compare",
        "h1": "Tanqo vs Visibuild",
        "paragraphs": [
            "Visibuild targets quality programs across construction. Tanqo is purpose-built for waterproofing contractors and builders who need fast photo proof, trade response, and closeout documentation.",
        ],
    },
    "contact": {
        "title": "Contact Tanqo",
        "description": "Contact the Tanqo team about waterproofing job management, demos, and support.",
        "eyebrow": "Contact",
        "h1": "Talk to the Tanqo team",
        "paragraphs": [
            "Questions about rollout, pricing, or how Tanqo fits your waterproofing workflow? We'd love to hear from you.",
            "Email hello@tanqo.co or book a demo walkthrough to see capture, trade response, and handover reporting on realistic project data.",
        ],
    },
    "demo": {
        "title": "Book a Tanqo Demo",
        "description": "Book a short Tanqo walkthrough — defect capture, trade response, and handover packs.",
        "eyebrow": "Demo",
        "h1": "See Tanqo on a real project workflow",
        "paragraphs": [
            "Book a 20-minute walkthrough. We'll show defect capture, subcontractor response, QA review, and the handover pack using realistic construction data.",
            "No credit card. No hard sell. Just a practical look at how Tanqo keeps waterproofing closeout moving.",
        ],
    },
    "features": {
        "title": "Tanqo Features",
        "description": "Tanqo features for defect management, punch lists, photo evidence, QA, and handover.",
        "eyebrow": "Features",
        "h1": "The waterproofing closeout workflow, end to end",
        "paragraphs": [
            "From the defect walk to the handover pack — each part of Tanqo is built around capturing, assigning, and closing defects with proof.",
        ],
        "children": [
            ("Defect Management", "defect-management", "Capture, assign and close every defect with photo evidence."),
            ("Punch List Software", "punch-list-software", "Run your final defect list as a live, photo-backed register."),
            ("Photo Evidence", "photo-evidence", "Original, rectification and closeout photos on every item."),
            ("Subcontractor Closeout", "subcontractor-closeout", "Trades respond and upload rectification photos from any phone."),
            ("Handover Reports", "handover-reports", "Produce a clean handover pack with the photo on each item."),
            ("QA Inspections", "qa-inspections", "Inspections that feed the same register with a consistent standard."),
        ],
    },
    "features/defect-management": {
        "title": "Defect Management — Tanqo",
        "description": "Capture, assign and close construction defects with photo evidence in one register.",
        "eyebrow": "Features",
        "h1": "Defect management with proof at every step",
        "paragraphs": [
            "Log defects on site with photos, location, and trade assignment. Track status from open to rectified to closed — all in one register your builder can trust.",
        ],
    },
    "features/handover-reports": {
        "title": "Handover Reports — Tanqo",
        "description": "Produce builder-ready handover packs with photo evidence on every defect item.",
        "eyebrow": "Features",
        "h1": "Handover reports your builder can sign off",
        "paragraphs": [
            "Export a structured handover pack that shows the original issue, rectification photo, and closeout status — ready for practical completion.",
        ],
    },
    "features/photo-evidence": {
        "title": "Photo Evidence — Tanqo",
        "description": "Link original, rectification and closeout photos to every defect item.",
        "eyebrow": "Features",
        "h1": "Photo evidence on every item",
        "paragraphs": [
            "Tanqo keeps the visual story intact: what was wrong, what was fixed, and who signed it off. No more chasing photos across group chats and email threads.",
        ],
    },
    "features/punch-list-software": {
        "title": "Punch List Software — Tanqo",
        "description": "Run a live punch list as a photo-backed defect register.",
        "eyebrow": "Features",
        "h1": "Punch lists that stay live until closeout",
        "paragraphs": [
            "Turn your final walk into a working register. Assign trades, capture rectifications, and close items with proof — not a spreadsheet that goes stale on day two.",
        ],
    },
    "features/qa-inspections": {
        "title": "QA Inspections — Tanqo",
        "description": "Run QA inspections that feed the same defect register.",
        "eyebrow": "Features",
        "h1": "QA inspections tied to closeout",
        "paragraphs": [
            "Standardise waterproofing QA checks and push failures straight into the defect workflow. One register for inspections, punch items, and handover.",
        ],
    },
    "features/subcontractor-closeout": {
        "title": "Subcontractor Closeout — Tanqo",
        "description": "Let trades respond and upload rectification photos without installing an app.",
        "eyebrow": "Features",
        "h1": "Subcontractor closeout without friction",
        "paragraphs": [
            "Send trades a simple link to view their items and upload rectification photos from any phone. You review, approve, and close — with a full audit trail.",
        ],
    },
    "pricing": {
        "title": "Tanqo Pricing",
        "description": "Simple Tanqo pricing for waterproofing teams and builders.",
        "eyebrow": "Pricing",
        "h1": "Pricing that scales with your jobs",
        "paragraphs": [
            "Tanqo pricing is designed for waterproofing contractors and builder QA teams — per project or rolling site licenses depending on your rollout.",
            "Contact us for current plans, trial access, and multi-site pricing. We'll match the model to how your crews actually work on site.",
        ],
    },
    "privacy": {
        "title": "Privacy Policy — Tanqo",
        "description": "How Tanqo collects, uses, and protects your data.",
        "eyebrow": "Legal",
        "h1": "Privacy policy",
        "paragraphs": [
            "Tanqo respects your privacy. Project photos, defect data, and account information are stored securely and used only to provide the service.",
            "We do not sell personal data. For data access, retention, or deletion requests, contact hello@tanqo.co.",
        ],
    },
    "resources": {
        "title": "Tanqo Resources",
        "description": "Guides, templates, and tools for construction defect management.",
        "eyebrow": "Resources",
        "h1": "Resources for better closeout",
        "paragraphs": [
            "Practical guides and templates to help your team run cleaner defect walks, faster trade response, and smoother handover.",
        ],
        "children": [
            ("Construction defect management guide", "construction-defect-management-guide", "A practical guide to running defect programs."),
            ("Defect closeout checklist", "defect-closeout-checklist", "Checklist for practical completion readiness."),
            ("Defect management ROI calculator", "defect-management-roi-calculator", "Estimate time saved with photo-first workflows."),
            ("Photo evidence in construction", "photo-evidence-in-construction", "Why visual proof matters at every stage."),
            ("Punch list template", "punch-list-template", "Starter template for final walk defect lists."),
        ],
    },
    "resources/construction-defect-management-guide": {
        "title": "Construction Defect Management Guide — Tanqo",
        "description": "A practical guide to construction defect management and closeout.",
        "eyebrow": "Resources",
        "h1": "Construction defect management guide",
        "paragraphs": [
            "Strong defect management starts with a single register, clear ownership, and photo proof at capture and closeout.",
            "This guide covers walk planning, trade assignment, rectification review, and handover documentation for Australian construction teams.",
        ],
    },
    "resources/defect-closeout-checklist": {
        "title": "Defect Closeout Checklist — Tanqo",
        "description": "A defect closeout checklist for practical completion.",
        "eyebrow": "Resources",
        "h1": "Defect closeout checklist",
        "paragraphs": [
            "Use this checklist before handover: register complete, photos on every item, trades signed off, and builder pack exported.",
        ],
        "bullets": [
            "Final walk completed with named owners per item",
            "Rectification photos uploaded and reviewed",
            "Open items escalated with dates",
            "Handover report generated and shared",
        ],
    },
    "resources/defect-management-roi-calculator": {
        "title": "Defect Management ROI Calculator — Tanqo",
        "description": "Estimate ROI from faster defect closeout and photo-first workflows.",
        "eyebrow": "Resources",
        "h1": "Defect management ROI calculator",
        "paragraphs": [
            "Teams using photo-first defect registers typically spend less time chasing updates and rework evidence.",
            "Contact Tanqo for a tailored ROI review based on your project volume, trade count, and closeout cycle time.",
        ],
    },
    "resources/photo-evidence-in-construction": {
        "title": "Photo Evidence in Construction — Tanqo",
        "description": "Why photo evidence matters for construction QA and closeout.",
        "eyebrow": "Resources",
        "h1": "Photo evidence in construction",
        "paragraphs": [
            "Photos reduce disputes, speed up trade response, and give builders confidence at practical completion.",
            "Tanqo links original, rectification, and closeout images to each register item so the story stays in one place.",
        ],
    },
    "resources/punch-list-template": {
        "title": "Punch List Template — Tanqo",
        "description": "A starter punch list template for construction closeout.",
        "eyebrow": "Resources",
        "h1": "Punch list template",
        "paragraphs": [
            "Start with location, description, trade, due date, and photo columns — then move to a live register in Tanqo so nothing gets lost after the walk.",
        ],
    },
    "security": {
        "title": "Security — Tanqo",
        "description": "How Tanqo protects project data, photos, and account access.",
        "eyebrow": "Security",
        "h1": "Security you can stand behind",
        "paragraphs": [
            "Tanqo uses encrypted transport, access controls, and secure cloud storage for project photos and defect data.",
            "For security questionnaires or enterprise reviews, contact hello@tanqo.co.",
        ],
    },
    "solutions": {
        "title": "Tanqo Solutions",
        "description": "Tanqo solutions for builders, site managers, QA teams, and subcontractors.",
        "eyebrow": "Solutions",
        "h1": "Built for every role on the closeout",
        "paragraphs": [
            "Whether you run the site, manage quality, or respond as a trade — Tanqo keeps everyone aligned on the same defect register.",
        ],
        "children": [
            ("Builders", "builders", "Practical completion with fewer surprises."),
            ("Project Managers", "project-managers", "Visibility across trades and milestones."),
            ("Quality Managers", "quality-managers", "Consistent QA and audit-ready records."),
            ("Site Managers", "site-managers", "Capture and assign from the field."),
            ("Subcontractors", "subcontractors", "Simple response without app installs."),
        ],
    },
    "solutions/builders": {
        "title": "Tanqo for Builders",
        "description": "Defect and handover workflow for builders and developers.",
        "eyebrow": "Solutions",
        "h1": "Tanqo for builders",
        "paragraphs": [
            "Get photo-backed defect registers and handover packs that stand up at practical completion — without chasing spreadsheets and message threads.",
        ],
    },
    "solutions/project-managers": {
        "title": "Tanqo for Project Managers",
        "description": "Project visibility for defect closeout and trade coordination.",
        "eyebrow": "Solutions",
        "h1": "Tanqo for project managers",
        "paragraphs": [
            "See open items, overdue trades, and closeout progress across zones — one register instead of fragmented updates.",
        ],
    },
    "solutions/quality-managers": {
        "title": "Tanqo for Quality Managers",
        "description": "QA programs tied to defect closeout and handover.",
        "eyebrow": "Solutions",
        "h1": "Tanqo for quality managers",
        "paragraphs": [
            "Run inspections that feed the same register as punch items. Keep standards consistent and evidence audit-ready.",
        ],
    },
    "solutions/site-managers": {
        "title": "Tanqo for Site Managers",
        "description": "Mobile defect capture and trade assignment from site.",
        "eyebrow": "Solutions",
        "h1": "Tanqo for site managers",
        "paragraphs": [
            "Capture defects with photos on walk-through, assign trades instantly, and track rectifications without leaving the register.",
        ],
    },
    "solutions/subcontractors": {
        "title": "Tanqo for Subcontractors",
        "description": "Simple defect response and photo upload for trades.",
        "eyebrow": "Solutions",
        "h1": "Tanqo for subcontractors",
        "paragraphs": [
            "View your assigned items, upload rectification photos from any phone, and get closed out faster — no app install required.",
        ],
    },
}


def parse_sitemap() -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    urls = re.findall(r"<loc>https://tanqo\.co/([^<]*)</loc>", text)
    slugs: list[str] = []
    for u in urls:
        slug = u.strip("/")
        if slug and slug != "sep.html":
            slugs.append(slug)
    return slugs


def rel_to_root(slug: str) -> str:
    depth = slug.count("/") + 1
    return "../" * depth


def render_page(slug: str, meta: dict) -> str:
    prefix = rel_to_root(slug)
    home = f"{prefix}index.html"
    canonical = f"https://tanqo.co/{slug}/"
    title = meta["title"]
    description = meta["description"]

    body_parts = [
        f'      <p class="eyebrow">{meta["eyebrow"]}</p>',
        f"      <h1>{meta['h1']}</h1>",
    ]
    for para in meta.get("paragraphs", []):
        body_parts.append(f"      <p>{para}</p>")

    if bullets := meta.get("bullets"):
        body_parts.append("      <ul class=\"bullets\">")
        for item in bullets:
            body_parts.append(f"        <li>{item}</li>")
        body_parts.append("      </ul>")

    if children := meta.get("children"):
        body_parts.append("      <h2>Explore</h2>")
        body_parts.append("      <ul class=\"card-grid\">")
        for label, child_slug, desc in children:
            href = f"{child_slug}/"
            body_parts.append(
                f'        <li><a href="{href}">{label}</a><span class="desc">{desc}</span></li>'
            )
        body_parts.append("      </ul>")

    body_parts.extend(
        [
            '      <div class="btn-row">',
            f'        <a class="btn btn-primary" href="{prefix}demo/">Book a demo</a>',
            f'        <a class="btn btn-secondary" href="{home}">Back to home</a>',
            "      </div>",
        ]
    )

    nav_links = f"""
        <div class="nav-links">
          <a href="{prefix}features/">Features</a>
          <a href="{prefix}solutions/">Solutions</a>
          <a href="{prefix}pricing/">Pricing</a>
          <a href="{prefix}resources/">Resources</a>
          <a href="{prefix}contact/">Contact</a>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canonical}" />
  <style>{CSS}
  </style>
</head>
<body>
  <div class="nav-wrap">
    <div class="container">
      <nav>
        <a class="brand" href="{home}" aria-label="Tanqo home">Tanqo</a>
        {nav_links}
        <a class="nav-back" href="{home}">&larr; Home</a>
      </nav>
    </div>
  </div>

  <main>
    <div class="container">
{chr(10).join(body_parts)}
    </div>
  </main>

  <footer>
    <div class="container footer-inner">
      <a class="brand" href="{home}">Tanqo</a>
      <nav class="footer-links" aria-label="Site links">
        <a href="{prefix}privacy/">Privacy</a>
        <a href="{prefix}security/">Security</a>
        <a href="{prefix}sep.html">SEP</a>
      </nav>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    slugs = parse_sitemap()
    missing = [s for s in slugs if s not in PAGES]
    if missing:
        raise SystemExit(f"Missing page metadata for: {', '.join(missing)}")

    for slug in slugs:
        out_dir = ROOT / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        out_file.write_text(render_page(slug, PAGES[slug]), encoding="utf-8")
        print(f"Wrote {out_file.relative_to(ROOT)}")

    print(f"Generated {len(slugs)} pages.")


if __name__ == "__main__":
    main()
