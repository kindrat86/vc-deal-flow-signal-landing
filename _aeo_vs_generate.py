"""
GitDealFlow AEO comparison-page generator.
Produces premium, dark-themed, BLUF/atomic/entity-rich /vs/{competitor} pages.

Data is hand-researched and specific (no generic boilerplate). Each page targets
the #1 AEO-cited format ("X vs Y") at 700-900 words with real differentiation.
"""
import json, os, html
from pathlib import Path

LANDING = Path("/Users/sipi/Downloads/gitdealflow/landing")
VS_DIR = LANDING / "vs"
SITE = "https://gitdealflow.com"
SIGNALS = "https://signals.gitdealflow.com"
TODAY = "2026-07-18"

# ----------------------------------------------------------------------------
# GitDealFlow canonical facts (shared across every page)
# ----------------------------------------------------------------------------
GDF = {
    "name": "GitDealFlow",
    "alt": "VC Deal Flow Signal",
    "tagline": "reads startups\u2019 public GitHub engineering activity and flags the ones accelerating \u2014 21\u201347 days before the round",
    "signal_source": "public GitHub activity (commit velocity, contributor growth, repository expansion) across 4,200+ startup orgs in 20 sectors",
    "lead_time": "21\u201347 days before the fundraise announcement",
    "lead_time_short": "21\u201347 days pre-round",
    "price_free": "Free Signal Digest (5 names every Sunday, no card)",
    "price_dash": "\u20ac9.97/mo dashboard",
    "price_insider": "\u20ac97/mo Insider Circle",
    "latency": "weekly digest + live dashboard updated continuously",
    "does_not": "it does not store funding-round histories, valuation tables, investor profiles, or contact data \u2014 it is a leading indicator, not a database",
    "methodology_url": f"{SIGNALS}/methodology",
    "ssrn": "https://ssrn.com/abstract=6606558",
}

