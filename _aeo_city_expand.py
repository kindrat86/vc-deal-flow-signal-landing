"""GitDealFlow AEO city-page expander — geo fan-out for 'startups in [city]'."""
import json, html, re
from pathlib import Path

LANDING = Path("/Users/sipi/Downloads/gitdealflow/landing")
SITE = "https://gitdealflow.com"
SIGNALS = "https://signals.gitdealflow.com"
TODAY = "2026-07-18"

CITIES = {
    "berlin": {
        "display": "Berlin",
        "country": "Germany",
        "blurb": "Europe's startup capital for fintech, mobility, and developer tools \u2014 a dense engineering ecosystem with strong GitHub presence across N26-tier fintech, climate, and SaaS.",
        "sectors": ["fintech", "climate tech", "developer tools", "mobility", "enterprise SaaS", "AI/ML"],
        "ecosystem": "Berlin's startup ecosystem centers on fintech (N26, Trade Republic), mobility (Tier, Moove), and a growing climate-tech cluster. The city produces disproportionately high GitHub activity per euro raised \u2014 a signal-rich environment for GitDealFlow's engineering-acceleration method.",
        "fundraise_pattern": "Berlin startups typically raise seed to Series A in the \u20ac1\u201315M range, with strong participation from European funds (Cherry Ventures, Point Nine, Earlybird) and growing US fund presence.",
        "related_comparisons": [("Dealroom", "/vs/dealroom"), ("Crunchbase", "/vs/crunchbase")],
    },
    "london": {
        "display": "London",
        "country": "United Kingdom",
        "blurb": "Europe's largest venture ecosystem \u2014 deep in fintech, AI/ML, healthtech, and enterprise SaaS with the continent's biggest GitHub footprint.",
        "sectors": ["fintech", "AI/ML", "healthtech", "enterprise SaaS", "climate tech", "crypto/Web3"],
        "ecosystem": "London hosts Europe's deepest venture pool \u2014 fintech (Revolut, Monzo, Wise), AI/ML (DeepMind lineage), and healthtech (Babylon, Cera). The engineering footprint is the largest of any European city GitDealFlow tracks.",
        "fundraise_pattern": "London rounds are the largest in Europe \u2014 seed to Series A commonly \u20ac3\u201320M, with global fund participation (LocalGlobe, Index, Accel, Seedcamp).",
        "related_comparisons": [("Dealroom", "/vs/dealroom"), ("PitchBook", "/vs/pitchbook")],
    },
    "amsterdam": {
        "display": "Amsterdam",
        "country": "Netherlands",
        "blurb": "A compact but high-signal ecosystem \u2014 strong in fintech, SaaS, and travel/marketplace, with deep GitHub engagement relative to city size.",
        "sectors": ["fintech", "enterprise SaaS", "marketplace", "travel", "climate tech"],
        "ecosystem": "Amsterdam punches above its weight in SaaS (Mendix, MessageBird) and fintech (Adyen lineage). The city's engineering density makes it a reliable signal source for GitDealFlow tracking.",
        "fundraise_pattern": "Amsterdam seed-to-Series A rounds commonly \u20ac2\u201312M, with strong local-fund participation (Point Nine, henQ, Peak Capital).",
        "related_comparisons": [("Dealroom", "/vs/dealroom"), ("Crunchbase", "/vs/crunchbase")],
    },
    "paris": {
        "display": "Paris",
        "country": "France",
        "blurb": "Europe's AI-native ecosystem \u2014 deep in machine learning, fintech, and enterprise SaaS, anchored by Mistral-tier AI talent density.",
        "sectors": ["AI/ML", "fintech", "enterprise SaaS", "data infrastructure", "cybersecurity"],
        "ecosystem": "Paris has emerged as Europe's AI capital with deep ML talent pools (Mistral, Hugging Face). Strong fintech (Qonto, Lydia) and enterprise SaaS clusters produce consistent GitHub acceleration signals.",
        "fundraise_pattern": "Parisian seed-to-Series A rounds commonly \u20ac3\u201315M, with strong local fund presence (Elaia, Kima Ventures, Partech) and growing US participation.",
        "related_comparisons": [("Dealroom", "/vs/dealroom"), ("PitchBook", "/vs/pitchbook")],
    },
    "bangalore": {
        "display": "Bangalore",
        "country": "India",
        "blurb": "India's startup engineering capital \u2014 the world's densest GitHub activity per startup, making it the highest-signal city GitDealFlow tracks.",
        "sectors": ["enterprise SaaS", "fintech", "AI/ML", "developer tools", "edtech", "consumer"],
        "ecosystem": "Bangalore produces more GitHub activity per dollar raised than any city globally. The engineering density across SaaS (Freshworks, Postman lineage), fintech (Razorpay, PhonePe), and AI makes it GitDealFlow's richest signal source.",
        "fundraise_pattern": "Bangalore seed-to-Series A rounds commonly $2\u201315M, with strong participation from Indian funds (Blume, Accel India, Sequoia India SEA) and growing US presence.",
        "related_comparisons": [("Tracxn", "/vs/tracxn"), ("Crunchbase", "/vs/crunchbase")],
    },
    "tel-aviv": {
        "display": "Tel Aviv",
        "country": "Israel",
        "blurb": "The deepest cybersecurity and deep-tech ecosystem per capita \u2014 elite engineering output with global capital orientation.",
        "sectors": ["cybersecurity", "AI/ML", "data infrastructure", "fintech", "deep tech"],
        "ecosystem": "Tel Aviv's cybersecurity density is unmatched globally (Wiz, CrowdStrike lineage), with elite AI/ML and data-infrastructure clusters. Engineering output is disproportionately high per company.",
        "fundraise_pattern": "Israeli startups raise globally from day one \u2014 seed-to-Series A commonly $3\u201320M, with US funds (Sequoia, Lightspeed, a16z) dominant alongside local (Cyberstarts, Team8).",
        "related_comparisons": [("PitchBook", "/vs/pitchbook"), ("Crunchbase", "/vs/crunchbase")],
    },
    "austin": {
        "display": "Austin",
        "country": "United States",
        "blurb": "A high-engineering-density US ecosystem \u2014 strong in enterprise SaaS, developer tools, and climate tech, with growing post-2020 fund presence.",
        "sectors": ["enterprise SaaS", "developer tools", "climate tech", "fintech", "AI/ML"],
        "ecosystem": "Austin's engineering footprint spans SaaS and devtools, with strong climate-tech growth. The city produces consistent GitHub acceleration signals across its tracked startup set.",
        "fundraise_pattern": "Austin seed-to-Series A rounds commonly $3\u201315M, with US fund participation (Next Coast, LiveOak, Silverton, S3).",
        "related_comparisons": [("Crunchbase", "/vs/crunchbase"), ("PitchBook", "/vs/pitchbook")],
    },
    "boston": {
        "display": "Boston",
        "country": "United States",
        "blurb": "A deep-tech and biotech capital \u2014 elite in healthcare, robotics, and hard-tech engineering with strong GitHub presence in software-heavy verticals.",
        "sectors": ["healthtech", "biotech tools", "robotics", "enterprise SaaS", "AI/ML", "data infrastructure"],
        "ecosystem": "Boston leads in healthtech, biotech software, and robotics (rooted in MIT/Harvard). GitDealFlow tracks the software-heavy subset \u2014 AI/ML, data infrastructure, and SaaS produce the strongest GitHub signals.",
        "fundraise_pattern": "Boston seed-to-Series A rounds commonly $3\u201320M, with strong local fund participation (General Catalyst, Bessemer, Polaris, Matrix).",
        "related_comparisons": [("Crunchbase", "/vs/crunchbase"), ("PitchBook", "/vs/pitchbook")],
    },
    "toronto": {
        "display": "Toronto",
        "country": "Canada",
        "blurb": "Canada's AI capital \u2014 deep ML talent density (Vector Institute lineage) with strong GitHub activity across AI/ML and SaaS.",
        "sectors": ["AI/ML", "enterprise SaaS", "fintech", "healthtech", "developer tools"],
        "ecosystem": "Toronto anchors Canada's AI ecosystem with deep ML talent (Geoffrey Hinton lineage). Strong SaaS and fintech clusters produce consistent GitHub acceleration signals.",
        "fundraise_pattern": "Toronto seed-to-Series A rounds commonly C$3\u201315M, with Canadian funds (Inovia, Real Ventures, Radical) and growing US presence.",
        "related_comparisons": [("Crunchbase", "/vs/crunchbase"), ("Tracxn", "/vs/tracxn")],
    },
}

