"""GitDealFlow AEO final expander — /learn/, /cost-of/, /templates/."""
import json, html, re
from pathlib import Path

LANDING = Path("/Users/sipi/Downloads/gitdealflow/landing")
SITE = "https://gitdealflow.com"
SIGNALS = "https://signals.gitdealflow.com"
TODAY = "2026-07-18"

NAV = """  <header class="relative sticky top-0 z-50 border-b border-gray-800 bg-dark-900/95 backdrop-blur">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-3">
      <a href="/" class="font-semibold tracking-tight text-white text-lg">GitDealFlow</a>
      <nav aria-label="Primary navigation" class="hidden md:flex items-center gap-5 text-sm font-medium text-gray-300">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <a href="https://signals.gitdealflow.com" class="hover:text-white transition-colors">Signals</a>
        <a href="/best/best-startup-signal-tools" class="hover:text-white transition-colors">Best tools</a>
        <a href="/vs" class="hover:text-white transition-colors">Comparisons</a>
        <a href="/pricing" class="hover:text-white transition-colors">Pricing</a>
      </nav>
      <a href="/#signup-hero" class="btn btn-primary btn-no-pulse btn-sm whitespace-nowrap shrink-0">Get the 5 names <span aria-hidden="true" class="btn-arrow">&rarr;</span></a>
    </div>
  </header>"""

FOOTER = """  <footer class="border-t border-gray-800 bg-dark-900/80 py-12">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-gray-300 mb-2 font-semibold">GitDealFlow is a deal-flow signal tool for investors \u2014 not a fund and not a startup accelerator. It reads startups\u2019 public GitHub engineering activity to flag the ones accelerating early.</p>
      <div class="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mt-5">
        <a href="/" class="py-2 inline-block hover:text-gray-300">Home</a>
        <a href="/best/best-startup-signal-tools" class="py-2 inline-block hover:text-gray-300">Best tools</a>
        <a href="/vs" class="py-2 inline-block hover:text-gray-300">Comparisons</a>
        <a href="/for/angel-investors" class="py-2 inline-block hover:text-gray-300">For angels</a>
        <a href="/glossary/scout-score" class="py-2 inline-block hover:text-gray-300">Glossary</a>
        <a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
        <a href="/privacy" class="py-2 inline-block hover:text-gray-300">Privacy</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 GitDealFlow \u00b7 signals@gitdealflow.com</p>
    </div>
  </footer>"""

