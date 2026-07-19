"""Final batch: 8 glossary + 5 hub pages + accuracy fix."""
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
      <p class="text-gray-300 mb-2 font-semibold">GitDealFlow is a deal-flow signal tool for investors — not a fund and not a startup accelerator.</p>
      <div class="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mt-5">
        <a href="/" class="py-2 inline-block hover:text-gray-300">Home</a><a href="/best/best-startup-signal-tools" class="py-2 inline-block hover:text-gray-300">Best tools</a><a href="/vs" class="py-2 inline-block hover:text-gray-300">Comparisons</a><a href="/glossary/scout-score" class="py-2 inline-block hover:text-gray-300">Glossary</a><a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 GitDealFlow</p>
    </div>
  </footer>"""

HEAD = """  <meta name="theme-color" content="#0f172a" /><meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/styles.css" as="style"><link rel="stylesheet" href="/styles.css">
  <style>
    .h-hero{padding:2.5rem 1.25rem 1.5rem;max-width:780px;margin:0 auto}
    .h-hero h1{font-size:clamp(1.85rem,4vw,2.5rem);line-height:1.15;font-weight:800;letter-spacing:-.02em;color:#fff;margin:.4em 0 .6em}
    .h-lede{font-size:1.12rem;color:#cbd5e1;line-height:1.6;margin-bottom:1.25rem}
    .h-section{max-width:780px;margin:0 auto;padding:1.25rem}
    .h-section h2{font-size:1.4rem;margin:1.5rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700}
    .h-section p,.h-section li{color:#cbd5e1;line-height:1.7}.h-section ul{padding-left:1.25rem;margin:.5rem 0}
    .def-box{background:#0f172a99;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:0 .5rem .5rem 0;margin:1rem 0}
    .def-box .term{color:#7dd3fc;font-weight:700;font-size:1.1rem}
    .callout{background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:.6rem;margin:1.25rem 0}
    .callout strong{color:#7dd3fc}
    .faq-item{border-bottom:1px solid #1e293b;padding:.85rem 0}
    .faq-item summary{cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none;font-size:1.02rem}
    .faq-item summary::-webkit-details-marker{display:none}
    .faq-item summary::before{content:"\\25b8 ";color:#0ea5e9;margin-right:.4rem}
    .faq-item[open] summary::before{content:"\\25be "}
    .faq-item p{margin:.55rem 0 0;color:#cbd5e1;line-height:1.6}
    .cta-final{background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2rem 1.5rem;border-radius:.8rem;margin-top:2rem;text-align:center}
    .cta-final .btn{display:inline-block;background:#fff;color:#0369a1;padding:.8rem 1.7rem;border-radius:.4rem;font-weight:700;margin-top:.7rem}
    .hub-list{list-style:none;padding:0;margin:0;display:grid;gap:.45rem}
    .hub-list a{display:block;background:#0f172acc;border:1px solid #1e293b;border-radius:.55rem;padding:.9rem 1.1rem;color:#7dd3fc;text-decoration:none;transition:border-color .15s}
    .hub-list a:hover{border-color:#334155}.hub-list a strong{color:#e2e8f0}
    .hub-list a span{display:block;color:#64748b;font-size:.85rem;margin-top:.15rem}
  </style>"""


def wrap(canonical, title, desc, h1, lede, body, schemas=None, bc=None):
    og = f"{SIGNALS}/opengraph-image"
    s = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": h1, "description": desc,
        "author": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "publisher": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "datePublished": TODAY, "dateModified": TODAY,
    }) + '</script>\n  '
    if schemas:
        for sch in schemas:
            s += '<script type="application/ld+json">' + json.dumps(sch) + '</script>\n  '
    if bc:
        items = [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i,(n,u) in enumerate(bc)]
        s += '<script type="application/ld+json">' + json.dumps(
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}) + '</script>\n  '
    nav_html = ""
    if bc:
        parts = []
        for i,(n,u) in enumerate(bc):
            parts.append('<a href="'+u+'" class="hover:text-gray-300">'+html.escape(n)+'</a>' if i<len(bc)-1 else '<span class="text-gray-300">'+html.escape(n)+'</span>')
        nav_html = '\n  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">' + ' <span class="mx-1">/</span> '.join(parts) + '</nav>'
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n  <title>'+html.escape(title)+'</title>\n  <meta name="description" content="'+html.escape(desc)+'">\n  <link rel="canonical" href="'+canonical+'" />\n  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />\n  <meta property="og:title" content="'+html.escape(title)+'" />\n  <meta property="og:description" content="'+html.escape(desc)+'" />\n  <meta property="og:url" content="'+canonical+'" />\n  <meta property="og:image" content="'+og+'" />\n  <meta name="twitter:card" content="summary_large_image" />\n  <meta name="twitter:site" content="@data_nerd" />\n  '+s+'\n'+HEAD+'\n</head>\n<body class="bg-dark-900 text-gray-100">\n'+NAV+'\n'+nav_html+'\n  <section class="h-hero">\n    <h1>'+h1+'</h1>\n    <p class="h-lede">'+lede+'</p>\n  </section>\n'+body+'\n'+FOOTER+'\n</body>\n</html>\n'


def faqs(fqs):
    items = ""
    for q, a in fqs:
        items += '          <details class="faq-item"><summary>'+html.escape(q)+'</summary><p>'+a+'</p></details>\n'
    return items

def faq_schema(fqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
        for q, a in fqs]}


# ============ GLOSSARY PAGES ============
GLOSS = {
    "commit-velocity": {
        "title": "Commit Velocity — GitDealFlow GitHub Signal Metric",
        "h1": "Commit velocity",
        "lede": "The rate of code commits in a repository over time — one of the three signals GitDealFlow reads to detect engineering acceleration and flag startups before the round.",
        "term": "Commit Velocity",
        "tagline": "The rate of code commits over time — one of three signals GitDealFlow uses to detect engineering acceleration.",
        "def": "Commit velocity measures how often a startup's engineering team pushes code to their public GitHub repositories over a rolling window. A rising commit velocity means the team is shipping faster — usually a sign of hiring focus, product-market pull, or an approaching fundraise.",
        "why": "Commit velocity alone isn't predictive — one burned-out founder can commit heavily. But combined with contributor growth and repo expansion, it forms part of the composite Engineering Momentum Score that has historically preceded fundraises by 21\u201347 days. GitDealFlow normalizes commit velocity per org and per team size to produce a comparable signal.",
        "why2": "The engineering-acceleration signal it powers has historically preceded fundraise announcements by 21\u201347 days. The full methodology is published as an SSRN preprint (abstract 6606558).",
        "context": "GitDealFlow tracks commit velocity across 4,200+ startup GitHub orgs in 20 sectors and normalizes it per org to make it comparable. It is the first signal in the composite Engineering Momentum Score, alongside contributor growth and repository expansion.",
        "faqs": [
            ("Is commit velocity enough on its own?", "No. A startup can have high commits from one founder. The composite (commits + contributor growth + repo expansion) is far more reliable."),
            ("How does GitDealFlow normalize commit velocity?", "Per team size and per org. The normalization method is published in the methodology at signals.gitdealflow.com/methodology. This makes a 5-person team's velocity comparable to a 50-person team's."),
            ("Where does the data come from?", "Public GitHub activity only. GitDealFlow does not access private repositories."),
        ],
    },
    "star-acceleration": {
        "title": "Star Acceleration — GitDealFlow GitHub Community Signal",
        "h1": "Star acceleration",
        "lede": "The second derivative of GitHub stars — how fast community interest is growing, used as a confirmation layer in GitDealFlow\u2019s Scout Score and acceleration detection.",
        "term": "Star Acceleration",
        "tagline": "The rate of change of GitHub star growth — a community-interest signal used in Scout Score and acceleration detection.",
        "def": "Star acceleration is the second derivative of a repository's GitHub star count: not how many stars the project has, but how fast the rate of starring is growing. A project going from 10 to 50 stars/week is accelerating; one going from 100 to 105 is linear or plateauing. Acceleration catches breakout interest before absolute numbers do.",
        "why": "Star acceleration is a community confirmation signal. A startup with rising commit velocity AND rising star acceleration is both building and attracting attention — a stronger pattern than either alone. GitDealFlow uses star acceleration as one input layer in Scout Score (the 0\u2013100 taste metric) and as a secondary signal in acceleration detection.",
        "why2": "In Scout Score specifically, the metric correlates with a user's ability to spot breakout repositories before the wider market. A user who consistently stars repos during their acceleration phase (not after they're popular) scores higher.",
        "context": "Pure star counts are a vanity metric — a repo with 10,000 stars that hasn't been updated in a year is parked. Star acceleration only cares about the active growth curve, which is what matters for investment signal.",
        "faqs": [
            ("How is star acceleration different from star count?", "Star count is the total. Star acceleration is how fast that total is growing. GitDealFlow uses acceleration, not the absolute number, because acceleration catches breakout before it's obvious."),
            ("Where is star acceleration used?", "Two places: as a secondary signal in acceleration detection (alongside commit velocity, contributor growth, and repo expansion), and as a primary input in Scout Score (at signals.gitdealflow.com/receipts)."),
        ],
    },
    "contributor-diversity": {
        "title": "Contributor Diversity — GitDealFlow GitHub Team Signal",
        "h1": "Contributor diversity",
        "lede": "The number and distribution of active contributors across a startup\u2019s GitHub organization — one of the three signals GitDealFlow reads to detect team growth before fundraise announcements.",
        "term": "Contributor Diversity",
        "tagline": "The number and distribution of active contributors — the team-growth signal in GitDealFlow\u2019s composite.",
        "def": "Contributor diversity measures how many distinct people are actively contributing to a startup's GitHub org, not just how many commits there are. A growing, diverse contributor base means the startup is hiring, onboarding, and scaling — one of the strongest leading indicators of a fundraise.",
        "why": "Adding senior contributors is one of the most reliable pre-raise signals GitDealFlow has observed. Teams hire and scale engineering before they raise money to fund that scaling. Contributor diversity catches the hiring pattern that precedes the raise.",
        "why2": "Across 219 validated fundraises, rising contributor diversity in the 14-day window before the announcement was present in a majority of cases. It's the team signal that commit velocity alone misses — a startup can have high commits from one person burning out, but diverse, growing contributors means real team momentum.",
        "context": "GitDealFlow weighs contributor diversity alongside commit velocity and repository expansion in the composite Engineering Momentum Score. The three together answer: are they shipping (velocity), are they growing (diversity), and are they expanding (repos).",
        "faqs": [
            ("How is contributor diversity different from commit velocity?", "Commit velocity measures output; contributor diversity measures team growth. A startup with high commits but static contributors may be burning out. One with growing contributors AND rising commits is scaling."),
            ("Does GitDealFlow identify individual contributors?", "No. GitDealFlow counts distinct contributors but does not identify or profile them. The signal is aggregate, not individual."),
        ],
    },
    "github-org-activity": {
        "title": "GitHub Org Activity — GitDealFlow Aggregate Signal Source",
        "h1": "GitHub org activity",
        "lede": "The aggregate commit, pull request, and issue activity across all repositories in a startup\u2019s GitHub organization — the raw data source for GitDealFlow\u2019s engineering-acceleration signal.",
        "term": "GitHub Org Activity",
        "tagline": "Aggregate activity across all repos in a startup\u2019s GitHub organization — the raw input for GitDealFlow\u2019s signal.",
        "def": "GitHub org activity is the sum of all public activity across a startup's GitHub organization: commits, pull requests, issues, and code reviews across every repository in the org. GitDealFlow reads this aggregate for each of 4,200+ tracked startup orgs weekly to detect acceleration patterns.",
        "why": "Looking at individual repos misses the picture. A startup that's adding a new product line opens a new repo — that doesn't show in the main repo's velocity, but it appears in org-level activity. GitDealFlow's composite signal (Engineering Momentum Score) reads org-level activity to catch both internal acceleration and expansion.",
        "why2": "Org-level tracking also normalizes for startups that use monorepos (one big repo, all activity there) vs multi-repo architectures (activity spread across many repos). Both patterns should produce a comparable signal.",
        "context": "GitDealFlow tracks org activity weekly, normalizes it per team size and architecture, and feeds it into the Engineering Momentum Score alongside contributor growth and repository expansion.",
        "faqs": [
            ("Does GitDealFlow access private repos?", "No. All data comes from public GitHub activity only. Startups with exclusively private repositories do not surface in the signal."),
            ("Can a startup falsify its GitHub activity?", "Bots and automated commits are filtered from the signal. The methodology includes bot-detection and normalization to reduce manipulation risk. Gaming the signal is possible but materially harder than self-reporting a fake traction number."),
        ],
    },
    "deal-flow": {
        "title": "Deal Flow — Definition & How GitDealFlow Improves It",
        "h1": "Deal flow",
        "lede": "Deal flow is the pipeline of investment opportunities a fund or investor sees over time. GitDealFlow adds a new category of deal flow: pre-round engineering signal that surfaces startups before the conventional pipeline.",
        "term": "Deal Flow",
        "tagline": "The pipeline of investment opportunities — and how GitDealFlow adds a pre-round signal layer.",
        "def": "Deal flow is the total pipeline of investment opportunities an investor sees: the startups that cross their desk, the pitch decks in their inbox, the warm introductions, and the systematic signals they track. Quality deal flow means seeing the right deals early enough to act; poor deal flow means hearing about good deals after the round closes or not at all.",
        "why": "Most deal flow comes from three sources: network (warm intros, accelerators), inbound (cold pitch, founder outreach), and databases (Crunchbase, PitchBook \u2014 post-round). GitDealFlow adds a fourth category: <strong>pre-round engineering signal</strong> \u2014 startups accelerating on GitHub 21\u201347 days before the round, before they appear in any database or press cycle.",
        "why2": "This fourth category is valuable because it surfaces deal flow that hasn't yet hit the network or database layer. A startup accelerating on GitHub may not have started pitching investors yet, which means less competition and more room to build a relationship before the round formalizes.",
        "context": "GitDealFlow reads public GitHub engineering activity across 4,200+ startup orgs and sends five accelerating startups every Sunday (free) with sector, stage, and a plain-English note. The Dashboard (\u20ac9.97/month) and Insider Circle (\u20ac97/month) add filters, watchlists, and API access for systematic deal flow.",
        "faqs": [
            ("How is GitDealFlow\u2019s deal flow different from Crunchbase\u2019s?", "Crunchbase records rounds after they close. GitDealFlow surfaces startups before the round. Most investors combine the two: GitDealFlow for discovery, Crunchbase for confirmation."),
            ("Is GitDealFlow\u2019s deal flow only for software startups?", "It works best for startups with public GitHub activity, which skews toward developer tools, AI/ML, fintech infrastructure, cybersecurity, and similar code-heavy sectors. It\u2019s weaker for hardware or non-tech businesses without public repos."),
            ("How much deal flow does the free tier provide?", "Five startups every Sunday in the free Signal Digest, plus unlimited browsing on the live signal board at signals.gitdealflow.com. The Dashboard tier adds 60+ ranked startups with filters."),
        ],
    },
    "deal-velocity": {
        "title": "Deal Velocity — Definition for VC & PE Investors",
        "h1": "Deal velocity",
        "lede": "Deal velocity is the speed at which a deal progresses from first contact to close, measured in days or weeks. GitDealFlow\u2019s pre-round signal improves deal velocity by helping investors find startups earlier.",
        "term": "Deal Velocity",
        "tagline": "The speed of deal progression from first contact to close — and why early signal matters.",
        "def": "Deal velocity measures how fast an investment opportunity moves through the pipeline: first contact \u2192 initial meeting \u2192 partner meeting \u2192 term sheet \u2192 close. Faster deal velocity means less time competing, better allocation terms, and more time for diligence. The single biggest factor in deal velocity is <strong>when you found the deal</strong> \u2014 the earlier you spot a startup, the more leverage you have on timing.",
        "why": "GitDealFlow improves deal velocity by shifting \u201cwhen you found the deal\u201d to 21\u201347 days before the conventional pipeline. If most investors see a startup on Crunchbase the week the round is announced, and you saw it three weeks earlier on GitDealFlow, you have a three-week head start on relationship-building, diligence, and term-sheet negotiation.",
        "why2": "That time advantage translates directly into better terms: you\u2019re not competing with funds who saw the same deal on the same database on the same day. You\u2019re in the room before the room exists.",
        "context": "Systematic early deal flow is the biggest lever on deal velocity. GitDealFlow provides it as a pre-round engineering signal, supported by 4,200+ tracked startup orgs, SSRN methodology 6606558, and 219 validated fundraises.",
        "faqs": [
            ("How does early signal improve deal velocity?", "The earlier you find a startup, the more time you have for relationship-building and diligence, and the less competition you face. A 3-week head start on the conventional pipeline can mean the difference between a competitive allocation and a proprietary deal."),
            ("How fast does the weekly digest arrive?", "Every Sunday. Five accelerating startups with sector, stage, and a plain-English note. Free, no card."),
        ],
    },
    "due-diligence": {
        "title": "Due Diligence — Definition & Engineering Signal Layer",
        "h1": "Due diligence",
        "lede": "Due diligence is the investigation process before an investment. GitDealFlow\u2019s engineering-acceleration signal adds a quantitative layer that augments (not replaces) traditional DD.",
        "term": "Due Diligence",
        "tagline": "The investigation process before investing — and how GitDealFlow adds a quantitative signal layer.",
        "def": "Due diligence is the investigation an investor conducts before committing capital: verifying the team, market, technology, financials, and legal standing of a target company. Early-stage DD is typically qualitative (founder interviews, reference checks, market analysis) because quantitative data is sparse. GitDealFlow\u2019s engineering signal adds a quantitative layer: objective GitHub activity (commit velocity, contributor growth, repo expansion) that can confirm or contradict what the team says about their velocity.",
        "why": "Founders describe their team as \u201cstrong\u201d and their velocity as \u201cfast.\u201d GitDealFlow provides a third-party check: is the team actually shipping at or above the 4,200+ tracked startup benchmark? Is velocity accelerating or plateauing? These questions have objective answers in the engineering signal, and they\u2019re especially useful when the founder\u2019s narrative and the public data diverge.",
        "why2": "GitDealFlow is not a replacement for DD \u2014 it doesn\u2019t replace reference calls, market analysis, or legal review. It\u2019s an additional data layer that can surface red flags (plateauing engineering velocity before a raise) or green flags (accelerating velocity confirming the founder\u2019s narrative) early in the process.",
        "context": "The free Technical Diligence Template (at /templates/technical-diligence-template) includes a GitDealFlow signal-snapshot field for standardizing the engineering-velocity check across deals.",
        "faqs": [
            ("Does GitDealFlow replace traditional DD?", "No. It adds a quantitative engineering-velocity layer that augments \u2014 not replaces \u2014 founder interviews, reference checks, and market analysis. Use it as a signal check alongside, not instead of, standard DD."),
            ("Can GitDealFlow detect red flags?", "Yes \u2014 a startup claiming hypergrowth but showing flat commit velocity on GitHub is a flag worth digging into. The signal doesn\u2019t prove deception, but it can highlight a discrepancy between narrative and data."),
            ("Is the methodology peer-reviewed?", "Published as SSRN preprint 6606558 and archived on Zenodo. It\u2019s open for review and replication."),
        ],
    },
    "portfolio-velocity": {
        "title": "Portfolio Velocity — Tracking Startup Performance with GitHub",
        "h1": "Portfolio velocity",
        "lede": "Portfolio velocity is the aggregate pace of progress across a fund\u2019s portfolio companies. GitDealFlow\u2019s engineering signal adds a quantitative, non-financial layer for tracking portfolio-company momentum.",
        "term": "Portfolio Velocity",
        "tagline": "Aggregate pace of progress across portfolio companies — tracked via GitHub engineering signal.",
        "def": "Portfolio velocity is how fast a fund\u2019s portfolio companies are progressing as a group. Traditionally measured in revenue growth, hiring, and round velocity, GitDealFlow adds a non-financial layer: engineering acceleration. Tracking commit velocity, contributor growth, and repo expansion across portfolio companies gives an early signal on which startups are building and which are stalling \u2014 often weeks before financial data confirms it.",
        "why": "Financial metrics lag. A startup can have a flat revenue quarter for structural reasons while simultaneously ramping engineering for the next product launch \u2014 something revenue data won\u2019t show for months. Engineering signal surfaces that ramp immediately, helping funds distinguish between a temporary pause and a structural stall.",
        "why2": "At the portfolio level, aggregate portfolio velocity gives partners a leading-indicator dashboard: is the portfolio accelerating as a group (good), plateauing (watch), or declining (intervene). Combined with traditional portfolio-review tools, it adds a layer that no financial-only review captures.",
        "context": "The Pipeline Review Template (at /templates/pipeline-review-template) includes a \u201csignal snapshot\u201d field for standardizing engineering-velocity tracking across all active deals. The Dashboard tier (\u20ac9.97/month) adds ranking and filtering for systematic portfolio tracking.",
        "faqs": [
            ("Does GitDealFlow replace traditional portfolio tracking?", "No. It adds an engineering-velocity layer that augments financial and operational tracking. Most funds run GitDealFlow alongside their existing portfolio-review tools (Carta, Notion, Affinity)."),
            ("How often is portfolio velocity updated?", "GitDealFlow updates weekly. The Sunday digest includes the top five accelerating startups; the Dashboard and Insider tiers offer continuous live tracking."),
        ],
    },
}


def render_glossary(slug, data):
    canonical = SITE + "/glossary/" + slug
    faq_sch = faq_schema(data["faqs"])
    fqs = faqs(data["faqs"])
    body = '''  <section class="h-section">
    <div class="def-box">
      <div class="term">''' + data["term"] + '''</div>
      <p style="color:#cbd5e1;margin-top:.4rem">''' + data["tagline"] + '''</p>
    </div>
    <h2>Definition</h2>
    <p>''' + data["def"] + '''</p>
    <h2>Why it matters</h2>
    <p>''' + data.get("why", "") + '''</p>
    <p>''' + data.get("why2", "") + '''</p>
    <h2>How GitDealFlow uses it</h2>
    <p>''' + data["context"] + '''</p>
    <h2>Common questions</h2>
''' + fqs + '''
    <div class="cta-final">
      <h2>Get five accelerating startups every Sunday</h2>
      <p style="color:#e0f2fe">Free, no card. 21\u201347 days before the round.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>'''
    return wrap(canonical, data["title"], re.sub(r'<[^>]+>', '', data["tagline"]),
                data["h1"], data["tagline"], body,
                schemas=[faq_sch],
                bc=[("Home", SITE + "/"), ("Glossary", SITE + "/glossary"), (data["term"], canonical)])


# ============ HUB PAGES ============
def render_hub(slug, title, h1, lede, items):
    """items: list of (name, url, description) tuples"""
    canonical = SITE + "/" + slug
    list_html = ""
    for name, url, desc in items:
        list_html += '      <li><a href="' + url + '"><strong>' + html.escape(name) + '</strong><span>' + html.escape(desc) + '</span></a></li>\n'
    body = '''  <section class="h-section">
    <ul class="hub-list">
''' + list_html + '''    </ul>
  </section>'''
    return wrap(canonical, title + " \u2014 GitDealFlow", lede, h1, lede, body,
                bc=[("Home", SITE + "/"), (title, canonical)])


def main():
    count = 0
    # Glossary pages
    for slug, data in GLOSS.items():
        out = LANDING / "glossary" / slug / "index.html"
        rendered = render_glossary(slug, data)
        out.write_text(rendered, encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', rendered, flags=re.S)).split())
        print(f"  glossary/{slug:30s} {wc}w")
        count += 1
        # Clean stale .html
        p = LANDING / "glossary" / f"{slug}.html"
        if p.exists(): p.unlink(); print(f"    removed stale {slug}.html")

    # Hub pages
    hubs = {
        "glossary": ("Glossary", "Deal flow & engineering signal terms",
            [("Scout Score", "/glossary/scout-score", "GitDealFlow\u2019s 0\u2013100 taste metric"),
             ("Engineering Momentum Score", "/glossary/engineering-momentum-score", "Composite GitHub signal"),
             ("Commit Velocity", "/glossary/commit-velocity", "One of three signals"),
             ("Contributor Diversity", "/glossary/contributor-diversity", "Team growth signal"),
             ("Star Acceleration", "/glossary/star-acceleration", "Community interest signal"),
             ("GitHub Org Activity", "/glossary/github-org-activity", "Aggregate activity source"),
             ("Deal Flow", "/glossary/deal-flow", "Investment pipeline"),
             ("Deal Velocity", "/glossary/deal-velocity", "Speed of deal progression"),
             ("Due Diligence", "/glossary/due-diligence", "Investigation process"),
             ("Portfolio Velocity", "/glossary/portfolio-velocity", "Portfolio progress tracking")]),
        "learn": ("Learn", "How-to guides for investors using deal-flow signals",
            [("What is a deal flow signal", "/learn/what-is-a-deal-flow-signal", "Definition & types"),
             ("How to find startups before they raise", "/learn/how-to-find-startups-before-they-raise", "6-step playbook"),
             ("How to track engineering velocity", "/learn/how-to-track-startup-engineering-velocity", "GitHub signal tracking"),
             ("How to track startup momentum", "/learn/how-to-track-startup-momentum", "4-layer framework")]),
        "sectors": ("Sectors", "Startup sectors tracked by GitDealFlow",
            [("AI Infrastructure", "/sectors/ai-infrastructure", "Training, inference, orchestration"),
             ("Biotech Tools", "/sectors/biotech", "Computational biology, lab platforms"),
             ("Climate Tech", "/sectors/climate-tech-startups", "Carbon, grid, energy transition"),
             ("Developer Tools", "/sectors/devtools-startups", "CI/CD, observability, platforms"),
             ("Fintech", "/sectors/fintech-startups", "Payments, banking, compliance"),
             ("Gaming", "/sectors/gaming", "Engines, platforms, backends"),
             ("HealthTech", "/sectors/healthtech-startups", "Digital health, data infrastructure"),
             ("InsurTech", "/sectors/insurtech", "Underwriting, claims, automation"),
             ("LegalTech", "/sectors/legaltech", "Contract analysis, e-discovery"),
             ("Robotics", "/sectors/robotics-startups", "Autonomous systems, automation")]),
        "templates": ("Templates", "Free templates for VCs, angels & scouts",
            [("Deal Memo Template", "/templates/deal-memo-template", "One-page evaluation format"),
             ("Investment Thesis Template", "/templates/investment-thesis-template", "Fund thesis structure"),
             ("Technical Diligence Template", "/templates/technical-diligence-template", "Engineering DD checklist"),
             ("Pipeline Review Template", "/templates/pipeline-review-template", "Weekly deal review"),
             ("Scout Report Template", "/templates/scout-report-template", "Scout-to-fund format")]),
        "cost-of": ("Cost", "Pricing breakdowns for deal-flow tools",
            [("Crunchbase pricing", "/cost-of/crunchbase-pricing", "Tiers: free to $30k+/year"),
             ("PitchBook pricing", "/cost-of/pitchbook-pricing", "Enterprise: $20k\u2013$150k+/year"),
             ("Tracxn pricing", "/cost-of/tracxn-pricing", "Mid-market: $5k\u2013$30k+/year")]),
    }
    for slug, (title, lede, items) in hubs.items():
        out = LANDING / slug / "index.html"
        rendered = render_hub(slug, title, title, lede, items)
        out.write_text(rendered, encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', rendered, flags=re.S)).split())
        print(f"  /{slug}/ index hub              {wc}w")
        count += 1

    # Accuracy fix: "400+ startup" → "4,200+ startup"
    import glob
    fixed = 0
    for f in glob.glob("**/*.html", recursive=True):
        content = Path(f).read_text(encoding="utf-8", errors="ignore")
        if "400+ startup" in content:
            content = content.replace("400+ startup", "4,200+ startup")
            Path(f).write_text(content, encoding="utf-8")
            fixed += 1
    print(f"\n  accuracy fix: '400+ startup' → '4,200+ startup' in {fixed} files")

    print(f"\nTotal: {count} pages generated + {fixed} accuracy fixes")


if __name__ == "__main__":
    main()