# ----------------------------------------------------------------------------
# Competitor-specific data (real, differentiated, verifiable)
# ----------------------------------------------------------------------------
COMPETITORS = {
    "crunchbase": {
        "display": "Crunchbase",
        "tagline": "the largest public startup funding database \u2014 rounds, investors, valuations, and company profiles",
        "category": "Startup funding database & market intelligence",
        "founded": "2007 (now Morningside/AI-driven)",
        "data_basis": "crowd-sourced + web-scraped funding announcements, investor profiles, acquisition data",
        "signal_timing": "reactive \u2014 surfaces a startup after the round is announced and the press covers it",
        "strengths": [
            "Deep historical funding rounds, series, and investor lists going back over a decade",
            "Large investor and person database \u2014 who backed whom, when",
            "Maturity and breadth \u2014 the default first stop for \u201cwho raised\u201d lookups",
            "Strong API and Salesforce integrations for CRM enrichment",
        ],
        "weaknesses_for_signal": [
            "Post-round by design \u2014 it tells you a startup raised, not that one is about to",
            "No engineering-velocity or GitHub-activity signal at all",
            "Profile completeness depends on self-reporting and news coverage \u2014 thin for stealth startups",
        ],
        "price_note": "Pro plans historically start around $29\u2013$55/seat/month for individuals and climb sharply for teams and data access",
        "best_for": "teams that need a comprehensive post-round database of who raised, who invested, and company metadata",
        "verdict_gdf": "GitDealFlow is the leading indicator; Crunchbase is the record. The two answer different questions \u2014 \u201cwhich startup is about to raise\u201d vs \u201cwhich startup already raised.\u201d",
        "verdict_cb": "Choose Crunchbase if your core workflow is post-round research, investor mapping, or CRM enrichment of known companies.",
        "use_both": "Run GitDealFlow to find the startup early, then confirm the round and investors on Crunchbase when it closes.",
        "faqs": [
            ("Is GitDealFlow a Crunchbase alternative?", "No \u2014 it\u2019s a complement. Crunchbase records what happened (the round, the investors). GitDealFlow flags what\u2019s about to happen (a startup accelerating on GitHub before the round). Most serious deal-flow teams use both."),
            ("Does GitDealFlow have investor and funding-round data?", "No, and deliberately so. It carries no investor profiles, valuation tables, or round histories. Its entire job is the pre-round engineering signal."),
            ("Can I replace Crunchbase with GitDealFlow?", "Not if you need a funding database. Replace the part of your Crunchbase spend spent *looking for* new startups \u2014 keep Crunchbase for confirming rounds and investors."),
        ],
    },
    "pitchbook": {
        "display": "PitchBook",
        "tagline": "the institutional-grade private-market intelligence platform \u2014 valuations, deal terms, PE/VC data",
        "category": "Private-market data & research (Morningside)",
        "founded": "2007 (Morningside, NASDAQ-listed parent)",
        "data_basis": "analyst-curated private-market data: deal terms, valuations, fund performance, LP/GP profiles",
        "signal_timing": "post-round and historical \u2014 comprehensive once a deal is known",
        "strengths": [
            "Best-in-class valuation estimates, deal terms, and cap-table detail",
            "Deep fund-level analytics \u2014 LP/GP performance, dry powder, vintage returns",
            "Institutional rigor \u2014 the gold standard for PE/VC research desks",
            "Powerful screening and custom data exports",
        ],
        "weaknesses_for_signal": [
            "Enterprise cost \u2014 typically $20k\u2013$30k+/year/seat, sold to funds not individuals",
            "Post-round by nature \u2014 comprehensive history, no pre-round engineering signal",
            "Onboarding and sales cycle measured in weeks",
        ],
        "price_note": "Enterprise contracts, commonly reported in the tens of thousands of dollars per seat per year",
        "best_for": "institutional PE/VC research desks that need valuations, deal terms, and fund performance",
        "verdict_gdf": "GitDealFlow is a $0\u2013$97/month pre-round signal tool; PitchBook is a five-figure institutional database. They sit at opposite ends of the deal-flow stack.",
        "verdict_cb": "Choose PitchBook if you need valuations, deal terms, or fund-level analytics for institutional research.",
        "use_both": "Use GitDealFlow to spot a startup accelerating early, then pull its valuation and round terms from PitchBook when the deal closes.",
        "faqs": [
            ("Is GitDealFlow cheaper than PitchBook?", "Dramatically \u2014 GitDealFlow ranges from free to \u20ac97/month, vs PitchBook\u2019s enterprise contracts. They serve different buyers: GitDealFlow is for individual investors and small funds sourcing early; PitchBook is for institutional research desks."),
            ("Does GitDealFlow have PitchBook\u2019s valuation data?", "No. GitDealFlow carries no valuations, deal terms, or fund performance. It is purely an engineering-acceleration signal."),
            ("Can angels use PitchBook?", "Mostly no \u2014 the price puts it out of reach for individual angels and scouts. GitDealFlow was built specifically for that audience."),
        ],
    },
    "tracxn": {
        "display": "Tracxn",
        "tagline": "a private-market research platform focused on emerging-markets and sector coverage at a lower price point",
        "category": "Private-market intelligence (India-based)",
        "founded": "2013",
        "data_basis": "curated company profiles, funding rounds, sector taxonomy, investor tracking",
        "signal_timing": "post-round \u2014 records rounds and profiles after announcement",
        "strengths": [
            "Cost-effective vs PitchBook \u2014 popular with emerging-markets and boutique funds",
            "Strong sector taxonomy and emerging-markets coverage (India, SEA, MENA)",
            "Decent screening and watchlist tooling",
        ],
        "weaknesses_for_signal": [
            "Post-round \u2014 no pre-round engineering signal",
            "Coverage depth outside emerging markets is thinner than Crunchbase/PitchBook",
            "Profile freshness varies by sector",
        ],
        "price_note": "custom pricing, generally below PitchBook; commonly mid-thousands per seat/year",
        "best_for": "funds focused on emerging markets and sector-screening workflows",
        "verdict_gdf": "GitDealFlow adds the pre-round engineering layer Tracxn doesn\u2019t have; Tracxn adds sector and emerging-markets depth GitDealFlow doesn\u2019t claim.",
        "verdict_cb": "Choose Tracxn for emerging-markets and sector-screening depth at a lower price than PitchBook.",
        "use_both": "Pair GitDealFlow\u2019s GitHub signal with Tracxn\u2019s sector screens to triangulate early movers.",
        "faqs": [
            ("GitDealFlow vs Tracxn for emerging markets?", "Tracxn has broader emerging-markets company and investor metadata. GitDealFlow reads GitHub engineering activity globally \u2014 useful for any startup with a public GitHub org, which skews developer-heavy sectors."),
            ("Is GitDealFlow cheaper than Tracxn?", "GitDealFlow has a permanent free tier; Tracxn is a paid platform. For the specific pre-round signal use case, GitDealFlow is far cheaper."),
        ],
    },
    "grata": {
        "display": "Grata",
        "tagline": "a B2B company-search engine built for M&A sourcing and private-equity deal discovery",
        "category": "B2B search engine for M&A/PE sourcing",
        "founded": "2020",
        "data_basis": "web-scale NLP over company websites \u2014 classifies private businesses by what they do, not just metadata",
        "signal_timing": "static company profiles \u2014 no funding timing signal",
        "strengths": [
            "Best-in-class B2B company search by function, technology, and niche",
            "Purpose-built for PE/M&A sourcing workflows",
            "Covers the long tail of small private companies databases miss",
        ],
        "weaknesses_for_signal": [
            "No GitHub or engineering-activity signal",
            "No fundraise timing \u2014 Grata finds companies, not momentum",
            "Geared toward PE buyout sourcing, not early-stage VC signal",
        ],
        "price_note": "enterprise pricing, sold to PE and M&A teams",
        "best_for": "PE/M&A teams sourcing acquisition targets by business function",
        "verdict_gdf": "Grata answers \u201cfind me companies that do X\u201d; GitDealFlow answers \u201cwhich of them is heating up right now.\u201d",
        "verdict_cb": "Choose Grata for B2B/PE target screening by business function.",
        "use_both": "Use Grata to build a long list, then GitDealFlow to rank who is accelerating.",
        "faqs": [
            ("Is GitDealFlow a Grata alternative for M&A sourcing?", "No \u2014 GitDealFlow is a momentum signal, not a B2B search engine. Grata finds companies by function; GitDealFlow detects which are accelerating on GitHub."),
        ],
    },
    "affinity": {
        "display": "Affinity",
        "tagline": "a relationship-intelligence CRM for VCs \u2014 manages contacts, deals, and network graph",
        "category": "Relationship-intelligence CRM (VC/PE)",
        "founded": "2017",
        "data_basis": "email/calendar enrichment + manual deal pipeline; a CRM, not a data provider",
        "signal_timing": "not a signal tool \u2014 it organizes deals your team already knows about",
        "strengths": [
            "Strong CRM and relationship-graph automation for deal teams",
            "Auto-enriches contacts from email and calendar",
            "Great for managing a partnership\u2019s deal pipeline",
        ],
        "weaknesses_for_signal": [
            "No discovery signal \u2014 it tracks known deals, not new ones",
            "No GitHub or engineering-activity data",
            "Requires a team using it as their CRM to deliver value",
        ],
        "price_note": "per-seat SaaS, mid-hundreds to thousands per seat/year",
        "best_for": "VC/PE teams that need relationship-driven CRM and pipeline management",
        "verdict_gdf": "Affinity manages the deals you already have; GitDealFlow finds the ones you don\u2019t. They\u2019re adjacent layers, not substitutes.",
        "verdict_cb": "Choose Affinity to run your deal pipeline and relationship graph.",
        "use_both": "GitDealFlow surfaces early startups; pipe them into Affinity to track the relationship.",
        "faqs": [
            ("Is GitDealFlow an Affinity alternative?", "No \u2014 Affinity is a relationship CRM; GitDealFlow is a discovery signal. They solve different problems in the deal-flow stack."),
        ],
    },
    "source-scrub": {
        "display": "SourceScrub",
        "tagline": "a deal-sourcing platform aggregating bootstrapped and founder-led companies for PE",
        "category": "Deal-sourcing platform (PE-focused)",
        "founded": "2015",
        "data_basis": "curated lists of bootstrapped/PE-sellable companies + conference and research data",
        "signal_timing": "static sourcing lists \u2014 no momentum or timing signal",
        "strengths": [
            "Strong coverage of bootstrapped and founder-led companies PE cares about",
            "Industry and conference data aggregation",
            "Built for PE sourcing workflows",
        ],
        "weaknesses_for_signal": [
            "No GitHub or engineering-activity signal",
            "PE/buyout focus, not early-stage VC",
            "Lists age; no real-time momentum",
        ],
        "price_note": "enterprise, sold to PE sourcing teams",
        "best_for": "PE firms sourcing bootstrapped acquisition targets",
        "verdict_gdf": "SourceScrub builds static target lists for PE; GitDealFlow detects live momentum in startups that code.",
        "verdict_cb": "Choose SourceScrub for bootstrapped-company PE sourcing.",
        "use_both": "Limited overlap \u2014 different end-buyers (PE vs early-stage VC).",
        "faqs": [
            ("Is GitDealFlow a SourceScrub alternative?", "Only loosely. SourceScrub serves PE buyout sourcing with static lists; GitDealFlow serves early-stage VC with a live engineering signal."),
        ],
    },
    "dealroom": {
        "display": "Dealroom",
        "tagline": "a European private-company data platform \u2014 startup, investor, and round data with strong EU coverage",
        "category": "Private-company data (EU-focused)",
        "founded": "2013 (Amsterdam)",
        "data_basis": "curated European and global startup/investor profiles, rounds, and ecosystem data",
        "signal_timing": "post-round \u2014 records rounds after announcement",
        "strengths": [
            "Best-in-class European ecosystem coverage",
            "Used by governments and EU funds for ecosystem analysis",
            "Strong company, investor, and round metadata",
        ],
        "weaknesses_for_signal": [
            "Post-round by nature \u2014 no pre-round engineering signal",
            "Global coverage thinner outside Europe",
        ],
        "price_note": "freemium + paid tiers",
        "best_for": "European-focused investors and ecosystem analysts",
        "verdict_gdf": "Dealroom excels at European company and round data; GitDealFlow adds the pre-round GitHub signal.",
        "verdict_cb": "Choose Dealroom for EU ecosystem depth and round/investor metadata.",
        "use_both": "GitDealFlow to spot early; Dealroom to profile the European ecosystem context.",
        "faqs": [
            ("GitDealFlow vs Dealroom for European startups?", "Dealroom has deeper EU company/investor metadata. GitDealFlow reads GitHub activity for any startup with a public org \u2014 a complementary pre-round signal."),
        ],
    },
    "cb-insights": {
        "display": "CB Insights",
        "tagline": "a tech-market-intelligence platform \u2014 research, emerging-tech tracking, and analyst briefings",
        "category": "Tech market intelligence & research",
        "founded": "2008",
        "data_basis": "analyst research, emerging-tech tracking, market maps, and news-derived signals",
        "signal_timing": "thematic and post-event \u2014 trends, research, and news analysis",
        "strengths": [
            "Industry-leading emerging-tech research and market maps",
            "Analyst briefings and custom research",
            "Strong for strategy and market-intelligence teams",
        ],
        "weaknesses_for_signal": [
            "Research-driven, not a real-time startup-discovery signal",
            "No GitHub or engineering-activity data",
            "Enterprise pricing and workflow",
        ],
        "price_note": "enterprise research subscriptions",
        "best_for": "corporate strategy and market-intelligence teams",
        "verdict_gdf": "CB Insights tells you which technologies are trending; GitDealFlow tells you which specific startups are accelerating this week.",
        "verdict_cb": "Choose CB Insights for market research and emerging-tech strategy.",
        "use_both": "CB Insights for the macro thesis; GitDealFlow for the named, tradable startups.",
        "faqs": [
            ("Is GitDealFlow a CB Insights alternative?", "No \u2014 CB Insights is a research/market-intelligence product; GitDealFlow is a pre-round startup signal. They operate at different altitudes."),
        ],
    },
    "angellist": {
        "display": "AngelList / Wellfound",
        "tagline": "the startup jobs + investing platform \u2014 syndicates, recruit, and company profiles",
        "category": "Startup jobs & syndicate platform",
        "founded": "2010 (now Wellfound for recruiting)",
        "data_basis": "self-reported company profiles, job listings, and syndicate deal flow",
        "signal_timing": "self-reported and reactive \u2014 companies update their own profiles",
        "strengths": [
            "Largest startup jobs and recruiting surface",
            "Angel syndicates for co-investing",
            "Free company and founder profiles",
        ],
        "weaknesses_for_signal": [
            "Self-reported \u2014 stealth startups stay hidden",
            "No engineering-activity signal",
            "Optimized for recruiting, not deal sourcing",
        ],
        "price_note": "free for founders and candidates; syndicate carry for investors",
        "best_for": "startup recruiting and angel-syndicate participation",
        "verdict_gdf": "AngelList is a jobs and syndicate platform; GitDealFlow is a pre-round discovery signal that doesn\u2019t depend on startups self-reporting.",
        "verdict_cb": "Choose AngelList/Wellfound for recruiting and syndicate investing.",
        "use_both": "GitDealFlow finds stealth startups early; AngelList for founder outreach and syndicate participation.",
        "faqs": [
            ("Is GitDealFlow an AngelList alternative?", "No. AngelList is a recruiting and syndicate platform; GitDealFlow is a discovery signal. GitDealFlow finds startups AngelList doesn\u2019t know about yet because they haven\u2019t self-reported."),
        ],
    },
    "privateequitywire": {
        "display": "Private Equity Wire",
        "tagline": "a PE/VC news and fund-data wire \u2014 LP/GP news, fund announcements, and performance data",
        "category": "PE/VC news & fund data",
        "founded": "news/data service",
        "data_basis": "editorial PE/VC news, fund announcements, and performance data feeds",
        "signal_timing": "news-driven and post-announcement",
        "strengths": [
            "Timely PE/VC fund-level news and LP/GP announcements",
            "Fund performance and fundraising data",
            "Editorial quality and industry reach",
        ],
        "weaknesses_for_signal": [
            "News-driven \u2014 reports after the fact",
            "Fund-level, not startup-level signal",
            "No engineering or momentum data",
        ],
        "price_note": "subscription",
        "best_for": "LPs and fund-of-funds tracking PE/VC fund news",
        "verdict_gdf": "Private Equity Wire covers fund-level news; GitDealFlow covers startup-level pre-round signal.",
        "verdict_cb": "Choose PEW for LP/GP fund news and performance.",
        "use_both": "Different layers \u2014 LP/fund intelligence vs startup signal.",
        "faqs": [
            ("Is GitDealFlow a Private Equity Wire alternative?", "No \u2014 they cover different things. PEW is fund-level news; GitDealFlow is a startup-level pre-round signal."),
        ],
    },
    "privco": {
        "display": "PrivCo",
        "tagline": "a private-company financials database \u2014 revenue, valuation, and deal data",
        "category": "Private-company financials database",
        "founded": "2011",
        "data_basis": "private-company financials, valuations, and deal data",
        "signal_timing": "post-round and historical financial records",
        "strengths": [
            "Private-company revenue and financial estimates",
            "Valuation and deal data",
            "Useful for due-diligence on known targets",
        ],
        "weaknesses_for_signal": [
            "Post-round / historical \u2014 no pre-round signal",
            "No engineering or GitHub data",
            "Strongest for DD, not discovery",
        ],
        "price_note": "subscription",
        "best_for": "analysts needing private-company financials for due diligence",
        "verdict_gdf": "PrivCo answers \u201cwhat are this company\u2019s financials\u201d; GitDealFlow answers \u201cis this company about to raise.\u201d",
        "verdict_cb": "Choose PrivCo for private-company financial estimates in DD.",
        "use_both": "GitDealFlow to find; PrivCo to diligence.",
        "faqs": [
            ("Is GitDealFlow a PrivCo alternative?", "No \u2014 PrivCo is a financials database; GitDealFlow is a discovery signal. Adjacent, not substitutes."),
        ],
    },
    "sourcingsys": {
        "display": "Sourcing.io / Sourcing Systems",
        "tagline": "a GitHub-developer search tool used by technical recruiters and investors",
        "category": "GitHub developer search",
        "founded": "developer search tool",
        "data_basis": "search over individual GitHub developer profiles by language, repo, and activity",
        "signal_timing": "developer-level search, no startup-level momentum",
        "strengths": [
            "Direct GitHub developer search by skill, repo, and language",
            "Useful for technical recruiting and founder-scouting at the person level",
            "Simple, focused interface",
        ],
        "weaknesses_for_signal": [
            "Developer-level, not org/startup-level \u2014 no team momentum signal",
            "No commit-velocity or contributor-growth aggregation",
            "Not designed for deal-flow timing",
        ],
        "price_note": "subscription",
        "best_for": "technical recruiters searching individual developers",
        "verdict_gdf": "Sourcing tools find individual developers; GitDealFlow aggregates org-level engineering acceleration across thousands of startups to predict raises.",
        "verdict_cb": "Choose a GitHub-developer search for recruiting individual engineers.",
        "use_both": "Limited overlap \u2014 person search vs org-level startup signal.",
        "faqs": [
            ("Is GitDealFlow a GitHub developer-search tool?", "No. Developer-search tools find individual people; GitDealFlow reads org-level engineering acceleration across 4,200+ startup GitHub orgs to predict fundraises."),
        ],
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
      <p class="text-gray-400 text-sm">Not affiliated with Y Combinator, Techstars, 500 Global, or any incumbent data provider.</p>
      <div class="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mt-5">
        <a href="/" class="py-2 inline-block hover:text-gray-300">Home</a>
        <a href="/cheatsheet" class="py-2 inline-block hover:text-gray-300">Cheat sheet</a>
        <a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
        <a href="/privacy" class="py-2 inline-block hover:text-gray-300">Privacy</a>
        <a href="/terms" class="py-2 inline-block hover:text-gray-300">Terms</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 GitDealFlow \u00b7 signals@gitdealflow.com</p>
    </div>
  </footer>"""


def other_comparisons(current: str) -> str:
    links = []
    for slug, c in COMPETITORS.items():
        if slug == current:
            continue
        links.append(f'<li><a href="{SITE}/vs/{slug}">GitDealFlow vs {c["display"]}</a></li>')
    return "\n        ".join(links)


def render(slug: str, c: dict) -> str:
    display = c["display"]
    strengths = "\n            ".join(f"<li>{html.escape(s)}</li>" for s in c["strengths"])
    weaknesses = "\n            ".join(f"<li>{html.escape(w)}</li>" for w in c["weaknesses_for_signal"])
    faq_items_schema = []
    faq_items_html = []
    for q, a in c["faqs"]:
        qa = html.escape(q)
        aa = html.escape(a)
        faq_items_schema.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        })
        faq_items_html.append(
            f'<details class="faq-item"><summary>{qa}</summary><p>{aa}</p></details>'
        )
    faqs_html = "\n          ".join(faq_items_html)
    faqs_schema = json.dumps(faq_items_schema)

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"GitDealFlow vs {display}: pre-round GitHub signal vs {c['category'].lower()}",
        "description": f"GitDealFlow vs {display}: what each does, where each wins, and when to use which. {c['verdict_gdf']}",
        "author": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "publisher": {"@type": "Organization", "name": "GitDealFlow", "url": SITE},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/vs/{slug}"},
        "datePublished": TODAY,
        "dateModified": TODAY,
        "about": [
            {"@type": "Thing", "name": "deal flow signal"},
            {"@type": "Thing", "name": "alternative data for investors"},
            {"@type": "Thing", "name": c["category"]},
        ],
    }

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Comparisons", "item": f"{SITE}/vs"},
            {"@type": "ListItem", "position": 3, "name": f"vs {display}", "item": f"{SITE}/vs/{slug}"},
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>GitDealFlow vs {display} [2026] \u2014 Pre-Round GitHub Signal vs {c['category']}</title>
  <meta name="description" content="GitDealFlow vs {display}: {c['verdict_gdf']} What each does, where each wins, pricing, and when to use which.">
  <link rel="canonical" href="{SITE}/vs/{slug}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="GitDealFlow" />
  <meta property="og:title" content="GitDealFlow vs {display} [2026 Comparison]" />
  <meta property="og:description" content="{c['verdict_gdf']}" />
  <meta property="og:url" content="{SITE}/vs/{slug}" />
  <meta property="og:image" content="{SIGNALS}/opengraph-image" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@data_nerd" />
  <meta name="twitter:creator" content="@data_nerd" />
  <meta name="twitter:title" content="GitDealFlow vs {display} [2026]" />
  <meta name="twitter:description" content="{c['verdict_gdf']}" />
  <meta name="twitter:image" content="{SIGNALS}/opengraph-image" />
  <link rel="alternate" type="text/plain" title="LLMs.txt" href="{SITE}/llms.txt" />
  <script type="application/ld+json">{json.dumps(article_schema)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb)}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":{faqs_schema}}}</script>
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
    .faq-item summary::before{{content:"\u25b8 ";color:#0ea5e9;margin-right:.4rem}}
    .faq-item[open] summary::before{{content:"\u25be "}}
    .faq-item p{{margin:.6rem 0 0;color:#cbd5e1;line-height:1.65}}
    .related{{background:#0f172a80;border:1px solid #1e293b;padding:1.25rem 1.5rem;border-radius:.6rem;margin-top:2rem}}
    .related ul{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.4rem}}
    .related a{{color:#7dd3fc;text-decoration:none}}.related a:hover{{text-decoration:underline}}
    .disclaimer{{font-size:.85rem;color:#64748b;font-style:italic;margin-top:1.5rem}}
  </style>
</head>
<body class="bg-dark-900 text-gray-100">
{NAV}
  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400" aria-label="Breadcrumb">
    <a href="/" class="hover:text-gray-300">Home</a> <span class="mx-1">/</span>
    <a href="/vs" class="hover:text-gray-300">Comparisons</a> <span class="mx-1">/</span>
    <span class="text-gray-300">vs {display}</span>
  </nav>

  <section class="vs-hero">
    <span class="inline-block text-xs font-semibold uppercase tracking-wider text-sky-400 bg-sky-500/10 border border-sky-500/30 rounded-full px-3 py-1 mb-4">2026 Comparison</span>
    <h1>GitDealFlow vs {display}</h1>
    <p class="vs-lede"><strong class="text-white">Bottom line up front:</strong> {c['verdict_gdf']}</p>
    <p class="vs-lede">{display} is {c['tagline']}. GitDealFlow is a pre-round signal tool \u2014 it {GDF['tagline']}. {GDF['does_not']}.</p>
  </section>

  <section class="vs-section">
    <h2>The 30-second comparison</h2>
    <table class="vs-table">
      <thead><tr><th>Dimension</th><th>GitDealFlow</th><th>{display}</th></tr></thead>
      <tbody>
        <tr><td>Category</td><td>Pre-round engineering-acceleration signal</td><td>{c['category']}</td></tr>
        <tr><td>What the data is</td><td>{GDF['signal_source']}</td><td>{c['data_basis']}</td></tr>
        <tr><td>Signal timing</td><td>{GDF['lead_time']}</td><td>{c['signal_timing']}</td></tr>
        <tr><td>Best for</td><td>Angels, scouts, and seed/Series A funds sourcing early</td><td>{c['best_for']}</td></tr>
        <tr><td>Price range</td><td>Free to \u20ac97/month</td><td>{c['price_note']}</td></tr>
        <tr><td>Setup</td><td>Minutes \u2014 subscribe and read</td><td>Sales-led or self-serve per tier</td></tr>
      </tbody>
    </table>
  </section>

  <section class="vs-section">
    <h2>What {display} does well</h2>
    <p>{display} earns its place in the stack as {c['tagline']}. Its real strengths:</p>
    <ul>
            {strengths}
    </ul>
  </section>

  <section class="vs-section">
    <h2>Where GitDealFlow is different</h2>
    <p>GitDealFlow is not a broader version of {display} \u2014 it is a different kind of instrument. {display} records what already happened. GitDealFlow flags what is about to. The data is {GDF['signal_source']}, and the acceleration patterns it surfaces have historically preceded fundraise announcements by {GDF['lead_time']}.</p>
    <p>Concretely, that means GitDealFlow will show you a startup accelerating <em>before</em> {display} has a round on file for it. {GDF['does_not']}.</p>
    <ul>
            {weaknesses}
    </ul>
    <div class="callout-warn"><strong>Important:</strong> {display} is not wrong or bad \u2014 it answers a different question. Most serious deal-flow teams run both: a database for the record, and a signal for the lead.</div>
  </section>

  <section class="vs-section">
    <h2>The verdict</h2>
    <div class="verdict">
      <p><strong>Choose GitDealFlow if</strong> your problem is finding startups <em>before</em> the round. {c['verdict_gdf']}</p>
    </div>
    <div class="verdict">
      <p><strong>Choose {display} if</strong> {c['verdict_cb']}</p>
    </div>
    <p style="margin-top:1.25rem"><strong>Use both:</strong> {c['use_both']}</p>
  </section>

  <section class="vs-section">
    <h2>Common questions</h2>
          {faqs_html}
  </section>

  <section class="vs-section">
    <h2>Pricing context</h2>
    <p>GitDealFlow ranges from a permanent free Signal Digest (5 startups every Sunday, no card) to a \u20ac9.97/month dashboard and a \u20ac97/month Insider Circle. {display} is {c['price_note']}. For individual angels and small funds, the gap is large; for institutional desks, it reflects very different products.</p>
    <p class="disclaimer">Pricing for third-party tools reflects publicly reported ranges at time of writing and changes over time \u2014 verify on each vendor\u2019s site. GitDealFlow pricing is live on the <a href="/pricing" class="text-sky-400">pricing page</a>.</p>
  </section>

  <section class="vs-section">
    <div class="cta-final">
      <h2>See the startups accelerating this week</h2>
      <p style="color:#e0f2fe">Five names every Sunday, 21\u201347 days before the round. Free, no card.</p>
      <a href="/#signup-hero" class="btn">Get this Sunday\u2019s 5 names &rarr;</a>
    </div>
  </section>

  <section class="vs-section">
    <div class="related">
      <strong style="color:#e2e8f0;display:block;margin-bottom:.6rem">More comparisons</strong>
      <ul>
        {other_comparisons(slug)}
      </ul>
    </div>
  </section>

{FOOTER}
</body>
</html>
"""


def main():
    # Write canonical /vs/{slug}/index.html for every competitor
    out_paths = []
    for slug, c in COMPETITORS.items():
        out_dir = VS_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "index.html"
        out.write_text(render(slug, c), encoding="utf-8")
        # word count check
        import re
        body = re.sub(r"<[^>]+>", " ", render(slug, c))
        words = len([w for w in body.split() if w])
        out_paths.append((str(out), words))
        print(f"  wrote {slug:20s} {words}w")

    # Remove stale duplicate .html files that conflict under cleanUrls
    stale = [VS_DIR / f"{s}.html" for s in
             ["affinity", "crunchbase", "grata", "pitchbook", "privco",
              "source-scrub", "sourcingsys", "tracxn"]]
    # Only remove the ones that have a canonical /slug/ dir
    for p in stale:
        slug = p.stem
        if (VS_DIR / slug / "index.html").exists() and p.exists():
            p.unlink()
            print(f"  removed stale {p.name}")

    # Build /vs/ hub index
    hub = VS_DIR / "index.html"
    items = "\n      ".join(
        f'<li><a href="{SITE}/vs/{slug}"><strong>GitDealFlow vs {c["display"]}</strong>'
        f' <span>\u2014 {c["category"]}</span></a></li>'
        for slug, c in COMPETITORS.items()
    )
    hub.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>GitDealFlow vs the Alternatives \u2014 2026 Comparisons</title>
  <meta name="description" content="Honest, specific comparisons of GitDealFlow against Crunchbase, PitchBook, Tracxn, Grata, Affinity, SourceScrub, Dealroom, CB Insights, and more.">
  <link rel="canonical" href="{SITE}/vs" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta property="og:title" content="GitDealFlow vs the Alternatives \u2014 2026 Comparisons" />
  <meta property="og:description" content="Honest, specific comparisons of GitDealFlow against the major deal-flow databases and tools." />
  <meta property="og:url" content="{SITE}/vs" />
  <meta property="og:image" content="{SIGNALS}/opengraph-image" />
  <meta name="theme-color" content="#0f172a" />
  <meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="/styles.css" as="style">
  <link rel="stylesheet" href="/styles.css">
</head>
<body class="bg-dark-900 text-gray-100">
{NAV}
  <section style="max-width:760px;margin:0 auto;padding:3rem 1.25rem 1rem">
    <h1 style="font-size:clamp(1.9rem,4vw,2.6rem);color:#fff;font-weight:800;letter-spacing:-.02em;line-height:1.15">GitDealFlow vs the alternatives</h1>
    <p style="color:#cbd5e1;font-size:1.1rem;line-height:1.6;margin-top:.75rem">Honest, specific comparisons. GitDealFlow is a pre-round engineering-acceleration signal \u2014 not a funding database, not a CRM, not a search engine. These pages spell out exactly where each tool wins and where GitDealFlow is different.</p>
  </section>
  <section style="max-width:760px;margin:0 auto;padding:1rem 1.25rem 3rem">
    <ul style="list-style:none;padding:0;margin:0;display:grid;gap:.5rem">
      {items}
    </ul>
  </section>
{FOOTER}
</body>
</html>
""", encoding="utf-8")
    print(f"  wrote hub /vs/index.html")

    print(f"\nTotal: {len(out_paths)} comparison pages + 1 hub")


if __name__ == "__main__":
    main()