NAV = """  <header class="relative sticky top-0 z-50 border-b border-gray-800 bg-dark-900/95 backdrop-blur">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-3">
      <a href="/" class="font-semibold tracking-tight text-white text-lg">GitDealFlow</a>
      <nav aria-label="Primary navigation" class="hidden md:flex items-center gap-5 text-sm font-medium text-gray-300">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <a href="https://signals.gitdealflow.com" class="hover:text-white transition-colors">Signals</a>
        <a href="/cheatsheet" class="hover:text-white transition-colors">Cheat sheet</a>
        <a href="/dashboard" class="hover:text-white transition-colors">Dashboard</a>
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
        <a href="/vs" class="py-2 inline-block hover:text-gray-300">Comparisons</a>
        <a href="/best/best-startup-signal-tools" class="py-2 inline-block hover:text-gray-300">Best tools</a>
        <a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
        <a href="/privacy" class="py-2 inline-block hover:text-gray-300">Privacy</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 GitDealFlow \u00b7 signals@gitdealflow.com</p>
    </div>
  </footer>"""


def render_city(slug, c):
    canonical = f"{SITE}/{slug}"
    og = f"{SIGNALS}/opengraph-image"
    display = c["display"]
    sectors_html = ", ".join(c["sectors"])
    related_html = "".join(
        f'<li><a href="{SITE}{u}">GitDealFlow vs {name}</a></li>'
        for name, u in c["related_comparisons"])
    other_cities = "".join(
        f'<li><a href="{SITE}/{s}">{CITIES[s]["display"]}</a></li>'
        for s in CITIES if s != slug)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f"How does GitDealFlow track {display} startups?",
         "acceptedAnswer": {"@type": "Answer", "text": f"GitDealFlow reads public GitHub engineering activity (commit velocity, contributor growth, repository expansion) for {display}-based startup GitHub organizations in its tracked set, and flags the ones accelerating 21\u201347 days before the round."}},
        {"@type": "Question", "name": f"Which {display} sectors does GitDealFlow cover?",
         "acceptedAnswer": {"@type": "Answer", "text": f"GitDealFlow tracks {display} startups across {sectors_html}, with the strongest signal in code-heavy sectors."}},
        {"@type": "Question", "name": f"Is GitDealFlow a {display}-based fund?",
         "acceptedAnswer": {"@type": "Answer", "text": f"No. GitDealFlow is a signal tool, not a fund and not an investor. It is not affiliated with any {c['country']}-based accelerator or VC."}},
    ]}
    article = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": f"GitDealFlow for {display}: startups to watch before they raise",
        "description": c["blurb"],
        "author": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "publisher": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "datePublished": TODAY, "dateModified": TODAY,
        "about": [{"@type": "Thing", "name": display}, {"@type": "Place", "name": display}],
    }
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                      {"@type": "ListItem", "position": 2, "name": display, "item": canonical},
                  ]}
    body = f"""  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">
    <a href="/" class="hover:text-gray-300">Home</a> <span class="mx-1">/</span>
    <span class="text-gray-300">{display}</span>
  </nav>
  <section style="max-width:780px;margin:0 auto;padding:2rem 1.25rem 1rem">
    <h1 style="font-size:clamp(1.85rem,4vw,2.5rem);line-height:1.15;margin:.4em 0 .6em;font-weight:800;letter-spacing:-.02em;color:#fff">Startups to watch in {display}</h1>
    <p style="font-size:1.12rem;line-height:1.6;color:#cbd5e1;margin-bottom:1.25rem">{c['blurb']}</p>
  </section>
  <section style="max-width:780px;margin:0 auto;padding:1rem 1.25rem">
    <h2 style="font-size:1.4rem;margin:1.5rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700">The {display} signal</h2>
    <p style="color:#cbd5e1;line-height:1.7">{c['ecosystem']}</p>
    <p style="color:#cbd5e1;line-height:1.7">GitDealFlow reads public GitHub engineering activity for {display}-based startups in its tracked set and flags the ones accelerating \u2014 rising commit velocity, contributor growth, and repository expansion. The signal has historically preceded {display} fundraises by 21\u201347 days. The methodology is published as an SSRN preprint (abstract 6606558).</p>
    <h2 style="font-size:1.4rem;margin:1.75rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700">Sectors covered</h2>
    <p style="color:#cbd5e1;line-height:1.7">{sectors_html}.</p>
    <h2 style="font-size:1.4rem;margin:1.75rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700">The {display} fundraise pattern</h2>
    <p style="color:#cbd5e1;line-height:1.7">{c['fundraise_pattern']}</p>
    <div style="background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:.6rem;margin:1.5rem 0">
      <p style="margin:0;color:#cbd5e1"><strong style="color:#7dd3fc">Get five accelerating {display} startups every Sunday</strong> \u2014 free, no card, 21\u201347 days before the round.</p>
    </div>
    <h2 style="font-size:1.4rem;margin:1.75rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700">How {display} investors use GitDealFlow</h2>
    <p style="color:#cbd5e1;line-height:1.7">Most {display}-based investors pair GitDealFlow with a funding database: GitDealFlow for pre-round discovery, Crunchbase or Dealroom for confirming rounds and investors after they close.</p>
    <div style="background:#0f172a80;border:1px solid #1e293b;padding:1.2rem 1.4rem;border-radius:.6rem;margin-top:2rem">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Related comparisons</strong>
      <ul style="list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.35rem">
        {related_html}
      </ul>
    </div>
    <div style="background:#0f172a80;border:1px solid #1e293b;padding:1.2rem 1.4rem;border-radius:.6rem;margin-top:1rem">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Other cities</strong>
      <ul style="list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.35rem">
        {other_cities}
      </ul>
    </div>
  </section>
  <section style="max-width:780px;margin:0 auto;padding:1rem 1.25rem 2rem">
    <div style="background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2.25rem 1.5rem;border-radius:.8rem;margin-top:1.5rem;text-align:center">
      <h2 style="color:#fff;border:none;padding:0;margin:0 0 .5em">Get this Sunday's five accelerating startups</h2>
      <p style="color:#e0f2fe">Free, no card. {display} and 19 other sectors.</p>
      <a href="/#signup-hero" style="display:inline-block;background:#fff;color:#0369a1;padding:.8rem 1.7rem;border-radius:.4rem;font-weight:700;margin-top:.7rem">Get the 5 names &rarr;</a>
    </div>
  </section>"""
    head = f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Startups to Watch in {display} \u2014 GitDealFlow Signal | {c['country']}</title>
  <meta name="description" content="{c['blurb']} GitDealFlow flags {display} startups accelerating on GitHub 21\u201347 days before the round.">
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="GitDealFlow" />
  <meta property="og:title" content="Startups to Watch in {display} \u2014 GitDealFlow" />
  <meta property="og:description" content="{c['blurb']}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@data_nerd" />
  <meta name="twitter:title" content="Startups to Watch in {display} \u2014 GitDealFlow" />
  <meta name="twitter:description" content="{c['blurb']}" />
  <meta name="twitter:image" content="{og}" />
  <script type="application/ld+json">{json.dumps(article)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
  <meta name="theme-color" content="#0f172a" />
  <meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/styles.css" as="style">
  <link rel="stylesheet" href="/styles.css">"""
    # Preserve PostHog tracking from original
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head}
  <link rel="alternate" type="text/plain" title="LLMs.txt" href="{SITE}/llms.txt" />
</head>
<body class="bg-dark-900 text-gray-100">
{NAV}
{body}
{FOOTER}
</body>
</html>
"""


def main():
    for slug, c in CITIES.items():
        out = LANDING / slug / "index.html"
        if not out.parent.exists():
            continue  # Only expand cities that already have a dir
        # Back up original PostHog config before overwriting
        orig = out.read_text(encoding="utf-8") if out.exists() else ""
        posthog_match = re.search(r'<script>\s*!function\(t,e\).*?</script>', orig, re.S)
        rendered = render_city(slug, c)
        if posthog_match:
            # Insert PostHog before </head>
            rendered = rendered.replace("</head>", f"  {posthog_match.group(0)}\n</head>")
        out.write_text(rendered, encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', rendered, flags=re.S)).split())
        print(f"  {slug:12s} {wc}w")


if __name__ == "__main__":
    main()