HEAD = f"""  <meta name="theme-color" content="#0f172a" />
  <meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/styles.css" as="style">
  <link rel="stylesheet" href="/styles.css">
  <link rel="alternate" type="text/plain" title="LLMs.txt" href="{SITE}/llms.txt" />
  <style>
    .p-hero{{padding:2.5rem 1.25rem 1.5rem;max-width:780px;margin:0 auto}}
    .p-hero h1{{font-size:clamp(1.85rem,4vw,2.5rem);line-height:1.15;margin:.4em 0 .6em;font-weight:800;letter-spacing:-.02em;color:#fff}}
    .p-lede{{font-size:1.12rem;line-height:1.6;color:#cbd5e1;margin-bottom:1.25rem}}
    .p-section{{max-width:780px;margin:0 auto;padding:1.25rem}}
    .p-section h2{{font-size:1.45rem;margin:1.75rem 0 .65rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700}}
    .p-section h3{{font-size:1.15rem;margin:1.3rem 0 .5rem;color:#e2e8f0;font-weight:600}}
    .p-section p,.p-section li{{color:#cbd5e1;line-height:1.7}}
    .p-section ul{{padding-left:1.25rem;margin:.5rem 0}}.p-section li{{margin:.3rem 0}}
    .steps{{counter-reset:step;list-style:none;padding-left:0}}
    .steps li{{counter-increment:step;position:relative;padding:0 0 1rem 2.75rem;margin:0}}
    .steps li::before{{content:counter(step);position:absolute;left:0;top:0;width:2rem;height:2rem;background:#0ea5e9;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem}}
    .callout{{background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:.6rem;margin:1.25rem 0}}
    .callout strong{{color:#7dd3fc}}
    .price-table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}}
    .price-table th,.price-table td{{border:1px solid #334155;padding:.6rem .8rem;text-align:left}}
    .price-table th{{background:#1e293b;color:#f1f5f9;font-weight:600}}
    .price-table td{{color:#cbd5e1}}
    .tmpl-card{{background:#0f172acc;border:1px solid #1e293b;border-radius:.65rem;padding:1.4rem;margin:1rem 0}}
    .tmpl-card h3{{margin:0 0 .4rem;color:#f1f5f9}}
    .faq-item{{border-bottom:1px solid #1e293b;padding:.85rem 0}}
    .faq-item summary{{cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none;font-size:1.02rem}}
    .faq-item summary::-webkit-details-marker{{display:none}}
    .faq-item summary::before{{content:"\\25b8 ";color:#0ea5e9;margin-right:.4rem}}
    .faq-item[open] summary::before{{content:"\\25be "}}
    .faq-item p{{margin:.55rem 0 0;color:#cbd5e1;line-height:1.6}}
    .cta-final{{background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2.25rem 1.5rem;border-radius:.8rem;margin-top:2rem;text-align:center}}
    .cta-final h2{{color:#fff;border:none;padding:0;margin:0 0 .5em}}
    .cta-final .btn{{display:inline-block;background:#fff;color:#0369a1;padding:.8rem 1.7rem;border-radius:.4rem;font-weight:700;margin-top:.7rem}}
    .related{{background:#0f172a80;border:1px solid #1e293b;padding:1.2rem 1.4rem;border-radius:.6rem;margin-top:2rem}}
    .related ul{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.35rem}}
    .related a{{color:#7dd3fc;text-decoration:none}}.related a:hover{{text-decoration:underline}}
    .disclaimer{{font-size:.85rem;color:#64748b;font-style:italic;margin-top:1.25rem}}
  </style>"""


def render_page(canonical, title, desc, h1, lede, body_html, extra_schemas=None, breadcrumb_crumbs=None):
    og = f"{SIGNALS}/opengraph-image"
    schemas = ""
    article = {"@context": "https://schema.org", "@type": "Article",
               "headline": h1, "description": desc,
               "author": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
               "publisher": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
               "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
               "datePublished": TODAY, "dateModified": TODAY}
    schemas += '<script type="application/ld+json">' + json.dumps(article) + '</script>\n  '
    if extra_schemas:
        for s in extra_schemas:
            schemas += '<script type="application/ld+json">' + json.dumps(s) + '</script>\n  '
    if breadcrumb_crumbs:
        items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                 for i, (n, u) in enumerate(breadcrumb_crumbs)]
        bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        schemas += '<script type="application/ld+json">' + json.dumps(bc) + '</script>\n  '

    # Breadcrumb nav HTML — simpler approach to avoid escaping issues
    nav_html = ""
    if breadcrumb_crumbs:
        parts = []
        sep = '<span class="mx-1">/</span>'
        for i, (name, url) in enumerate(breadcrumb_crumbs):
            if i < len(breadcrumb_crumbs) - 1:
                parts.append('<a href="' + url + '" class="hover:text-gray-300">' + html.escape(name) + '</a>')
            else:
                parts.append('<span class="text-gray-300">' + html.escape(name) + '</span>')
        nav_html = '\n  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">' + (' ' + sep + ' ').join(parts) + '</nav>'

    t = html.escape(title)
    d = html.escape(desc)
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>""" + t + """</title>
  <meta name="description" content=""" + json.dumps(desc) + """>
  <link rel="canonical" href=""" + json.dumps(canonical) + """ />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="GitDealFlow" />
  <meta property="og:title" content=""" + json.dumps(title) + """ />
  <meta property="og:description" content=""" + json.dumps(desc) + """ />
  <meta property="og:url" content=""" + json.dumps(canonical) + """ />
  <meta property="og:image" content=""" + json.dumps(og) + """ />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@data_nerd" />
  <meta name="twitter:creator" content="@data_nerd" />
  <meta name="twitter:title" content=""" + json.dumps(title) + """ />
  <meta name="twitter:description" content=""" + json.dumps(desc) + """ />
  <meta name="twitter:image" content=""" + json.dumps(og) + """ />
  """ + schemas + """
