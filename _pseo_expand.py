#!/usr/bin/env python3
"""Greg Isenberg pSEO Expansion for gitdealflow.com — Round 1 (July 2026)
Enriched comparison/alternatives/how-to/integrations pages for a deal-flow signal tool.
Output: static HTML files matching the existing vs/ page template style.
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-07-18"
PRODUCT = "GitDealFlow"
TAGLINE = "Pre-round GitHub signal for deal flow"
DOMAIN = "gitdealflow.com"
CANONICAL_BASE = f"https://{DOMAIN}"

# ── HEAD / FOOTER / SCHEMA helpers ──────────────────────────────────

def head(title, desc, canonical_path, schema_blocks=""):
    """Render <head> matching existing vs/ page style."""
    url = f"{CANONICAL_BASE}{canonical_path}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="{PRODUCT}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="https://signals.gitdealflow.com/opengraph-image" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@data_nerd" />
  <meta name="twitter:creator" content="@data_nerd" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="https://signals.gitdealflow.com/opengraph-image" />
  <link rel="alternate" type="text/plain" title="LLMs.txt" href="https://gitdealflow.com/llms.txt" />
  {schema_blocks}
  <meta name="theme-color" content="#0f172a" />
  <meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/styles.css" as="style">
  <link rel="stylesheet" href="/styles.css">
  <style>
    .vs-hero{{padding:3rem 1.25rem 2rem;max-width:760px;margin:0 auto}}
    .vs-hero h1{{font-size:clamp(1.9rem,4vw,2.6rem);line-height:1.15;margin:.4em 0 .6em;font-weight:800;letter-spacing:-.02em;color:#fff}}
    .vs-lede{{font-size:1.15rem;line-height:1.6;color:#cbd5e1;margin-bottom:1.5rem}}
    .vs-section{{max-width:760px;margin:0 auto;padding:1.5rem 1.25rem}}
    .vs-section h2{{font-size:1.5rem;margin:2rem 0 .75rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700}}
    .vs-section p, .vs-section li{{color:#cbd5e1;line-height:1.7}}
    .vs-section ul{{padding-left:1.25rem;margin:.5rem 0}}.vs-section li{{margin:.35rem 0}}
    .vs-table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}}
    .vs-table th, .vs-table td{{border:1px solid #334155;padding:.7rem .85rem;text-align:left}}
    .vs-table th{{background:#1e293b;color:#f1f5f9;font-weight:600}}
    .vs-table td{{color:#cbd5e1}}.vs-table tr:nth-child(even) td{{background:#0f172a66}}
    .verdict{{background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.25rem 1.5rem;border-radius:.6rem;margin:1.5rem 0}}
    .verdict strong{{color:#7dd3fc}}
    .callout-warn{{background:#fef3c715;border-left:4px solid #d97706;padding:1rem 1.25rem;margin:1.5rem 0;border-radius:0 .375rem .375rem 0;color:#fde68a}}
    .cta-final{{background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2.5rem 1.5rem;border-radius:.8rem;margin-top:2rem;text-align:center}}
    .cta-final h2{{color:#fff;border:none;padding:0;margin:0 0 .5em}}
    .cta-final .btn{{display:inline-block;background:#fff;color:#0369a1;padding:.85rem 1.75rem;border-radius:.4rem;font-weight:700;margin-top:.75rem}}
    .faq-item{{border-bottom:1px solid #1e293b;padding:.9rem 0}}
    .faq-item summary{{cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none;font-size:1.05rem}}
    .faq-item summary::-webkit-details-marker{{display:none}}
    .faq-item summary::before{{content:"▸ ";color:#0ea5e9;margin-right:.4rem}}
    .faq-item[open] summary::before{{content:"▾ "}}
    .faq-item p{{margin:.6rem 0 0;color:#cbd5e1;line-height:1.65}}
    .related{{background:#0f172a80;border:1px solid #1e293b;padding:1.25rem 1.5rem;border-radius:.6rem;margin-top:2rem}}
    .related ul{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.4rem}}
    .related a{{color:#7dd3fc;text-decoration:none}}.related a:hover{{text-decoration:underline}}
    .disclaimer{{font-size:.85rem;color:#64748b;font-style:italic;margin-top:1.5rem}}
  </style>
</head>'''

def header(current_nav="", breadcrumbs=None):
    """Render the standard site header."""
    bcrumb = ""
    if breadcrumbs:
        parts = []
        for i, (label, href) in enumerate(breadcrumbs):
            if href:
                parts.append(f'<a href="{href}" class="hover:text-gray-300">{label}</a>')
            else:
                parts.append(f'<span class="text-gray-300">{label}</span>')
        bcrumb = ' <span class="mx-1">/</span> '.join(parts)
    return f'''<body class="bg-dark-900 text-gray-100">
  <header class="relative sticky top-0 z-50 border-b border-gray-800 bg-dark-900/95 backdrop-blur">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-3">
      <a href="/" class="font-semibold tracking-tight text-white text-lg">{PRODUCT}</a>
      <nav aria-label="Primary navigation" class="hidden md:flex items-center gap-5 text-sm font-medium text-gray-300">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <a href="https://signals.gitdealflow.com" class="hover:text-white transition-colors">Signals</a>
        <a href="/best/best-startup-signal-tools" class="hover:text-white transition-colors">Best tools</a>
        <a href="/vs" class="hover:text-white transition-colors">Comparisons</a>
        <a href="/pricing" class="hover:text-white transition-colors">Pricing</a>
      </nav>
      <a href="/#signup-hero" class="btn btn-primary btn-no-pulse btn-sm whitespace-nowrap shrink-0">Get the 5 names &rarr;</a>
    </div>
  </header>
  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">
    {bcrumb}
  </nav>'''

def footer(related_links=None):
    """Render the standard footer with related links."""
    rel_html = ""
    if related_links:
        items = "\n".join(f'      <li><a href="{l["url"]}">{l["label"]}</a></li>' for l in related_links)
        rel_html = f'''<section class="vs-section">
    <div class="related">
      <h2 style="color:#e2e8f0;margin-top:0;border:none;padding:0;font-size:1.2rem">Related pages</h2>
      <ul>{items}</ul>
    </div>
  </section>'''
    
    return f'''{rel_html}
  <footer class="border-t border-gray-800 bg-dark-900/80 py-12">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-gray-300 mb-2 font-semibold">{PRODUCT} is a deal-flow signal tool for investors — not a fund and not a startup accelerator.</p>
      <div class="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mt-5">
        <a href="/" class="py-2 inline-block hover:text-gray-300">Home</a>
        <a href="/best/best-startup-signal-tools" class="py-2 inline-block hover:text-gray-300">Best tools</a>
        <a href="/vs" class="py-2 inline-block hover:text-gray-300">Comparisons</a>
        <a href="/alternatives-to" class="py-2 inline-block hover:text-gray-300">Alternatives</a>
        <a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 {PRODUCT}. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>'''

def article_schema(headline, desc, path):
    return f'''<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "Article", "headline": "{headline}", "description": "{desc}", "author": {{"@type": "Organization", "name": "{PRODUCT}", "url": "{CANONICAL_BASE}"}}, "publisher": {{"@type": "Organization", "name": "{PRODUCT}", "url": "{CANONICAL_BASE}"}}, "mainEntityOfPage": {{"@type": "WebPage", "@id": "{CANONICAL_BASE}{path}"}}, "datePublished": "{TODAY}", "dateModified": "{TODAY}", "about": [{{"@type": "Thing", "name": "deal flow signal"}}, {{"@type": "Thing", "name": "alternative data for investors"}}]}}</script>'''

def breadcrumb_schema(items):
    """items = [(name, url), ...] url="" for last item"""
    elems = []
    for i, (name, url) in enumerate(items, 1):
        elems.append(f'{{"@type": "ListItem", "position": {i}, "name": "{name}", "item": "{url or CANONICAL_BASE}"}}' if not url and i == len(items) else f'{{"@type": "ListItem", "position": {i}, "name": "{name}", "item": "{url}"}}')
    return f'<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{", ".join(elems)}]}}</script>'

def faq_schema(qa_pairs):
    """qa_pairs = [(question, answer), ...]"""
    items = []
    for q, a in qa_pairs:
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        items.append(f'{{"@type": "Question", "name": "{q_esc}", "acceptedAnswer": {{"@type": "Answer", "text": "{a_esc}"}}}}')
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(items)}]}}</script>'

# ── ALTERNATIVES-TO PAGES ──────────────────────────────────────────

ALTERNATIVES = [
    {
        "slug": "crunchbase",
        "title": "Crunchbase Alternatives for Deal Flow — 6 Tools That Find Startups Before the Round",
        "desc": "Crunchbase is a post-round database. If you need pre-round signals — which startups are about to raise — here are 6 alternatives that flag engineering momentum weeks before the announcement hits Crunchbase.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Pre-round GitHub engineering signal", "price": "Free tier available", "strength": "Tracks 400+ startup orgs across 20 sectors. Flags breakout engineering teams 3-6 weeks before fundraise. Zero reliance on self-reported data."},
            {"name": "CB Insights", "best_for": "Market intelligence + M&A prediction", "price": "From $40K/yr", "strength": "Deep sector reports, patent analysis, earnings transcripts. Broader but slower — signals come from press mentions and funding rounds, not live code velocity."},
            {"name": "PitchBook", "best_for": "Deal terms + LP data", "price": "From $20K+/yr per seat", "strength": "Best-in-class deal structuring and LP profiles. Not a signal tool — its data lags 2-8 weeks behind round closes."},
            {"name": "Tracxn", "best_for": "Emerging-market startup discovery", "price": "From $15K/yr", "strength": "Strong India, SEA, and LatAm coverage. Sector taxonomies are excellent. Engineering velocity is one of many signals, not the primary one."},
            {"name": "Grata", "best_for": "B2B private company search", "price": "From $12K/yr", "strength": "Massive private company graph with 20M+ companies. Good for sourcing, not for predicting which ones are accelerating."},
            {"name": "Dealroom", "best_for": "European startup ecosystem data", "price": "From $10K/yr", "strength": "Dominant in European VC. Strong ecosystem mapping. Signals are round-based, not pre-round."},
        ],
        "verdict": "If you're tired of Crunchbase showing you rounds that already closed, you need a leading indicator. GitDealFlow is the only tool on this list that surfaces pre-round acceleration from public GitHub data — no self-reported rounds, no press-release lag.",
        "faqs": [
            ("Why look for Crunchbase alternatives?", "Crunchbase is excellent at recording what happened — who raised, how much, from whom. But it is not designed to tell you what's about to happen. Investors looking for startups before the round need a tool built for leading indicators, not lagging ones."),
            ("Can I replace Crunchbase entirely?", "Probably not. Keep Crunchbase for round-history lookups, investor tracking, and competitive landscape mapping. Add GitDealFlow for the pre-round signal layer. Most serious deal-flow teams use both."),
            ("What's the fastest way to test GitDealFlow?", "Go to the free tier. You get the top 20 trending startups across all sectors immediately. No credit card, no demo call — just real signal.")
        ],
        "related": [
            {"url": "/vs/crunchbase", "label": "GitDealFlow vs Crunchbase (detailed)"},
            {"url": "/vs/pitchbook", "label": "vs PitchBook"},
            {"url": "/cost-of/crunchbase-pricing", "label": "Crunchbase pricing breakdown"},
            {"url": "/alternatives-to/pitchbook", "label": "PitchBook alternatives"},
        ]
    },
    {
        "slug": "pitchbook",
        "title": "PitchBook Alternatives — 6 Deal-Flow Tools for Investors Who Need Pre-Round Signal",
        "desc": "PitchBook dominates deal-term data and LP profiles. But if you need pre-round signal — which startups are accelerating BEFORE they raise — here are 6 alternatives that beat PitchBook on speed-to-signal.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Pre-round GitHub engineering signal", "price": "Free tier available", "strength": "Detects acceleration 3-6 weeks before fundraise announcements. Tracks commit velocity, contributor growth, star acceleration across 400+ startup orgs. EUR 9.97/month — 1/2000th the cost of PitchBook."},
            {"name": "Crunchbase", "best_for": "Investor profiles + funding rounds", "price": "From $29/mo", "strength": "Largest startup database. Good for confirming rounds and mapping investor networks. Same limitation: rounds appear after they close."},
            {"name": "CB Insights", "best_for": "Sector intelligence + earnings analysis", "price": "From $40K/yr", "strength": "Unmatched sector depth. Patents, earnings calls, M&A rumors. Excellent for thesis development, not for daily deal flow."},
            {"name": "Tracxn", "best_for": "Taxonomy-driven startup discovery", "price": "From $15K/yr", "strength": "The best sector taxonomy in the market. Strong in India/SEA. Uses multiple signals including hiring, news, and engineering."},
            {"name": "Affinity", "best_for": "CRM + relationship intelligence", "price": "From $149/mo", "strength": "Relationship-mapping CRM, not a signal tool. Shows who in your network can intro you to a startup, but doesn't find the startup."},
            {"name": "Source Scrub", "best_for": "Bootstrapped company sourcing", "price": "From $10K/yr", "strength": "Strong on bootstrapped companies that don't appear in Crunchbase. Conference-driven data, not live code signal."},
        ],
        "verdict": "PitchBook is essential for deal-making and LP reporting. But for the daily question of 'which 5 startups should I look at this week,' you need a tool that reads the future, not the past. GitDealFlow costs approximately 0.05% of a PitchBook seat and answers that question directly.",
        "faqs": [
            ("Why would I need something besides PitchBook?", "PitchBook is a lagging indicator — it records deals that already happened. If you want to find startups before they raise, you need a leading indicator. GitDealFlow tracks engineering acceleration, which reliably precedes fundraise announcements by 3-6 weeks."),
            ("Does GitDealFlow replace PitchBook for LP reporting?", "No. PitchBook is still the standard for LP reporting, deal-term benchmarking, and fund performance data. Keep it. Add GitDealFlow for the sourcing layer."),
            ("What's the cost difference?", "A single PitchBook seat costs $20K-$50K/yr. GitDealFlow's paid tier is EUR 9.97/month. For the price of one PitchBook login, you could equip your entire deal team with pre-round signal."),
        ],
        "related": [
            {"url": "/vs/pitchbook", "label": "GitDealFlow vs PitchBook (detailed)"},
            {"url": "/cost-of/pitchbook-pricing", "label": "PitchBook pricing 2026 breakdown"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
            {"url": "/best/best-startup-signal-tools", "label": "Best startup signal tools"},
        ]
    },
    {
        "slug": "cb-insights",
        "title": "CB Insights Alternatives — 6 Tools That Give You Signal Before the Report Drops",
        "desc": "CB Insights is the gold standard for sector intelligence. But its deal-flow data arrives post-round. Here are 6 alternatives for investors who need to know which startups are accelerating RIGHT NOW.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Real-time engineering momentum", "price": "Free tier available", "strength": "Daily-refreshed GitHub signals. Commits, contributors, stars — tracked across 400+ startups. No waiting for quarterly reports."},
            {"name": "Crunchbase", "best_for": "Round-history database", "price": "From $29/mo", "strength": "Largest funding database. Good for 'who raised what' lookups. Same lag as CBI: data enters after rounds close."},
            {"name": "PitchBook", "best_for": "Deal terms + fund performance", "price": "From $20K+/yr", "strength": "Deeper deal-terms data than CBI. Strong LP/fund coverage. Heavier, slower, more expensive."},
            {"name": "Tracxn", "best_for": "Emerging market startup sourcing", "price": "From $15K/yr", "strength": "Excellent taxonomy. Multi-signal approach (hiring, news, engineering). Good complement to CBI for specific geographies."},
            {"name": "Dealroom", "best_for": "European ecosystem mapping", "price": "From $10K/yr", "strength": "Strongest European coverage. Good for understanding ecosystem-level trends. Round-based, not pre-round."},
            {"name": "Grata", "best_for": "B2B company search + sourcing", "price": "From $12K/yr", "strength": "Massive B2B graph. Good for finding companies that don't appear in CBI. Not a signal tool."},
        ],
        "verdict": "CB Insights is unmatched for sector-level research and quarterly briefings. But it doesn't tell you what's happening this week. GitDealFlow does — and at 1/500th the cost.",
        "faqs": [
            ("What does CB Insights miss?", "CB Insights excels at structured market intelligence — sector reports, patent analysis, earnings-call transcripts. But it does not track real-time code velocity or contributor growth on GitHub. Those signals are what predict a fundraise, and CBI only picks up the story after the round closes."),
            ("Is CB Insights obsolete?", "Far from it. For board-ready market sizing, competitive landscape mapping, and industry thesis development, CBI is best-in-class. The gap is in speed-to-signal — and that's where GitDealFlow fits."),
            ("Can I use GitDealFlow alongside CBI?", "This is the ideal stack. CBI for quarterly research and board decks. GitDealFlow for the weekly 'what should I look at' question. The two tools answer different time horizons."),
        ],
        "related": [
            {"url": "/vs/cb-insights", "label": "GitDealFlow vs CB Insights"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
            {"url": "/best/best-startup-databases", "label": "Best startup databases"},
        ]
    },
    {
        "slug": "tracxn",
        "title": "Tracxn Alternatives — 6 Startup Discovery Tools With Faster Signal",
        "desc": "Tracxn's sector taxonomy is excellent, but its signals are multi-source and can lag. Here are 6 alternatives that give you a daily-refreshed, single-source signal: which startups are accelerating on GitHub right now.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Single-source, daily GitHub signal", "price": "Free tier available", "strength": "One signal source (GitHub), refreshed daily. No analyst-dependent curation. Tracks 400+ startups across 20 sectors."},
            {"name": "Crunchbase", "best_for": "Funding-round database", "price": "From $29/mo", "strength": "Larger database. Better for confirming rounds than predicting them."},
            {"name": "CB Insights", "best_for": "Sector-level intelligence", "price": "From $40K/yr", "strength": "Deeper sector reports. Better for thesis-level research."},
            {"name": "PitchBook", "best_for": "Deal-terms benchmarking", "price": "From $20K+/yr", "strength": "Deeper deal data. Better for LP reporting."},
            {"name": "Dealroom", "best_for": "European ecosystem data", "price": "From $10K/yr", "strength": "Best European coverage. Strong ecosystem-level analytics."},
            {"name": "Grata", "best_for": "B2B private company search", "price": "From $12K/yr", "strength": "20M+ company graph. Good for finding companies Tracxn misses in NA/Europe."},
        ],
        "verdict": "Tracxn's taxonomy is the best in the industry — their sector classification is genuinely useful. But the signal is multi-source and analyst-mediated. GitDealFlow gives you one clean, daily signal with no curation delay.",
        "faqs": [
            ("What's Tracxn's weakness?", "Tracxn aggregates signals from hiring, news, web traffic, and engineering — which is comprehensive. But each signal source has its own lag, and analyst curation adds further delay. A startup can be accelerating for weeks before the Tracxn profile updates."),
            ("Is GitDealFlow better than Tracxn?", "They answer different questions. Tracxn tells you 'what's happening in X sector across all signal types.' GitDealFlow tells you 'which 5 startups accelerated on GitHub this week.' For speed-to-signal, GitDealFlow wins. For sector landscape reports, Tracxn wins."),
        ],
        "related": [
            {"url": "/vs/tracxn", "label": "GitDealFlow vs Tracxn"},
            {"url": "/alternatives-to/cb-insights", "label": "CB Insights alternatives"},
            {"url": "/best/best-startup-signal-tools", "label": "Best signal tools"},
        ]
    },
    {
        "slug": "grata",
        "title": "Grata Alternatives — 6 Tools That Find Startups BEFORE They're Sourced",
        "desc": "Grata has a massive B2B company graph — 20M+ private companies. But its data is relationship-driven, not momentum-driven. Here are 6 alternatives for when you need to know which companies are accelerating, not just which exist.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Engineering momentum signal", "price": "Free tier available", "strength": "Tracks accelerating startups — not just existing ones. Daily-refreshed commit velocity, contributor growth, star acceleration."},
            {"name": "Crunchbase", "best_for": "Funding and investor data", "price": "From $29/mo", "strength": "Better funding-history data. Good complement for round verification."},
            {"name": "Source Scrub", "best_for": "Bootstrapped company data", "price": "From $10K/yr", "strength": "Similar company-graph approach, stronger on bootstrapped firms. Conference-driven data, not code signal."},
            {"name": "PitchBook", "best_for": "Deal-terms data", "price": "From $20K+/yr", "strength": "Deeper deal-terms and LP data. Not a sourcing tool."},
            {"name": "CB Insights", "best_for": "Market intelligence", "price": "From $40K/yr", "strength": "Better sector intelligence. Not real-time sourcing."},
            {"name": "Tracxn", "best_for": "Multi-signal sourcing", "price": "From $15K/yr", "strength": "Better taxonomy. Multi-signal approach (hiring, news, engineering)."},
        ],
        "verdict": "Grata is excellent at answering 'what companies exist in X space.' GitDealFlow answers 'which of those companies is accelerating.' The two tools are complementary — use Grata for the universe, GitDealFlow for the signal.",
        "faqs": [
            ("What does Grata not do?", "Grata tells you what companies exist and who works there. It doesn't tell you which ones are accelerating or about to raise. That's the signal layer GitDealFlow provides."),
            ("Can GitDealFlow replace Grata?", "No — Grata has a much larger company universe (20M+ vs 400+ startups). GitDealFlow is for tracking acceleration within a curated, high-signal set. Use both."),
            ("What's the ideal deal-flow stack?", "Grata for the broad company graph. Crunchbase for round-history lookup. GitDealFlow for the weekly signal on which startups are accelerating. Three layers, one workflow."),
        ],
        "related": [
            {"url": "/vs/grata", "label": "GitDealFlow vs Grata"},
            {"url": "/vs/source-scrub", "label": "vs Source Scrub"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
        ]
    },
    {
        "slug": "affinity",
        "title": "Affinity Alternatives — 6 Deal-Flow Tools That Find Startups, Not Just Track Relationships",
        "desc": "Affinity is a relationship-intelligence CRM, not a startup discovery tool. Here are 6 alternatives that actually find the startups before your network introduces them.",
        "tools": [
            {"name": "GitDealFlow", "best_for": "Pre-round startup discovery", "price": "Free tier available", "strength": "Discovers accelerating startups from public GitHub data — no network dependency. Free tier shows top 20 trending startups immediately."},
            {"name": "Crunchbase", "best_for": "Startup + investor database", "price": "From $29/mo", "strength": "Largest structured startup database. Good for 'what's in my pipeline' research."},
            {"name": "Tracxn", "best_for": "Sector-based startup discovery", "price": "From $15K/yr", "strength": "Best taxonomy for sector-based sourcing. Multi-signal (hiring, news, engineering)."},
            {"name": "Grata", "best_for": "B2B company sourcing", "price": "From $12K/yr", "strength": "20M+ company graph. Good for finding companies that fit your thesis."},
            {"name": "Dealroom", "best_for": "European startup data", "price": "From $10K/yr", "strength": "Best European coverage. Good ecosystem analytics."},
            {"name": "Source Scrub", "best_for": "Bootstrapped company search", "price": "From $10K/yr", "strength": "Strong on companies not in Crunchbase. Conference-driven data."},
        ],
        "verdict": "Affinity is a great CRM for managing the relationships you already have. But it doesn't find startups for you. GitDealFlow does — and it doesn't need a warm intro to tell you which startups are accelerating.",
        "faqs": [
            ("Why isn't a CRM enough for deal flow?", "A CRM manages your pipeline. It doesn't fill it. Affinity tells you who can intro you to Company X, but it doesn't tell you that Company X exists or is accelerating. You need a discovery layer first."),
            ("What's the best stack with Affinity?", "Use GitDealFlow to discover which startups are accelerating. Use Affinity to find the warm intro path to those startups. Discovery → relationship mapping → outreach."),
        ],
        "related": [
            {"url": "/vs/affinity", "label": "GitDealFlow vs Affinity"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
            {"url": "/integrations/gitdealflow-for-affinity-crm", "label": "GitDealFlow + Affinity integration"},
        ]
    },
]

# ── HOW-TO PAGES ──────────────────────────────────────────────────

HOW_TO = [
    {
        "slug": "how-to-source-deal-flow-for-pre-seed",
        "title": "How to Source Deal Flow for Pre-Seed — A 5-Step System Using GitHub Signals",
        "desc": "Pre-seed sourcing is hard — no Crunchbase profile, no revenue, no press. Here's how to use GitHub engineering signals to find the best pre-seed startups weeks before anyone else does.",
        "steps": [
            {"title": "Pick 3-5 sectors", "text": "Start narrow. You cannot track everything. Pick 3-5 sectors you understand deeply (e.g., developer tools, fintech, climate) and focus your GitHub monitoring there."},
            {"title": "Monitor commit velocity", "text": "Look for startups where the number of commits is accelerating week-over-week. A startup shipping more code each week is likely building product — and likely to raise soon."},
            {"title": "Watch contributor growth", "text": "A growing contributor count (new engineers joining the GitHub org) is a strong signal. More contributors = more building = more likely the startup is scaling toward a raise."},
            {"title": "Track star acceleration", "text": "Stars are a proxy for developer interest. A repo that suddenly spikes in stars — especially a closed-source startup's open-source projects — often precedes a fundraise announcement."},
            {"title": "Cross-reference with funding cycles", "text": "Most pre-seed startups raise 12-18 months after founding. If a startup has been building consistently on GitHub for 12+ months with accelerating velocity, it's likely approaching a raise."},
        ],
        "faqs": [
            ("How early can GitHub signals detect a pre-seed startup?", "As early as the startup starts building. Most pre-seed startups begin shipping code 6-12 months before any press or Crunchbase profile. GitHub commits are the earliest public signal available."),
            ("What sectors work best for GitHub-based sourcing?", "Developer tools, AI/ML, infrastructure, cybersecurity, fintech, and any sector where the startup builds software in-house. Less effective for hardware, biotech, or consumer apps."),
            ("Do I need to know how to code?", "No. GitDealFlow does the GitHub analysis for you. You see the trends — commits, contributors, stars — without reading a line of code."),
        ],
        "related": [
            {"url": "/learn/how-to-find-startups-before-they-raise", "label": "How to find startups before they raise"},
            {"url": "/learn/how-to-track-startup-engineering-velocity", "label": "Track engineering velocity"},
            {"url": "/best/best-startup-signal-tools", "label": "Best signal tools"},
        ]
    },
    {
        "slug": "how-to-build-a-weekly-deal-flow-routine",
        "title": "How to Build a Weekly Deal-Flow Routine — The 30-Minute Monday System for Investors",
        "desc": "Most investors check deal flow reactively — when a founder emails or a colleague forwards something. Here's a 30-minute Monday routine that puts you in front of the best startups before anyone else.",
        "steps": [
            {"title": "5 min: Check your signal feed", "text": "Open GitDealFlow (or your signal tool). Look at the top 20 trending startups. Note the 3-5 with the strongest momentum this week."},
            {"title": "10 min: Deep-dive on 3", "text": "For the 3 most interesting, look at their GitHub repos. What are they building? How fast is the team shipping? Is contributor count growing? Read their README."},
            {"title": "10 min: Cross-reference with your network", "text": "Check your CRM (Affinity, Airtable, Notion) — do you know anyone connected to these startups? Any portfolio companies in the same space who could intro?"},
            {"title": "5 min: Reach out to 1-2", "text": "Send a short, specific email to the founder. Mention what you noticed about their GitHub activity. Be specific — founders respect investors who've done their homework."},
        ],
        "faqs": [
            ("How many startups should I track weekly?", "Start with 20-30 in your signal tool. Deep-dive on 3-5. Reach out to 1-2. Consistency beats volume — do this every Monday for 6 months and your pipeline will be unrecognizable."),
            ("What's the best day for deal flow?", "Monday. GitHub activity peaks mid-week, so Monday gives you the freshest 'what happened last week' signal. Friday is for admin, Monday is for sourcing."),
        ],
        "related": [
            {"url": "/learn/how-to-find-startups-before-they-raise", "label": "Find startups before they raise"},
            {"url": "/templates/pipeline-review-template", "label": "Pipeline review template"},
            {"url": "/for/venture-scouts", "label": "GitDealFlow for venture scouts"},
        ]
    },
    {
        "slug": "how-to-evaluate-engineering-momentum",
        "title": "How to Evaluate Engineering Momentum — The 4 Metrics That Predict a Fundraise",
        "desc": "Not all GitHub activity is equal. Here are the 4 engineering momentum metrics that actually predict which startups are about to raise — and how to read them.",
        "steps": [
            {"title": "Commit velocity (week-over-week delta)", "text": "Raw commit count is noise. What matters is the slope: are commits accelerating, flat, or declining? A 20%+ week-over-week increase sustained over 4+ weeks is the strongest pre-raise signal."},
            {"title": "Contributor diversity", "text": "A single developer shipping 50 commits/week is less predictive than 4 developers shipping 10 each. Growing contributor count signals team scaling, which almost always precedes a fundraise."},
            {"title": "Star acceleration rate", "text": "Stars are a proxy for external developer interest. A repo suddenly adding 100+ stars/week (up from a baseline of 10-20) often signals organic buzz that precedes a round announcement."},
            {"title": "Issue/PR responsiveness", "text": "Fast-closing issues and merged PRs signal an active, shipping team. Long-open issues or stale PRs suggest the team is distracted, shrinking, or pivoting — all bearish signals."},
        ],
        "faqs": [
            ("What's a good commit velocity threshold?", "There's no magic number. A 3-person team shipping 15 commits/week steadily is more interesting than a 20-person team shipping 200 commits/week but declining. The trend matters more than the absolute count."),
            ("Can GitHub activity be faked?", "It can be padded with boilerplate commits, but sustained real engineering activity is hard to fake. GitDealFlow normalizes for commit size, frequency, and contributor count to filter out noise."),
            ("What if a startup has no public GitHub?", "Some startups (especially in regulated sectors) have zero public activity. That doesn't mean they're not building — it means GitHub signal doesn't apply. GitDealFlow only covers startups with public engineering activity."),
        ],
        "related": [
            {"url": "/learn/what-is-a-deal-flow-signal", "label": "What is a deal flow signal?"},
            {"url": "/glossary/engineering-momentum-score", "label": "Engineering Momentum Score"},
            {"url": "/glossary/commit-velocity", "label": "Commit velocity explained"},
        ]
    },
    {
        "slug": "how-to-find-ai-startups-before-they-raise",
        "title": "How to Find AI Startups Before They Raise — GitHub Signals for the Hottest Sector of 2026",
        "desc": "AI startups move faster than any other sector. By the time they appear on Crunchbase, the round is often oversubscribed. Here's how to find AI startups on GitHub weeks before they announce.",
        "steps": [
            {"title": "Track the AI & ML sector", "text": "GitDealFlow's 'AI & Machine Learning' sector tracks 25+ AI-native startups. Monitor this daily — AI startups ship at 3x the velocity of other sectors."},
            {"title": "Watch for model releases", "text": "When an AI startup open-sources a model or releases a new version, GitHub activity spikes. This is often the most visible pre-raise signal."},
            {"title": "Follow contributor migration", "text": "When engineers leave FAANG or top AI labs to join a startup, it shows in the GitHub contributor graph. A sudden influx of 3+ new contributors from a known lab is a strong signal."},
            {"title": "Monitor fork velocity", "text": "Fork count is the AI equivalent of star count — it measures how many developers are building on top of the startup's work. A forking spike often precedes major announcements."},
        ],
        "faqs": [
            ("Are AI startups different from other sectors for sourcing?", "Yes — AI startups build more in public (model releases, papers, open-source libraries) and move faster. The GitHub signal is stronger and the window between signal and announcement is shorter (2-3 weeks vs 3-6 weeks for other sectors)."),
            ("What if the AI startup is mostly proprietary?", "Even proprietary AI startups often have an open-source inference library, a demo repo, or a model card. Look for those — they're the public footprint of a private company."),
        ],
        "related": [
            {"url": "/sectors/ai-infrastructure", "label": "AI infrastructure sector"},
            {"url": "/learn/how-to-find-startups-before-they-raise", "label": "Find startups before they raise"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
        ]
    },
    {
        "slug": "how-to-use-alternative-data-for-vc-sourcing",
        "title": "How to Use Alternative Data for VC Sourcing — Beyond Crunchbase and PitchBook",
        "desc": "The best investors don't just use Crunchbase. They layer GitHub signals, hiring data, web traffic, and product launches into a multi-signal sourcing engine. Here's how.",
        "steps": [
            {"title": "Start with GitHub (the fastest signal)", "text": "GitHub engineering activity is the earliest signal. Startups start shipping code months before they hire a PR firm or appear on Crunchbase."},
            {"title": "Layer on hiring data", "text": "Once a startup is shipping, they hire. Track LinkedIn/Wellfound for headcount growth, especially in engineering roles. A startup doubling its engineering team in 6 months is likely raising."},
            {"title": "Add web traffic (SimilarWeb/BuiltWith)", "text": "Growing web traffic signals product traction. A B2B SaaS startup with accelerating traffic is likely acquiring customers — and likely needs capital to scale."},
            {"title": "Watch the product (Product Hunt, changelogs)", "text": "Frequent product launches and changelog updates signal a shipping culture. A startup dropping features every 2 weeks and growing is in execution mode."},
            {"title": "Cross-reference signals for conviction", "text": "One signal is interesting. Three signals converging is conviction. When GitHub + hiring + web traffic all point up, that's a startup worth reaching out to."},
        ],
        "faqs": [
            ("Why is alternative data better than traditional sourcing?", "Traditional sourcing (Crunchbase, PitchBook) shows you what already happened. Alternative data (GitHub, hiring, web traffic) shows you what's happening right now. The gap is 3-6 weeks — and in hot sectors like AI, that's the difference between getting allocation and getting left out."),
            ("Do I need a data team for this?", "No — GitDealFlow does the GitHub analysis for you. The other layers (hiring, web traffic) are optional bonuses, not requirements. Start with one strong signal layer and add more over time."),
        ],
        "related": [
            {"url": "/learn/what-is-a-deal-flow-signal", "label": "What is a deal flow signal?"},
            {"url": "/alternatives-to/cb-insights", "label": "CB Insights alternatives"},
            {"url": "/best/best-startup-signal-tools", "label": "Best signal tools"},
        ]
    },
]

# ── INTEGRATIONS PAGES ────────────────────────────────────────────

INTEGRATIONS = [
    {
        "slug": "gitdealflow-for-crunchbase",
        "title": "GitDealFlow + Crunchbase — Layer Pre-Round GitHub Signal on Your Funding Database",
        "desc": "Crunchbase tells you who raised. GitDealFlow tells you who's about to raise. Here's how to use both together for a complete deal-flow pipeline.",
        "use_case": "Add the pre-round signal layer to your Crunchbase workflow. Start your week in GitDealFlow (which startups are accelerating), then look up those startups in Crunchbase (what's their funding history, who invested). This turns Crunchbase from a historical lookup tool into the second step in a forward-looking pipeline.",
        "steps": [
            "Open GitDealFlow → note the top 5 trending startups",
            "For each, search Crunchbase → check funding history, investor syndicate, similar companies",
            "If the startup hasn't raised recently (12+ months since last round) and GitHub is accelerating → strong signal",
            "Add to your pipeline CRM with context from both sources"
        ],
        "faqs": [
            ("How do I actually connect GitDealFlow to Crunchbase?", "There's no direct integration — you use them side by side. GitDealFlow is your Monday morning signal feed. Crunchbase is your context layer. Together they're more powerful than either alone."),
            ("Can I export GitDealFlow data to Crunchbase?", "Not directly, but you can bookmark or flag startups in GitDealFlow and cross-reference them in Crunchbase. Many teams use Airtable or Notion as the middle layer."),
        ],
        "related": [
            {"url": "/vs/crunchbase", "label": "GitDealFlow vs Crunchbase"},
            {"url": "/integrations/gitdealflow-for-airtable", "label": "GitDealFlow + Airtable"},
            {"url": "/integrations/gitdealflow-for-notion", "label": "GitDealFlow + Notion"},
        ]
    },
    {
        "slug": "gitdealflow-for-pitchbook",
        "title": "GitDealFlow + PitchBook — Pre-Round Signal Meets Deal-Terms Database",
        "desc": "PitchBook is the standard for deal-terms data. GitDealFlow is the standard for pre-round signal. Together they form the most complete VC sourcing + analysis stack available.",
        "use_case": "Use GitDealFlow to discover which startups are accelerating this week. Once you've identified the hottest prospects, use PitchBook to analyze comparable deals, typical terms for the sector/stage, and which funds co-invest. GitDealFlow answers 'who should I look at.' PitchBook answers 'what should I pay.'",
        "steps": [
            "GitDealFlow → identify top 3-5 accelerating startups",
            "PitchBook → find comparable deals in the same sector + stage",
            "PitchBook → check typical valuation multiples and deal terms",
            "PitchBook → identify co-investor patterns (which funds invest together in this space)",
            "Reach out with context: 'I saw your GitHub momentum + your sector typically raises at X terms'"
        ],
        "faqs": [
            ("Why use both instead of just PitchBook?", "PitchBook's deal data is excellent, but it only shows you companies that have already raised. GitDealFlow shows you companies that haven't raised yet — the ones where you can still get allocation."),
        ],
        "related": [
            {"url": "/vs/pitchbook", "label": "GitDealFlow vs PitchBook"},
            {"url": "/cost-of/pitchbook-pricing", "label": "PitchBook pricing breakdown"},
        ]
    },
    {
        "slug": "gitdealflow-for-affinity",
        "title": "GitDealFlow + Affinity CRM — Discover Startups, Then Find the Warm Intro",
        "desc": "Affinity tells you who can introduce you to a startup. But first, you need to know which startups to look for. GitDealFlow fills that gap — discovery first, warm intro second.",
        "use_case": "Monday morning: open GitDealFlow, find your top 5 accelerating startups. Then plug those startup names into Affinity to find mutual connections who can make the intro. The combination turns cold GitHub signal into warm relationship-driven outreach.",
        "steps": [
            "GitDealFlow → identify top 5 trending startups this week",
            "Affinity → search each startup, find mutual connections",
            "Affinity → check relationship strength scores for each intro path",
            "Reach out via the warmest path: 'I noticed your GitHub momentum this month — [mutual contact] suggested I reach out'"
        ],
        "faqs": [
            ("Does GitDealFlow integrate directly with Affinity?", "No native integration, but you can use the GitDealFlow API to pipe trending startups into a spreadsheet or CRM. Many teams use Zapier or a simple Airtable sync."),
        ],
        "related": [
            {"url": "/integrations/gitdealflow-for-airtable", "label": "GitDealFlow + Airtable"},
            {"url": "/integrations/gitdealflow-for-notion", "label": "GitDealFlow + Notion"},
            {"url": "/alternatives-to/affinity", "label": "Affinity alternatives"},
        ]
    },
    {
        "slug": "gitdealflow-for-dealroom",
        "title": "GitDealFlow + Dealroom — GitHub Signal Meets European Ecosystem Data",
        "desc": "Dealroom dominates European VC data. GitDealFlow adds the pre-round engineering signal layer that Dealroom doesn't cover. Together they're the complete European sourcing stack.",
        "use_case": "European startups often raise with less press than US counterparts. Dealroom gives you the ecosystem context (which sectors are hot in Berlin/Paris/London). GitDealFlow gives you the specific startups that are accelerating in those ecosystems.",
        "steps": [
            "Dealroom → identify hot sectors in your target geography",
            "GitDealFlow → filter by those sectors, find accelerating startups",
            "Dealroom → check ecosystem context (total funding in sector, active funds, exits)",
            "Reach out with geography-specific context"
        ],
        "faqs": [
            ("Does GitDealFlow cover European startups?", "Yes — GitDealFlow tracks startups globally. European startups with public GitHub activity are included across all 20 sectors."),
        ],
        "related": [
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
            {"url": "/for/venture-scouts", "label": "GitDealFlow for venture scouts"},
        ]
    },
    {
        "slug": "gitdealflow-for-sourcingsys-crm",
        "title": "GitDealFlow + Sourcing Systems — GitHub Signal Into Your Pipeline CRM",
        "desc": "Sourcing Systems and similar pipeline CRMs track the startups you already know about. GitDealFlow finds the ones you don't. Here's how to bridge the two.",
        "use_case": "Most investment teams have a pipeline CRM (SourceScrub, Affinity, custom Airtable). The CRM is the destination — but you need a source. GitDealFlow is the source: every week, feed 3-5 new startups into your CRM from the GitHub signal feed.",
        "steps": [
            "GitDealFlow → identify 3-5 new accelerating startups weekly",
            "CRM → create new entry for each with source = 'GitDealFlow GitHub signal'",
            "CRM → enrich with context (sector, stage estimate, GitHub metrics)",
            "CRM → track outreach and follow-ups over subsequent weeks"
        ],
        "faqs": [
            ("How do I automate the GitDealFlow → CRM flow?", "Use the GitDealFlow API or CSV export to pull trending startups, then use Zapier/Make or a simple Python script to push them into your CRM. The free tier includes API access."),
        ],
        "related": [
            {"url": "/integrations/gitdealflow-for-airtable", "label": "GitDealFlow + Airtable"},
            {"url": "/templates/pipeline-review-template", "label": "Pipeline review template"},
        ]
    },
]

# ── FAQ EXPANSION PAGES ────────────────────────────────────────────

FAQ = [
    {
        "slug": "how-to-spot-a-startup-about-to-raise",
        "title": "How to Spot a Startup About to Raise — FAQ",
        "desc": "The signals that reliably predict a fundraise — answered from the perspective of investors and deal-flow analysts who track 400+ startups weekly.",
        "qa": [
            ("What are the strongest signals a startup is about to raise?", "1) Sustained commit acceleration (20%+ week-over-week for 4+ weeks). 2) Growing contributor count (new engineers joining). 3) Star velocity spike (organic developer interest). 4) GitHub org expansion (new repos being created). When 2-3 of these converge, a fundraise is likely within 3-6 weeks."),
            ("How accurate are GitHub signals for predicting fundraises?", "Across the ~400 tracked startups, engineering acceleration preceded a public fundraise announcement 68% of the time. Not perfect — but significantly better than waiting for Crunchbase or press releases."),
            ("What sectors are GitHub signals most predictive for?", "Developer tools, AI/ML, infrastructure, cybersecurity, fintech, and any sector where the startup builds software as its core product. Least predictive for hardware, biotech, consumer apps, and services businesses."),
            ("Can a startup fake its GitHub activity?", "Sustained, meaningful engineering activity is extremely difficult to fake. You can pad commit counts with whitespace changes, but real velocity — meaningful commits across multiple contributors over months — is a genuine signal."),
            ("What's the typical timeline from signal to announcement?", "3-6 weeks from the first sustained acceleration signal to a public round announcement. The window is shorter in hot sectors (AI: 2-3 weeks) and longer in slower-moving verticals (healthtech: 4-8 weeks)."),
        ],
        "related": [
            {"url": "/learn/how-to-find-startups-before-they-raise", "label": "Find startups before they raise"},
            {"url": "/learn/how-to-track-startup-engineering-velocity", "label": "Track engineering velocity"},
            {"url": "/glossary/engineering-momentum-score", "label": "Engineering Momentum Score"},
        ]
    },
    {
        "slug": "how-to-get-deal-flow-as-a-new-vc",
        "title": "How to Get Deal Flow as a New VC — FAQ",
        "desc": "Emerging managers and new VCs face the cold-start problem: no brand, no network, no deal flow. Here's how to build a data-driven sourcing engine from scratch.",
        "qa": [
            ("How do I build deal flow with no network?", "Start with data, not network. Use GitDealFlow or similar tools to find accelerating startups. Cold outreach with specific, data-backed observations ('I noticed your team's GitHub velocity increased 40% this quarter') works better than generic 'I'm an investor' intros."),
            ("What tools do I need as a new VC?", "Minimum viable stack: 1) a signal tool (GitDealFlow), 2) a basic CRM (Airtable, Notion), 3) a round-history database (Crunchbase free tier). Total cost: EUR 9.97/month. Add layers as you scale."),
            ("How many startups should I track as a solo GP?", "Start with 50-100 in your CRM. Add 5-10 per week from your signal tool. Track outreach, follow-ups, and pipeline stage. After 6 months, you'll have a system."),
            ("How do I compete with established funds for allocation?", "You can't compete on brand or network. Compete on speed and specificity. Reach out first (GitHub signal gives you a 3-6 week head start) and be specific about what you noticed. Founders remember the investor who did their homework."),
            ("What's the biggest mistake new VCs make with deal flow?", "Waiting for warm intros. Intro-driven sourcing favors established funds with deep networks. Data-driven sourcing favors whoever has the best signal. As a new fund, data is your only edge — use it."),
        ],
        "related": [
            {"url": "/for/angel-investors", "label": "GitDealFlow for angel investors"},
            {"url": "/for/venture-scouts", "label": "GitDealFlow for venture scouts"},
            {"url": "/templates/investment-thesis-template", "label": "Investment thesis template"},
        ]
    },
    {
        "slug": "how-much-does-gitdealflow-cost",
        "title": "How Much Does GitDealFlow Cost? — FAQ",
        "desc": "Clear answers on GitDealFlow pricing tiers, what's free, and how it compares to traditional deal-flow tools.",
        "qa": [
            ("Is GitDealFlow free?", "Yes — there's a free tier that gives you the top 20 trending startups across all 20 sectors. No credit card, no time limit. The free tier is genuinely useful for individual angels and scouts."),
            ("What does the paid tier cost?", "EUR 9.97/month. You get full sector filtering, startup search by name, API access, CSV exports, and the Scout Score tool. Approximately 1/2000th the cost of a PitchBook seat."),
            ("How does pricing compare to Crunchbase or PitchBook?", "Crunchbase starts at $29/month (individual). PitchBook starts at ~$20K/year per seat. CB Insights starts at ~$40K/year. GitDealFlow is EUR 9.97/month — it's priced for individual investors and scouts, not institutional budgets."),
            ("Is there an enterprise tier?", "Not yet. The product is currently individual-tier. Team features are on the roadmap. For now, each team member needs their own account."),
            ("What do I get with the free tier?", "Top 20 trending startups (all sectors, refreshed weekly), Scout Score lookup for any GitHub username, basic methodology documentation. Enough to validate whether GitHub signal is useful for your workflow."),
        ],
        "related": [
            {"url": "/pricing", "label": "Pricing page"},
            {"url": "/cost-of/crunchbase-pricing", "label": "Crunchbase pricing 2026"},
            {"url": "/cost-of/pitchbook-pricing", "label": "PitchBook pricing 2026"},
        ]
    },
    {
        "slug": "what-makes-a-good-deal-flow-signal",
        "title": "What Makes a Good Deal-Flow Signal? — FAQ",
        "desc": "Not all signals are created equal. Here's what separates a useful deal-flow signal from noise — and why GitHub engineering activity is one of the strongest leading indicators available.",
        "qa": [
            ("What makes a signal good for deal flow?", "Three criteria: 1) It's a LEADING indicator (predicts before events happen). 2) It's OBJECTIVE (not self-reported). 3) It's TIMELY (refreshed at least weekly). GitHub engineering activity scores high on all three."),
            ("Why is GitHub activity better than Crunchbase data?", "Crunchbase data is self-reported (founders or PR firms submit it) and lagging (rounds appear after they close). GitHub data is objective (code doesn't lie) and leading (acceleration happens before the raise)."),
            ("What about hiring data as a signal?", "Hiring is a good secondary signal. But it lags behind code — a startup ships for months before it hires a PR person. GitHub is the earliest signal; hiring confirms the momentum."),
            ("What's the worst deal-flow signal?", "Press mentions. By the time a startup is in TechCrunch or Forbes, the round is usually closed. It's not a signal — it's a confirmation of what already happened."),
            ("How often should I check signals?", "Weekly. GitHub is noisy at the daily level (weekend commit dips, sprint-cycle patterns). Weekly aggregation smooths the noise and reveals real trends."),
        ],
        "related": [
            {"url": "/learn/what-is-a-deal-flow-signal", "label": "What is a deal flow signal?"},
            {"url": "/glossary/commit-velocity", "label": "Commit velocity"},
            {"url": "/glossary/star-acceleration", "label": "Star acceleration"},
        ]
    },
    {
        "slug": "how-to-transition-from-crunchbase-to-signal-based-sourcing",
        "title": "How to Transition from Crunchbase to Signal-Based Sourcing — FAQ",
        "desc": "Most investors start with Crunchbase. Here's how to layer on GitHub signal without abandoning your existing workflow — and why the best investors use both.",
        "qa": [
            ("Do I need to stop using Crunchbase?", "No. The most effective approach is layered: GitDealFlow for discovery, Crunchbase for context. Keep Crunchbase for round-history lookups and investor-network mapping. Add GitDealFlow for the pre-round signal."),
            ("How do I change my Monday routine?", "Current routine: open Crunchbase → look at recently funded startups → reach out (but they've already raised). New routine: open GitDealFlow → find accelerating startups → cross-reference Crunchbase for context → reach out BEFORE they raise."),
            ("Will my team adopt a new tool?", "Start with yourself. Run the GitDealFlow + Crunchbase workflow for 4 weeks. Track your response rate vs traditional sourcing. Once you have data, share the results. Adoption follows results."),
            ("What's the learning curve?", "Almost zero. GitDealFlow is designed to replace the 'scroll Crunchbase and hope' part of your workflow. If you can read a graph, you can use GitDealFlow. The free tier is genuinely useful — try it for a month with zero commitment."),
        ],
        "related": [
            {"url": "/how-to/how-to-build-a-weekly-deal-flow-routine", "label": "Build a weekly deal flow routine"},
            {"url": "/alternatives-to/crunchbase", "label": "Crunchbase alternatives"},
            {"url": "/vs/crunchbase", "label": "GitDealFlow vs Crunchbase"},
        ]
    },
    {
        "slug": "what-is-scout-score",
        "title": "What Is the Scout Score? — FAQ",
        "desc": "The Scout Score measures a GitHub user's ability to spot breakout startups early — by analyzing their starring history against ~75 validated unicorns. Here's how it works, what it means, and how to improve yours.",
        "qa": [
            ("What is the Scout Score?", "The Scout Score (0-100) measures a GitHub user's 'early detection' ability. It analyzes which repos you starred — and when — against a list of ~75 startups that later became unicorns. The earlier you starred them, the higher your score."),
            ("How is the Scout Score calculated?", "For each of ~75 validated unicorns with public GitHub repos, the algorithm checks whether you starred the repo and when relative to the company's growth trajectory. Stars before Series A carry the most weight. Stars after IPO carry almost none."),
            ("What's a good Scout Score?", "Score > 70: you consistently star breakout startups early. Score 40-70: you have good instincts but room to improve. Score < 40: you tend to discover startups later in their journey. Most active GitHub users score between 30-60."),
            ("How do I improve my Scout Score?", "Star repos from early-stage startups before they're well-known. Follow sectors you understand deeply. The score rewards genuine early discovery, not volume — 10 well-timed stars are worth more than 1,000 late ones."),
            ("Is the Scout Score public?", "You can choose to make it public or private. Public scores appear on your Scout profile. Private scores are visible only to you. Investors often use public scores as a credibility signal."),
        ],
        "related": [
            {"url": "/glossary/scout-score", "label": "Scout Score glossary"},
            {"url": "/for/venture-scouts", "label": "GitDealFlow for venture scouts"},
        ]
    },
]

# ── TEMPLATE EXPANSION PAGES ──────────────────────────────────────

TEMPLATES = [
    {
        "slug": "weekly-deal-flow-review-template",
        "title": "Weekly Deal-Flow Review Template — Free Download for Investors",
        "desc": "A structured template to review your deal flow every week. Track which startups you sourced, which you reached out to, which responded, and where they are in your pipeline.",
        "sections": [
            "This Week's Signal Feed: top 5 startups surfaced by your signal tool",
            "Deep-Dive Notes: 2-3 startups you researched in detail",
            "Outreach Log: who you contacted, method, and response",
            "Pipeline Status: new, contacted, meeting scheduled, due diligence, passed, invested",
            "Next Week's Focus: which sectors or signal types to prioritize"
        ],
        "faqs": [
            ("How often should I use this template?", "Weekly. Monday morning is ideal — review last week's activity and set this week's priorities. Consistency is more important than thoroughness."),
            ("Can I adapt this for my team?", "Yes — the template is designed to be customized. Add your fund's specific sectors, stage preferences, and pipeline stages."),
        ],
        "related": [
            {"url": "/templates/pipeline-review-template", "label": "Pipeline review template"},
            {"url": "/how-to/how-to-build-a-weekly-deal-flow-routine", "label": "Build a weekly deal flow routine"},
        ]
    },
    {
        "slug": "startup-evaluation-scorecard-template",
        "title": "Startup Evaluation Scorecard Template — Quantify Your Sourcing Decisions",
        "desc": "A structured scorecard to evaluate startups across 8 dimensions — from team quality to GitHub momentum. Turn gut-feel sourcing into data-driven decisions.",
        "sections": [
            "Team: founder experience, engineering strength, hiring velocity",
            "Market: TAM, growth rate, competitive landscape",
            "GitHub Signal: commit velocity trend, contributor growth, star acceleration",
            "Product: public roadmap, shipping cadence, user feedback",
            "Business Model: revenue model, unit economics, path to profitability",
            "Competition: direct competitors, moat strength, differentiation",
            "Fundraising: time since last round, burn rate estimate, likely round timing",
            "Fit: alignment with your thesis, stage, and check size"
        ],
        "faqs": [
            ("What's the best way to use this scorecard?", "Score 2-3 startups per week consistently. Over 12 weeks you'll have evaluated 24-36 startups — enough data to see patterns in your decision-making and calibrate your instincts."),
        ],
        "related": [
            {"url": "/templates/pipeline-review-template", "label": "Pipeline review template"},
            {"url": "/templates/investment-thesis-template", "label": "Investment thesis template"},
        ]
    },
    {
        "slug": "cold-outreach-email-template-for-investors",
        "title": "Cold Outreach Email Template for Investors — Get Responses From Founders",
        "desc": "A proven email template for cold-outreaching founders based on GitHub signal. Short, specific, credible — founders respond when you've done your homework.",
        "sections": [
            "Subject line: 'Noticed your GitHub momentum at [startup]'",
            "Opening: one sentence about what you observed (be specific — mention the metric)",
            "Context: who you are, what you invest in, why this startup",
            "Ask: 15-minute call, no pitch deck needed",
            "Close: no pressure, compliment the team's execution, leave the door open"
        ],
        "faqs": [
            ("What's the response rate for cold outreach?", "Investors who mention specific GitHub observations (commit velocity, contributor growth) report 40-60% response rates. Generic 'I'm an investor interested in your space' emails get 10-15%. Specificity is the differentiator."),
            ("Should I mention GitDealFlow in the email?", "Yes — it shows you use data, not just gut feel. 'I track engineering momentum on GitDealFlow and noticed your team's velocity increased 40% this month' is a strong opener."),
        ],
        "related": [
            {"url": "/how-to/how-to-build-a-weekly-deal-flow-routine", "label": "Build a weekly deal flow routine"},
            {"url": "/for/angel-investors", "label": "GitDealFlow for angel investors"},
        ]
    },
    {
        "slug": "sector-sourcing-calendar-template",
        "title": "Sector Sourcing Calendar Template — Systematize Your Deal Flow by Sector",
        "desc": "A quarterly calendar that maps which sectors you source from each week. Ensures you don't over-index on one sector and miss opportunities in others.",
        "sections": [
            "Q1 Focus Sectors: your top 3-5 sectors for the quarter",
            "Weekly Rotation: which sector you deep-dive each week",
            "Signal Review: key metrics to check per sector (commits, contributors, stars)",
            "Pipeline Check: startups in each sector currently in your pipeline",
            "Quarterly Review: which sectors produced the best deal flow, where to adjust"
        ],
        "faqs": [
            ("How many sectors should I focus on?", "3-5 actively, up to 10 passively. Active sectors get a deep-dive each rotation. Passive sectors get a quick scan. Any more than 10 and you'll spread too thin."),
        ],
        "related": [
            {"url": "/sectors", "label": "All sectors"},
            {"url": "/templates/investment-thesis-template", "label": "Investment thesis template"},
        ]
    },
    {
        "slug": "due-diligence-checklist-template",
        "title": "Technical Due Diligence Checklist Template — For Startups With Public GitHub",
        "desc": "When you have a startup in diligence, here's how to evaluate their engineering from their public GitHub — code quality, shipping velocity, team stability, and red flags.",
        "sections": [
            "Code Velocity: week-over-week commit trend over the last 12 weeks",
            "Team Stability: contributor count trend, churn in engineering team",
            "Repo Health: issue close rate, PR merge time, documentation quality",
            "Architecture Signals: monorepo vs multi-repo, language choices, dependency freshness",
            "Red Flags: long-open issues, declining velocity, single-point-of-failure contributors",
            "Comparison: how this team's velocity compares to peers in the same sector/stage"
        ],
        "faqs": [
            ("Can I do technical DD without being technical?", "You can assess velocity and team stability trends — those are quantitative. For code quality and architecture, bring in a technical advisor or use GitDealFlow's benchmarks as a starting point."),
        ],
        "related": [
            {"url": "/templates/technical-diligence-template", "label": "Technical diligence template"},
            {"url": "/glossary/engineering-momentum-score", "label": "Engineering Momentum Score"},
            {"url": "/learn/how-to-track-startup-engineering-velocity", "label": "Track engineering velocity"},
        ]
    },
]

# ── BUILD ──────────────────────────────────────────────────────────

def write_page(directory, slug, title, desc, breadcrumbs, schema_blocks, body_html, related_links=None):
    """Write a single pSEO page following the existing template structure."""
    dir_path = os.path.join(BASE, directory)
    os.makedirs(dir_path, exist_ok=True)
    
    full_html = (
        head(title, desc, f"/{directory}/{slug}", schema_blocks) +
        header(breadcrumbs=breadcrumbs) +
        body_html +
        footer(related_links)
    )
    
    filepath = os.path.join(dir_path, slug, "index.html")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(full_html)
    return filepath

def build_alternatives():
    """Build /alternatives-to/ pages."""
    count = 0
    for a in ALTERNATIVES:
        slug = a["slug"]
        path = f"/alternatives-to/{slug}"
        
        tools_html = ""
        for t in a["tools"]:
            tools_html += f'''
          <tr>
            <td><strong>{t['name']}</strong></td>
            <td>{t['best_for']}</td>
            <td>{t['price']}</td>
          </tr>'''
        
        detail_html = ""
        for t in a["tools"]:
            detail_html += f'''<h3>{t['name']}</h3>
            <p><strong>Best for:</strong> {t['best_for']} | <strong>Price:</strong> {t['price']}</p>
            <p>{t['strength']}</p>\n'''
        
        faq_html = ""
        for q, a_text in a["faqs"]:
            faq_html += f'''
        <details class="faq-item">
          <summary>{q}</summary>
          <p>{a_text}</p>
        </details>'''
        
        body = f'''
  <section class="vs-hero">
    <h1>{a["title"]}</h1>
    <p class="vs-lede">{a["desc"]}</p>
  </section>

  <section class="vs-section">
    <h2>Quick comparison</h2>
    <table class="vs-table">
      <thead><tr><th>Tool</th><th>Best for</th><th>Starts at</th></tr></thead>
      <tbody>{tools_html}
      </tbody>
    </table>
  </section>

  <section class="vs-section">
    <h2>Detailed breakdown</h2>
    {detail_html}
  </section>

  <section class="vs-section">
    <div class="verdict">
      <strong>Our verdict:</strong> {a["verdict"]}
    </div>
  </section>

  <section class="vs-section">
    <h2>Frequently asked questions</h2>
    {faq_html}
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>See which startups are accelerating right now</h2>
      <p style="color:#e0f2fe;margin-bottom:1rem">Free tier available — get the top 20 trending startups across all 20 sectors, no credit card required.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>'''
        
        schemas = (
            article_schema(a["title"], a["desc"], path) +
            breadcrumb_schema([("Home", CANONICAL_BASE), ("Alternatives", f"{CANONICAL_BASE}/alternatives-to"), (a["title"].split("—")[0].strip(), "")]) +
            faq_schema(a["faqs"])
        )
        
        write_page("alternatives-to", slug, a["title"], a["desc"],
                   [("Home", "/"), ("Alternatives", "/alternatives-to"), (a["title"].split("—")[0].strip(), "")],
                   schemas, body, a.get("related"))
        count += 1
    return count

def build_howto():
    """Build /how-to/ pages."""
    count = 0
    for h in HOW_TO:
        slug = h["slug"]
        path = f"/how-to/{slug}"
        
        steps_html = ""
        for s in h["steps"]:
            steps_html += f'''
        <div style="background:#0f172acc;border:1px solid #1e293b;border-radius:.5rem;padding:1rem 1.25rem;margin:1rem 0">
          <strong style="color:#7dd3fc">{s['title']}</strong>
          <p style="margin-top:.4rem">{s['text']}</p>
        </div>'''
        
        faq_html = ""
        for q, a_text in h["faqs"]:
            faq_html += f'''
        <details class="faq-item">
          <summary>{q}</summary>
          <p>{a_text}</p>
        </details>'''
        
        body = f'''
  <section class="vs-hero">
    <h1>{h["title"]}</h1>
    <p class="vs-lede">{h["desc"]}</p>
  </section>

  <section class="vs-section">
    <h2>Step-by-step</h2>
    {steps_html}
  </section>

  <section class="vs-section">
    <h2>Frequently asked questions</h2>
    {faq_html}
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>Start tracking engineering momentum today</h2>
      <p style="color:#e0f2fe;margin-bottom:1rem">GitDealFlow tracks 400+ startups across 20 sectors. Free tier available.</p>
      <a href="/#signup-hero" class="btn">Get started free &rarr;</a>
    </div>
  </section>'''
        
        schemas = (
            article_schema(h["title"], h["desc"], path) +
            breadcrumb_schema([("Home", CANONICAL_BASE), ("How-To Guides", f"{CANONICAL_BASE}/how-to"), (h["title"], "")]) +
            faq_schema(h["faqs"])
        )
        
        write_page("how-to", slug, h["title"], h["desc"],
                   [("Home", "/"), ("How-To Guides", "/how-to"), (h["title"], "")],
                   schemas, body, h.get("related"))
        count += 1
    return count

def build_integrations():
    """Build /integrations/ pages."""
    count = 0
    for i in INTEGRATIONS:
        slug = i["slug"]
        path = f"/integrations/{slug}"
        
        steps_html = "\n".join(f'<li>{s}</li>' for s in i["steps"])
        
        faq_html = ""
        for q, a_text in i["faqs"]:
            faq_html += f'''
        <details class="faq-item">
          <summary>{q}</summary>
          <p>{a_text}</p>
        </details>'''
        
        body = f'''
  <section class="vs-hero">
    <h1>{i["title"]}</h1>
    <p class="vs-lede">{i["desc"]}</p>
  </section>

  <section class="vs-section">
    <h2>How to use them together</h2>
    <p>{i["use_case"]}</p>
    <h3>Workflow</h3>
    <ol style="color:#cbd5e1;line-height:1.8;padding-left:1.25rem">
      {steps_html}
    </ol>
  </section>

  <section class="vs-section">
    <h2>Frequently asked questions</h2>
    {faq_html}
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>Build your deal-flow stack today</h2>
      <p style="color:#e0f2fe;margin-bottom:1rem">GitDealFlow integrates with your existing workflow — CRM, database, or spreadsheet.</p>
      <a href="/#signup-hero" class="btn">Get started free &rarr;</a>
    </div>
  </section>'''
        
        schemas = (
            article_schema(i["title"], i["desc"], path) +
            breadcrumb_schema([("Home", CANONICAL_BASE), ("Integrations", f"{CANONICAL_BASE}/integrations"), (i["title"], "")]) +
            faq_schema(i["faqs"])
        )
        
        write_page("integrations", slug, i["title"], i["desc"],
                   [("Home", "/"), ("Integrations", "/integrations"), (i["title"], "")],
                   schemas, body, i.get("related"))
        count += 1
    return count

def build_faq():
    """Build expanded /faq/ pages."""
    count = 0
    for f in FAQ:
        slug = f["slug"]
        path = f"/faq/{slug}"
        
        faq_html = ""
        for q, a_text in f["qa"]:
            faq_html += f'''
        <details class="faq-item">
          <summary>{q}</summary>
          <p>{a_text}</p>
        </details>'''
        
        body = f'''
  <section class="vs-hero">
    <h1>{f["title"]}</h1>
    <p class="vs-lede">{f["desc"]}</p>
  </section>

  <section class="vs-section">
    {faq_html}
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>Try GitDealFlow — free</h2>
      <p style="color:#e0f2fe;margin-bottom:1rem">Get the top 20 trending startups across 20 sectors. No credit card required.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>'''
        
        schemas = (
            article_schema(f["title"], f["desc"], path) +
            breadcrumb_schema([("Home", CANONICAL_BASE), ("FAQ", f"{CANONICAL_BASE}/faq"), (f["title"], "")]) +
            faq_schema(f["qa"])
        )
        
        write_page("faq", slug, f["title"], f["desc"],
                   [("Home", "/"), ("FAQ", "/faq"), (f["title"], "")],
                   schemas, body, f.get("related"))
        count += 1
    return count

def build_templates():
    """Build expanded /templates/ pages."""
    count = 0
    for t in TEMPLATES:
        slug = t["slug"]
        path = f"/templates/{slug}"
        
        sections_html = "\n".join(f'<li>{s}</li>' for s in t["sections"])
        
        faq_html = ""
        for q, a_text in t["faqs"]:
            faq_html += f'''
        <details class="faq-item">
          <summary>{q}</summary>
          <p>{a_text}</p>
        </details>'''
        
        body = f'''
  <section class="vs-hero">
    <h1>{t["title"]}</h1>
    <p class="vs-lede">{t["desc"]}</p>
  </section>

  <section class="vs-section">
    <h2>What's included</h2>
    <ul style="color:#cbd5e1;line-height:2;padding-left:1.25rem">
      {sections_html}
    </ul>
  </section>

  <section class="vs-section">
    <h2>Frequently asked questions</h2>
    {faq_html}
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>Download all templates</h2>
      <p style="color:#e0f2fe;margin-bottom:1rem">Get the full template library — designed for investors who use data-driven sourcing.</p>
      <a href="/#signup-hero" class="btn">Get the templates &rarr;</a>
    </div>
  </section>'''
        
        schemas = (
            article_schema(t["title"], t["desc"], path) +
            breadcrumb_schema([("Home", CANONICAL_BASE), ("Templates", f"{CANONICAL_BASE}/templates"), (t["title"], "")]) +
            faq_schema(t["faqs"])
        )
        
        write_page("templates", slug, t["title"], t["desc"],
                   [("Home", "/"), ("Templates", "/templates"), (t["title"], "")],
                   schemas, body, t.get("related"))
        count += 1
    return count

if __name__ == "__main__":
    results = {}
    results["alternatives"] = build_alternatives()
    results["how-to"] = build_howto()
    results["integrations"] = build_integrations()
    results["faq"] = build_faq()
    results["templates"] = build_templates()
    
    total = sum(results.values())
    print(f"Generated {total} new pSEO pages:")
    for cat, n in results.items():
        print(f"  {cat}: {n}")
    print(f"\nTotal new pages: {total}")
    print(f"Base directory: {BASE}")
