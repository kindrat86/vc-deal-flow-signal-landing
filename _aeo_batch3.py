"""GitDealFlow AEO — remaining /for/ + /sectors/ + 404 expander."""
import json, html, re
from pathlib import Path

LANDING = Path("/Users/sipi/Downloads/gitdealflow/landing")
SITE = "https://gitdealflow.com"
SIGNALS = "https://signals.gitdealflow.com"
TODAY = "2026-07-18"

NAV, FOOTER, HEAD, faq_schema, faqs_html, render_page = None, None, None, None, None, None
def _init():
    global NAV, FOOTER, HEAD, faq_schema, faqs_html, render_page
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
    .pg-hero{{padding:2.5rem 1.25rem 1.5rem;max-width:780px;margin:0 auto}}
    .pg-hero h1{{font-size:clamp(1.85rem,4vw,2.5rem);line-height:1.15;font-weight:800;letter-spacing:-.02em;color:#fff;margin:.4em 0 .6em}}
    .pg-lede{{font-size:1.12rem;color:#cbd5e1;line-height:1.6;margin-bottom:1.25rem}}
    .pg-section{{max-width:780px;margin:0 auto;padding:1.25rem}}
    .pg-section h2{{font-size:1.4rem;margin:1.5rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700}}
    .pg-section p,.pg-section li{{color:#cbd5e1;line-height:1.7}}
    .pg-section ul{{padding-left:1.25rem;margin:.5rem 0}}
    .callout{{background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:.6rem;margin:1.25rem 0}}
    .callout strong{{color:#7dd3fc}}
    .faq-item{{border-bottom:1px solid #1e293b;padding:.85rem 0}}
    .faq-item summary{{cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none;font-size:1.02rem}}
    .faq-item summary::-webkit-details-marker{{display:none}}
    .faq-item summary::before{{content:"\\25b8 ";color:#0ea5e9;margin-right:.4rem}}
    .faq-item[open] summary::before{{content:"\\25be "}}
    .faq-item p{{margin:.55rem 0 0;color:#cbd5e1;line-height:1.6}}
    .cta-final{{background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2rem 1.5rem;border-radius:.8rem;margin-top:2rem;text-align:center}}
    .cta-final .btn{{display:inline-block;background:#fff;color:#0369a1;padding:.8rem 1.7rem;border-radius:.4rem;font-weight:700;margin-top:.7rem}}
    .related{{background:#0f172a80;border:1px solid #1e293b;padding:1.2rem 1.4rem;border-radius:.6rem;margin-top:2rem}}
    .related ul{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.35rem}}
    .related a{{color:#7dd3fc;text-decoration:none}}.related a:hover{{text-decoration:underline}}
  </style>"""
    def render_page(canonical, title, desc, h1, lede, body_html, extra_schemas=None, breadcrumb_crumbs=None, og=None):
        og = og or f"{SIGNALS}/opengraph-image"
        schemas = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Article",
            "headline": h1, "description": desc,
            "author": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
            "publisher": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            "datePublished": TODAY, "dateModified": TODAY,
        }) + '</script>\n  '
        if extra_schemas:
            for s in extra_schemas:
                schemas += '<script type="application/ld+json">' + json.dumps(s) + '</script>\n  '
        if breadcrumb_crumbs:
            items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                     for i, (n, u) in enumerate(breadcrumb_crumbs)]
            schemas += '<script type="application/ld+json">' + json.dumps(
                {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}) + '</script>\n  '
        nav_html = ""
        if breadcrumb_crumbs:
            parts = [
                '<a href="' + u + '" class="hover:text-gray-300">' + html_escape(n) + '</a>' if i < len(breadcrumb_crumbs) - 1
                else '<span class="text-gray-300">' + html_escape(n) + '</span>'
                for i, (n, u) in enumerate(breadcrumb_crumbs)]
            nav_html = '\n  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">' + ' <span class="mx-1">/</span> '.join(parts) + '</nav>'
        return '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n  <title>' + html_escape(title) + '</title>\n  <meta name="description" content=\"' + html_escape(desc) + '\">\n  <link rel="canonical" href=\"' + canonical + '\" />\n  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />\n  <meta property="og:type" content="article" />\n  <meta property="og:site_name" content="GitDealFlow" />\n  <meta property="og:title" content=\"' + html_escape(title) + '\" />\n  <meta property="og:description" content=\"' + html_escape(desc) + '\" />\n  <meta property="og:url" content=\"' + canonical + '\" />\n  <meta property="og:image" content=\"' + og + '\" />\n  <meta name="twitter:card" content="summary_large_image" />\n  <meta name="twitter:site" content="@data_nerd" />\n  ' + schemas + '\n' + HEAD + '\n</head>\n<body class="bg-dark-900 text-gray-100">\n' + NAV + '\n' + nav_html + '\n  <section class="pg-hero">\n    <h1>' + h1 + '</h1>\n    <p class="pg-lede">' + lede + '</p>\n  </section>\n' + body_html + '\n' + FOOTER + '\n</body>\n</html>\n'

    def faq_schema(faqs):
        return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}}
            for q, a in faqs]}

    def faqs_html(faqs):
        return "\n          ".join(
            '<details class="faq-item"><summary>' + html.escape(q) + '</summary><p>' + a + '</p></details>'
            for q, a in faqs)

_init()
html_escape = html.escape

# ============================================================================
# /for/ pages — remaining 8 thin audiences
# ============================================================================
FOR_MORE = {
    "accelerators": {
        "title": "GitDealFlow for Startup Accelerators — Scout Applicants Faster",
        "h1": "For startup accelerators",
        "lede": "Accelerators review thousands of applications. GitDealFlow\u2019s GitHub engineering signal gives you an objective filter on which teams are actually building fast \u2014 no self-reported progress required.",
        "body": "<h2>Why accelerators use GitDealFlow</h2><p>Startup accelerators (Y Combinator, Techstars, 500 Global, and others) need a way to cut through applications quickly. Self-reported traction is unreliable; public GitHub activity isn\u2019t. GitDealFlow reads commit velocity, contributor growth, and repo expansion across 4,200+ startup orgs in 20 sectors. An accelerator can benchmark any applicant with a public GitHub org against the tracked set and see whether they\u2019re truly accelerating or just describing themselves well.</p><h2>Two ways to use it</h2><p><strong>During intake:</strong> ask applicants for their GitHub org. Run it past GitDealFlow\u2019s signal threshold to see if engineering acceleration is above the published mark. That turns a subjective \u201cteam is strong\u201d into an objective data point.</p><p><strong>During the program:</strong> track participating teams\u2019 engineering velocity week over week. Teams that accelerate during the program signal real product-market discovery.</p><p class=\"disclaimer\"><strong>Important:</strong> GitDealFlow itself is <strong>not</strong> an accelerator program. It is a signal tool for investors and accelerators, and is not affiliated with Y Combinator, Techstars, 500 Global, or their cohorts.</p>",
        "faqs": [
            ("Is GitDealFlow an accelerator?", "No. GitDealFlow is a signal tool that reads public GitHub engineering activity. It is not a startup accelerator program, does not admit cohorts, and is not affiliated with Y Combinator, Techstars, or 500 Global."),
            ("Can accelerators use it to evaluate applicants?", "Yes. Any applicant with a public GitHub org can be benchmarked on engineering velocity against the 4,200+ tracked startups. It turns subjective \"team is building\" into an objective data point."),
            ("How is it different from the accelerator's own evaluation?", "Accelerator evaluations are qualitative (interviews, references, pitch). GitDealFlow adds a quantitative layer: the objective engineering velocity. The two complement each other."),
        ],
        "related": [("/for/accelerator-programs", "For accelerator programs"), ("/for/venture-scouts", "For venture scouts"), ("/best/best-startup-signal-tools", "Best tools")],
    },
    "corporate-vcs": {
        "title": "GitDealFlow for Corporate VCs — Pre-Round Startup Signal",
        "h1": "For corporate VCs",
        "lede": "Corporate VCs need to spot strategic startups before competitors do. GitDealFlow\u2019s pre-round engineering signal flags startups accelerating on GitHub weeks before the round \u2014 when partnership or investment terms are still negotiable.",
        "body": "<h2>Why corporate VCs use GitDealFlow</h2><p>Corporate venture arms (CVCs) have a harder job than traditional VCs: they need deals that are both financially sound and strategically aligned. The strategic window closes when a startup is in the press or on Crunchbase \u2014 by then the round is priced and competitors are in the data room. GitDealFlow\u2019s GitHub engineering signal flags startups 21\u201347 days before the round, when partnership conversations can still shape the outcome.</p><h2>The CVC workflow</h2><p>Most corporate VCs pair GitDealFlow (pre-round discovery) with Crunchbase or PitchBook (post-round confirmation) and run a sector-filtered watchlist. The 20-sector coverage means a CVC focused on, say, climate tech or AI infrastructure can filter the digest and dashboard to their adjacency.</p><p>The Insider Circle tier (\u20ac97/month) adds API access for integration into internal pipeline tools and custom watchlists.</p>",
        "faqs": [
            ("Which sectors are covered for CVCs?", "20 sectors including AI/ML, fintech, climate tech, developer tools, cybersecurity, enterprise SaaS, data infrastructure, robotics, and more. Filter by sector on the dashboard."),
            ("Is GitDealFlow priced for corporate budgets?", "Yes. The Insider Circle at \u20ac97/month with API access is trivial for corporate budgets and far below enterprise data-tool pricing (PitchBook at $20k+/year)."),
            ("How is this different from Crunchbase for CVCs?", "Crunchbase records rounds after they close. GitDealFlow flags startups before the round. CVCs use GitDealFlow to be early, Crunchbase to confirm."),
        ],
        "related": [("/vs/crunchbase", "vs Crunchbase"), ("/vs/pitchbook", "vs PitchBook"), ("/for/corp-dev", "For corp dev"), ("/cost-of/crunchbase-pricing", "Crunchbase pricing")],
    },
    "micro-vcs": {
        "title": "GitDealFlow for Micro VCs — Systematic Pre-Seed / Seed Discovery",
        "h1": "For micro VCs",
        "lede": "Micro VC funds ($10\u201350M) compete on early access and thesis fit. GitDealFlow\u2019s pre-round engineering signal gives analysts a systematic discovery layer without institutional pricing.",
        "body": "<h2>Why micro VCs use GitDealFlow</h2><p>Micro VCs (funds under $50M) face the same deal-flow problem as larger funds but without the infrastructure budget. PitchBook is $20k+/year/seat; Crunchbase Pro starts at $29\u2013$55/month. GitDealFlow\u2019s free Signal Digest (five accelerating startups every Sunday) plus the \u20ac9.97/month Dashboard gives a micro VC a systematic pre-round signal for less than the cost of one coffee per week.</p><h2>The micro VC stack</h2><p>Most micro VCs run: GitDealFlow (free, pre-round discovery) + Crunchbase Pro ($29\u2013$55/month, post-round confirmation) + a lightweight CRM (Affinity, Notion, or Airtable). Total stack: under $100/month per analyst.</p><p>The Dashboard tier adds ranked filters by sector, stage, and geography \u2014 enough for a small fund to run a disciplined pipeline without enterprise overhead.</p>",
        "faqs": [
            ("Is GitDealFlow enough for a micro VC on its own?", "For pre-round discovery, yes. You\u2019ll still want Crunchbase or PitchBook for post-round confirmation and investor mapping. The free tier + a cheap database covers most micro VC needs."),
            ("How does this compare to Tracxn?", "Tracxn starts at ~$5k\u2013$8k/year \u2014 often more than micro VCs want to spend at entry. GitDealFlow\u2019s free tier + $0\u201397/month dashboard is the lower-cost signal layer. See /cost-of/tracxn-pricing for the full comparison."),
            ("Can micro VCs use the API?", "Yes \u2014 the Insider Circle tier (\u20ac97/month) includes API access for integration into internal tools like Airtable and Notion."),
        ],
        "related": [("/for/seed-funds", "For seed funds"), ("/cost-of/tracxn-pricing", "Tracxn pricing"), ("/cost-of/crunchbase-pricing", "Crunchbase pricing"), ("/pricing", "Pricing")],
    },
    "hedge-funds": {
        "title": "GitDealFlow for Hedge Funds — Alternative Data for Pre-IPO Signal",
        "h1": "For hedge funds",
        "lede": "Hedge funds increasingly use alternative data to find alpha in private markets. GitDealFlow\u2019s GitHub engineering signal is a leading indicator that surfaces pre-IPO momentum before it\u2019s reflected in valuations.",
        "body": "<h2>Why hedge funds use GitDealFlow</h2><p>Hedge funds with private-market sleeves need alternative data that is early, quantitative, and not yet priced in. GitDealFlow\u2019s engineering-acceleration signal \u2014 rising commit velocity, contributor growth, and repo expansion across 4,200+ startup orgs \u2014 meets all three criteria. The signal has historically preceded fundraises by 21\u201347 days, meaning it surfaces momentum before secondaries price it and before databases record it.</p><h2>How it fits the quant workflow</h2><p>The Insider Circle tier (\u20ac97/month) includes API access, a JSON endpoint, and CSV exports, so hedge fund analysts can pipe the signal into internal models alongside other alternative data sets. The methodology is published as an SSRN preprint (abstract 6606558) for peer review.</p>",
        "faqs": [
            ("Is the signal quantitative enough for quant funds?", "Yes. The three underlying metrics (commit velocity, contributor growth, repo expansion) are numerical and published. The composite Engineering Momentum Score is a 0\u2013100 score. The methodology is peer-reviewed on SSRN (6606558)."),
            ("Can we pipe GitDealFlow data into our models?", "Yes via the API (Insider Circle), CSV export, or the MCP server for programmatic access."),
            ("Is this a replacement for other alternative data?", "No \u2014 it\u2019s one layer. Most quant funds combine GitHub signal with web traffic, hiring, and social data for a multi-signal view."),
        ],
        "related": [("/glossary/engineering-momentum-score", "Engineering Momentum Score"), ("/for/corp-dev", "For corp dev"), ("/pricing", "Pricing")],
    },
    "investment-bankers": {
        "title": "GitDealFlow for Investment Bankers — Pre-Mandate Deal Discovery",
        "h1": "For investment bankers",
        "lede": "Investment bankers who win mandates are the ones who see deals before the company hires a bank. GitDealFlow\u2019s pre-round engineering signal flags startups accelerating on GitHub 21\u201347 days before the round \u2014 before they\u2019re in the press or on banker call lists.",
        "body": "<h2>Why investment bankers use GitDealFlow</h2><p>Bankers compete on relationships and timing. The banker who calls a startup CEO the week engineering picks up (not the month the round is announced) wins the mandate. GitDealFlow reads GitHub engineering acceleration across 4,200+ startup orgs and flags the ones heating up weeks before they\u2019re on any database or press list.</p><h2>The banker workflow</h2><p>Subscribe to the free Sunday digest for awareness of the top five accelerating startups. The Dashboard (\u20ac9.97/month) adds filters by sector and geography so you can watch your coverage universe. Pair with PitchBook for valuations and deal terms once you\u2019re in the room.</p><p>The Insider Circle (\u20ac97/month) adds API access and custom watchlists for teams running systematic coverage programs.</p>",
        "faqs": [
            ("Is GitDealFlow a replacement for PitchBook?", "No. PitchBook gives you valuations and deal terms once you\u2019re in the mandate. GitDealFlow surfaces the startup before the mandate. Use GitDealFlow for discovery and timing, PitchBook for diligence and pricing."),
            ("How early is the signal?", "21\u201347 days before the fundraise announcement. The methodology is published as SSRN preprint 6606558 and validated against 219 documented fundraises."),
            ("Can a banking team set up sector watchlists?", "Yes via the Insider Circle tier which includes API access, custom watchlists, and the private Telegram group for live briefings."),
        ],
        "related": [("/vs/pitchbook", "vs PitchBook"), ("/cost-of/pitchbook-pricing", "PitchBook pricing"), ("/for/corp-dev", "For corp dev")],
    },
    "private-equity-analysts": {
        "title": "GitDealFlow for Private Equity Analysts — Growth Signal for Portfolio",
        "h1": "For private equity analysts",
        "lede": "PE analysts need to track portfolio company momentum and spot add-on targets. GitDealFlow\u2019s engineering signal provides a quantitative, non-financial growth indicator that is often visible weeks before revenue data.",
        "body": "<h2>Why PE analysts use GitDealFlow</h2><p>PE analysts track portfolio company health via financials, but financials lag. Engineering acceleration \u2014 rising commit velocity, contributor growth, repo expansion \u2014 is visible weeks earlier. For software-heavy portfolio companies and add-on acquisition targets with public GitHub orgs, GitDealFlow provides a leading indicator of whether the team is building, scaling, or stalling.</p><h2>Two use cases</h2><p><strong>Portfolio monitoring:</strong> track the engineering velocity of software portfolio companies. A plateauing signal before a revenue stall is an early warning; an accelerating signal before a growth quarter is a leading confirmation.</p><p><strong>Add-on discovery:</strong> watch for accelerating startups in adjacent sectors \u2014 candidates for bolt-on acquisitions before they\u2019re marketed by bankers.</p>",
        "faqs": [
            ("Does this work for non-software portfolio companies?", "Partial. It works best for portfolio companies with public GitHub activity \u2014 which skews toward software, SaaS, and tech-enabled businesses. It\u2019s weaker for hard assets, manufacturing, or services."),
            ("How is this different from Grata or SourceScrub?", "Grata and SourceScrub are PE-specific target search engines. GitDealFlow is a momentum layer \u2014 it tells you which targets are accelerating, not just which ones exist. See /vs/grata and /vs/source-scrub for full comparisons."),
        ],
        "related": [("/vs/grata", "vs Grata"), ("/vs/source-scrub", "vs SourceScrub"), ("/for/corp-dev", "For corp dev")],
    },
    "startup-studios": {
        "title": "GitDealFlow for Startup Studios — Validate Ideas with Engineering Signal",
        "h1": "For startup studios",
        "lede": "Startup studios build and validate ideas at high velocity. GitDealFlow\u2019s engineering signal helps studios benchmark their portfolio against the market and spot which sectors are actually accelerating.",
        "body": "<h2>Why startup studios use GitDealFlow</h2><p>Startup studios (e.g., Atomic, Science, eFounders, Pioneer Square Labs) build multiple companies in parallel. They need to know: which sectors are accelerating (so they build the right ideas), how their portfolio companies\u2019 engineering velocity compares to the market, and which emerging startups are potential competitors or partners. GitDealFlow\u2019s signal covers all three by reading public GitHub activity across 4,200+ startup orgs.</p><h2>Three studio use cases</h2><p><strong>Sector validation:</strong> before committing to a new studio idea, check whether startups in that sector are accelerating on GitHub. Rising engineering momentum in a sector suggests growing demand.</p><p><strong>Portfolio benchmarking:</strong> compare your studio\u2019s companies against the tracked set on engineering velocity. Are they building at market pace or lagging?</p><p><strong>Competitor monitoring:</strong> watch for new startups entering a sector your studio operates in \u2014 often weeks before they launch publicly.</p>",
        "faqs": [
            ("Can studios use this to benchmark portfolio companies?", "Yes. Any startup with a public GitHub org can be compared against the 4,200+ tracked startups on commit velocity, contributor growth, and repo expansion."),
            ("Does GitDealFlow work for pre-launch startups?", "Only if they have a public GitHub org. Studios that build in stealth (private repos only) won\u2019t surface in the signal, which is by design \u2014 GitDealFlow reads public GitHub activity only."),
            ("Is GitDealFlow a startup studio itself?", "No. GitDealFlow is a signal tool, not a studio, not an accelerator, and not a fund. It is not affiliated with any startup studio."),
        ],
        "related": [("/for/accelerators", "For accelerators"), ("/for/venture-scouts", "For venture scouts"), ("/best/best-startup-signal-tools", "Best tools")],
    },
}

# ============================================================================
# /sectors/ — 10 sector pages (98-143w currently)
# ============================================================================
SECTORS = {
    "ai-infrastructure": {
        "display": "AI Infrastructure",
        "blurb": "Startups building the foundational layer for the AI era: training platforms, inference optimization, model orchestration, vector databases, and GPU cloud.",
        "sectors": "LLM training, inference serving, vector databases, GPU cloud, model orchestration, MLOps, embeddings, data labeling, AI safety, agent frameworks",
        "funds": "a16z, Sequoia, Lightspeed, Index, NEA, Benchmark, Greylock, General Catalyst, Bessemer, Coatue",
        "scale": "AI infrastructure has been the single most active sector GitDealFlow tracks in 2026, with the highest average commit velocity and contributor growth across all 20 sectors.",
    },
    "biotech": {
        "display": "Biotech Tools",
        "blurb": "Software and data platforms serving biotech R&D: computational biology, protein design, lab orchestration, clinical trial analytics, and bioinformatics.",
        "sectors": "computational biology, protein design, lab automation, clinical trial analytics, bioinformatics, drug discovery software, genomics platforms",
        "funds": "a16z Bio+Health, Lux Capital, Flagship Pioneering, ARCH Venture Partners, DCVC, Obvious Ventures",
        "scale": "The software-heavy subset of biotech produces consistent GitHub signals where companies build public tools and platforms \u2014 the pure lab-only subset (no public repos) is not tracked.",
    },
    "climate-tech-startups": {
        "display": "Climate Tech",
        "blurb": "Climate and energy transition software: carbon accounting, grid optimization, EV infrastructure, climate risk modeling, and sustainable supply chain.",
        "sectors": "carbon accounting, grid optimization, EV infrastructure, climate risk modeling, sustainable supply chain, energy trading software, building efficiency, agtech",
        "funds": "Breakthrough Energy, Lowercarbon Capital, Climate Capital, Energy Impact Partners, G2 Venture Partners, Congruent Ventures",
        "scale": "Climate tech engineering activity is accelerating rapidly in 2026, particularly in carbon accounting and grid optimization \u2014 the two sub-sectors with the strongest GitHub signals.",
    },
    "devtools-startups": {
        "display": "Developer Tools",
        "blurb": "The tools developers use to build, test, deploy, and monitor software: CI/CD, observability, API platforms, code generation, and developer platforms.",
        "sectors": "CI/CD, observability, API platforms, code generation (AI), developer platforms, testing frameworks, deployment automation, infrastructure-as-code",
        "funds": "a16z, Index, Accel, Sequoia, Benchmark, Lightspeed, Madrona, Amplify Partners, boldstart ventures",
        "scale": "Developer tools produce the most consistently strong GitHub signals of any sector GitDealFlow tracks, because the customers (developers) use GitHub to evaluate the tools.",
    },
    "fintech-startups": {
        "display": "Fintech",
        "blurb": "Financial technology: payments infrastructure, banking-as-a-service, lending platforms, wealth management, insurance tech, and compliance software.",
        "sectors": "payments infrastructure, banking-as-a-service, lending platforms, wealth management, insurtech, compliance/regtech, crypto/Web3 infrastructure, accounting software",
        "funds": "a16z, Sequoia, Ribbit Capital, Index, Accel, QED Investors, Valar Ventures, Bain Capital Ventures, Lightspeed",
        "scale": "Fintech GitHub activity is concentrated in the infrastructure layer (payments, banking-as-a-service) rather than consumer fintech \u2014 these are the strongest signals.",
    },
    "gaming": {
        "display": "Gaming & Game Tech",
        "blurb": "Gaming infrastructure, game engines, developer platforms, and studios with public engineering activity on GitHub.",
        "sectors": "game engines, gaming infrastructure, developer platforms, multiplayer backends, creator tools, asset marketplaces, AI for games",
        "funds": "a16z Games, Makers Fund, Bitkraft Ventures, Galaxy Interactive, Griffin Gaming Partners, Lightspeed Gaming",
        "scale": "Gaming's GitHub signal is concentrated in infrastructure and platform companies rather than content studios \u2014 engines and backend providers produce the strongest signals.",
    },
    "healthtech-startups": {
        "display": "HealthTech",
        "blurb": "Digital health, medtech software, telehealth platforms, health data infrastructure, and clinical workflow tools.",
        "sectors": "digital health platforms, telehealth, health data infrastructure, clinical workflow, medtech software, patient engagement, provider tools",
        "funds": "a16z Bio+Health, General Catalyst, Oak HC/FT, Bessemer, Lux Capital, GV, Founders Fund, Transformation Capital",
        "scale": "HealthTech GitHub signals are strongest in data infrastructure and clinical workflow tools \u2014 the software-heavy verticals where engineering teams publish publicly.",
    },
    "insurtech": {
        "display": "InsurTech",
        "blurb": "Insurance technology: underwriting platforms, claims automation, distribution software, and insurance data infrastructure.",
        "sectors": "underwriting platforms, claims automation, distribution software, insurance data infrastructure, embedded insurance, actuarial tools",
        "funds": "Bessemer, Index, General Catalyst, Lightspeed, QED Investors, Anthemis, IA Capital, Munich Re Ventures",
        "scale": "InsurTech GitHub signals are concentrated in data infrastructure and underwriting platforms rather than distribution \u2014 the engineering-heavy subset produces the strongest pre-round indicators.",
    },
    "legaltech": {
        "display": "LegalTech",
        "blurb": "Legal technology: contract analysis, e-discovery, practice management, compliance automation, and AI-powered legal research.",
        "sectors": "contract analysis, e-discovery, practice management, compliance automation, legal research, document automation, IP management",
        "funds": "Bessemer, Index, Lightspeed, General Catalyst, Andreessen Horowitz, Nextlaw Ventures, The LegalTech Fund",
        "scale": "LegalTech GitHub signals are strongest in AI-powered legal research and contract analysis \u2014 the sub-sectors where engineering teams actively build and publish on GitHub.",
    },
    "robotics-startups": {
        "display": "Robotics",
        "blurb": "Robotics software and hardware-software companies: autonomous systems, industrial automation, drone platforms, and robotic process automation.",
        "sectors": "autonomous systems, industrial automation, drone platforms, robotic process automation, warehouse robotics, delivery robots, agricultural robotics",
        "funds": "Lux Capital, a16z, General Catalyst, Eclipse Ventures, DCVC, Founders Fund, Playground Global, Toyota Ventures",
        "scale": "Robotics GitHub signals are strongest in the software and simulation layer \u2014 autonomous driving software, perception stacks, and fleet orchestration produce the most consistent engineering signals.",
    },
}


def render_for_page(slug, data):
    canonical = f"{SITE}/for/{slug}"
    faq = faq_schema(data["faqs"])
    related = "\n        ".join(
        '<li><a href="' + u + '">' + html_escape(t) + '</a></li>' for u, t in data["related"])
    body = '''  <section class="pg-section">
    ''' + data["body"] + '''
    <h2>Common questions</h2>
          ''' + faqs_html(data["faqs"]) + '''
    <div class="related">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.5rem">Related</strong>
      <ul>
        ''' + related + '''
      </ul>
    </div>
    <div class="cta-final">
      <h2>Get this Sunday's five accelerating startups</h2>
      <p style="color:#e0f2fe">Free, no card. 21\u201347 days before the round.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>'''
    return render_page(canonical, data["title"], re.sub(r'<[^>]+>', '', data["lede"]),
                       data["h1"], data["lede"], body, extra_schemas=[faq],
                       breadcrumb_crumbs=[("Home", f"{SITE}/"), ("For", f"{SITE}/for"),
                                          (data["h1"].replace("For ", ""), canonical)])


def render_sector_page(slug, data):
    canonical = f"{SITE}/sectors/{slug}"
    faq = faq_schema([
        (f"Which {data['display']} startups does GitDealFlow track?",
         f"GitDealFlow tracks {data['display']} startups with public GitHub activity across sub-sectors including {data['sectors']}. The signal is strongest for software-heavy startups that build and publish on GitHub."),
        (f"Which funds invest in {data['display']}?",
         f"Major {data['display']} investors include {data['funds']}."),
        ("How does GitDealFlow detect acceleration in this sector?",
         "GitDealFlow reads commit velocity, contributor growth, and repository expansion for tracked startup GitHub orgs in this sector. Rising acceleration across the composite Engineering Momentum Score flags a startup for the weekly digest."),
    ])
    body = f'''  <section class="pg-section">
    <h2>The {data['display']} signal</h2>
    <p>{data['blurb']}</p>
    <p>GitDealFlow tracks {data['display']} startups through their public GitHub engineering activity: commit velocity, contributor growth, and repository expansion. The signal flags startups accelerating 21\u201347 days before the round.</p>
    <div class="callout"><strong>What we track in {data['display']}:</strong> {data['sectors']}.</div>
    <h2>Scale and signal strength</h2>
    <p>{data['scale']}</p>
    <h2>Who's active in {data['display']} funding</h2>
    <p>Key investors in {data['display']} include {data['funds']}. GitDealFlow is not affiliated with any of these funds or with the startups it tracks.</p>
    <h2>Common questions</h2>
          {faqs_html([(f"Which {data['display']} startups does GitDealFlow track?",
                       f"GitDealFlow tracks {data['display']} startups with public GitHub activity across sub-sectors including {data['sectors']}. The signal is strongest for software-heavy startups that build and publish on GitHub."),
                      (f"Which funds invest in {data['display']}?",
                       f"Major {data['display']} investors include {data['funds']}."),
                      ("How does GitDealFlow detect acceleration in this sector?",
                       "GitDealFlow reads commit velocity, contributor growth, and repository expansion for tracked startup GitHub orgs in this sector. Rising momentum flags a startup for the weekly digest.")])}
    <div class="cta-final">
      <h2>Get {data['display']} startups in your Sunday digest</h2>
      <p style="color:#e0f2fe">Free, no card. 21\u201347 days before the round.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>'''
    return render_page(canonical,
        f"{data['display']} Startup Investors — Engineering Signal | GitDealFlow",
        data["blurb"],
        f"{data['display']} startups to watch",
        f"{data['display']} startups accelerating on GitHub — tracked by GitDealFlow across 4,200+ startup orgs.",
        body, extra_schemas=[faq],
        breadcrumb_crumbs=[("Home", f"{SITE}/"), ("Sectors", f"{SITE}/sectors"),
                           (data['display'], canonical)])


def main():
    count = 0
    # /for/ pages
    for slug, data in FOR_MORE.items():
        out = LANDING / "for" / slug / "index.html"
        out.write_text(render_for_page(slug, data), encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', render_for_page(slug, data), flags=re.S)).split())
        print(f"  for/{slug:25s} {wc}w")
        count += 1
    # /sectors/ pages
    for slug, data in SECTORS.items():
        out = LANDING / "sectors" / slug / "index.html"
        out.write_text(render_sector_page(slug, data), encoding="utf-8")
        wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', render_sector_page(slug, data), flags=re.S)).split())
        print(f"  sectors/{slug:25s} {wc}w")
        count += 1
    # Clean stale .html
    for subdir, slugs in [("for", FOR_MORE), ("sectors", SECTORS)]:
        for slug in slugs:
            p = LANDING / subdir / f"{slug}.html"
            if (LANDING / subdir / slug / "index.html").exists() and p.exists():
                p.unlink()
                print(f"  removed stale {subdir}/{slug}.html")
    print(f"\nTotal: {count} pages")


if __name__ == "__main__":
    main()