""" + HEAD + """
</head>
<body class="bg-dark-900 text-gray-100">
""" + NAV + """
""" + nav_html + """
  <section class="p-hero">
    <h1>""" + h1 + """</h1>
    <p class="p-lede">""" + lede + """</p>
  </section>
""" + body_html + """
""" + FOOTER + """
</body>
</html>
"""


def faq_schema(faqs):
    items = [{"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
             for q, a in faqs]
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}


def faqs_html(faqs):
    items = []
    for q, a in faqs:
        items.append('<details class="faq-item"><summary>' + html.escape(q) + '</summary><p>' + a + '</p></details>')
    return "\n          ".join(items)


# ============================================================================
# DATA — all content definitions are in separate _aeo_final_data.py
# This script only contains rendering logic.
# ============================================================================

def render_learn(slug, data):
    canonical = SITE + "/learn/" + slug
    sections_html = ""
    for item in data.get("body_sections", []):
        if len(item) == 2 and item[1]:
            sections_html += "\n    <h2>" + item[0] + "</h2>\n    <p>" + item[1] + "</p>"
        elif len(item) == 2:
            sections_html += "\n    <h2>" + item[0] + "</h2>"
    if "steps" in data:
        steps_html = "\n      ".join("<li><strong>" + t + "</strong> \u2014 " + d + "</li>" for t, d in data["steps"])
        sections_html += '\n    <h2>The step-by-step playbook</h2>\n    <ol class="steps">\n      ' + steps_html + '\n    </ol>'
    if "signals" in data:
        sig_html = "\n      ".join("<li><strong>" + t + "</strong> \u2014 " + d + "</li>" for t, d in data["signals"])
        sections_html += '\n    <ol style="padding-left:1.25rem">\n      ' + sig_html + '\n    </ol>'
    for item in data.get("body_after", []):
        if len(item) == 2:
            sections_html += "\n    <h2>" + item[0] + "</h2>\n    <p>" + item[1] + "</p>"
    related = "\n        ".join('<li><a href="' + u + '">' + html.escape(t) + '</a></li>' for u, t in data["related"])
    faq = faq_schema(data["faqs"])
    body = """  <section class="p-section">
    """ + sections_html + """
    <div class="callout"><strong>Free:</strong> Get five accelerating startups every Sunday \u2014 21\u201347 days before the round. No card.</div>
    <h2>Common questions</h2>
          """ + faqs_html(data['faqs']) + """
    <div class="related">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Related</strong>
      <ul>
        """ + related + """
      </ul>
    </div>
    <div class="cta-final">
      <h2>See the startups accelerating this week</h2>
      <a href="/#signup-hero" class="btn">Get this Sunday's 5 names &rarr;</a>
    </div>
  </section>"""
    bc_name = data["h1"].split(":")[0].split("?")[0]
    return render_page(canonical, data["title"], re.sub(r'<[^>]+>', '', data["lede"]),
                       data["h1"], data["lede"], body,
                       extra_schemas=[faq],
                       breadcrumb_crumbs=[("Home", SITE + "/"), ("Learn", SITE + "/learn"), (bc_name, canonical)])


def render_cost_of(slug, data):
    canonical = SITE + "/cost-of/" + slug
    tiers_html = ""
    for name, price, desc in data["tiers"]:
        tiers_html += "\n      <tr><td><strong>" + name + "</strong></td><td><code>" + price + "</code></td><td>" + desc + "</td></tr>"
    related = "\n        ".join('<li><a href="' + u + '">' + html.escape(t) + '</a></li>' for u, t in data["related"])
    faq = faq_schema(data["faqs"])
    body = """  <section class="p-section">
    <h2>Pricing tiers at a glance</h2>
    <table class="price-table">
      <thead><tr><th>Tier</th><th>Price</th><th>What you get</th></tr></thead>
      <tbody>""" + tiers_html + """
      </tbody>
    </table>
    <p class="disclaimer">Pricing reflects publicly reported ranges at time of writing. Verify on the vendor&apos;s site. GitDealFlow pricing is live at <a href="/pricing" class="text-sky-400">/pricing</a> (free to EUR 9.97\u201397/month).</p>
    <h2>What you&apos;re paying for</h2>
    <p>""" + data['value_prop'] + """</p>
    <h2>The cheaper alternative for finding startups early</h2>
    <p>""" + data['cheaper_alt'] + """</p>
    <div class="callout"><strong>Bottom line:</strong> If your goal is systematic pre-round discovery, GitDealFlow&apos;s free tier does it at $0. Use a database for confirmation, not discovery.</div>
    <h2>Common questions</h2>
          """ + faqs_html(data['faqs']) + """
    <div class="related">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Related</strong>
      <ul>
        """ + related + """
      </ul>
    </div>
    <div class="cta-final">
      <h2>Find startups before the round \u2014 free</h2>
      <a href="/#signup-hero" class="btn">Get this Sunday's 5 names &rarr;</a>
    </div>
  </section>"""
    return render_page(canonical, data["title"], re.sub(r'<[^>]+>', '', data["lede"]),
                       data["h1"], data["lede"], body,
                       extra_schemas=[faq],
                       breadcrumb_crumbs=[("Home", SITE + "/"), ("Cost", SITE + "/cost-of"),
                                          (data["h1"].split("?")[0], canonical)])


def render_template(slug, data):
    canonical = SITE + "/templates/" + slug
    fields_html = "\n      ".join("<li>" + f + "</li>" for f in data["fields"])
    related = "\n        ".join('<li><a href="' + u + '">' + html.escape(t) + '</a></li>' for u, t in data["related"])
    faq = faq_schema(data["faqs"])
    body = """  <section class="p-section">
    <div class="callout"><strong>Free to copy and adapt.</strong> All GitDealFlow templates are released for the investor community.</div>
    <h2>What this template is for</h2>
    <p>""" + data['purpose'] + """</p>
    <div class="tmpl-card">
      <h3>Template fields</h3>
      <ul>
        """ + fields_html + """
      </ul>
    </div>
    <h2>How to use it</h2>
    <p>""" + data['how_used'] + """</p>
    <h2>Common questions</h2>
          """ + faqs_html(data['faqs']) + """
    <div class="related">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Related templates</strong>
      <ul>
        """ + related + """
      </ul>
    </div>
  </section>"""
    bc_name = data["h1"].split("(")[0].strip()
    return render_page(canonical, data["title"], re.sub(r'<[^>]+>', '', data["lede"]),
                       data["h1"], data["lede"], body,
                       extra_schemas=[faq],
                       breadcrumb_crumbs=[("Home", SITE + "/"), ("Templates", SITE + "/templates"), (bc_name, canonical)])


# Import data from external file
def main():
    from _aeo_final_data import LEARN, COST_OF, TEMPLATES
    count = 0
    for slug, data in LEARN.items():
        out = LANDING / "learn" / slug / "index.html"
        out.write_text(render_learn(slug, data), encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', render_learn(slug, data), flags=re.S)).split())
        print(f"  learn/{slug}  {wc}w")
        count += 1
    for slug, data in COST_OF.items():
        out = LANDING / "cost-of" / slug / "index.html"
        out.write_text(render_cost_of(slug, data), encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', render_cost_of(slug, data), flags=re.S)).split())
        print(f"  cost-of/{slug}  {wc}w")
        count += 1
    for slug, data in TEMPLATES.items():
        out = LANDING / "templates" / slug / "index.html"
        out.write_text(render_template(slug, data), encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', render_template(slug, data), flags=re.S)).split())
        print(f"  templates/{slug}  {wc}w")
        count += 1
    # Clean stale .html files
    for subdir, slugs in [("learn", LEARN), ("cost-of", COST_OF), ("templates", TEMPLATES)]:
        for slug in slugs:
            p = LANDING / subdir / f"{slug}.html"
            if (LANDING / subdir / slug / "index.html").exists() and p.exists():
                p.unlink()
                print(f"  removed stale {subdir}/{slug}.html")
    print(f"\nTotal: {count} pages")
if __name__ == "__main__": main()
