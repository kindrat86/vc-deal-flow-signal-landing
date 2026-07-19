"""Generate a linkable statistics page + sector/city matrix for gitdealflow.com."""
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
        <a href="/best/best-startup-signal-tools" class="hover:text-white transition-colors">Best tools</a>
        <a href="/vs" class="hover:text-white transition-colors">Comparisons</a>
        <a href="/stats" class="hover:text-white transition-colors">Stats</a>
        <a href="/pricing" class="hover:text-white transition-colors">Pricing</a>
      </nav>
      <a href="/#signup-hero" class="btn btn-primary btn-no-pulse btn-sm whitespace-nowrap shrink-0">Get the 5 names &rarr;</a>
    </div>
  </header>"""

FOOTER = """  <footer class="border-t border-gray-800 bg-dark-900/80 py-12">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 text-center">
      <p class="text-gray-300 mb-2 font-semibold">GitDealFlow is a deal-flow signal tool for investors — not a fund and not a startup accelerator.</p>
      <div class="flex flex-wrap justify-center gap-6 text-gray-400 text-sm mt-5">
        <a href="/" class="py-2 inline-block hover:text-gray-300">Home</a><a href="/stats" class="py-2 inline-block hover:text-gray-300">Stats</a><a href="/best/best-startup-signal-tools" class="py-2 inline-block hover:text-gray-300">Best tools</a><a href="/vs" class="py-2 inline-block hover:text-gray-300">Comparisons</a><a href="/pricing" class="py-2 inline-block hover:text-gray-300">Pricing</a>
      </div>
      <p class="text-gray-500 text-xs mt-6">&copy; 2026 GitDealFlow</p>
    </div>
  </footer>"""

HEAD = """  <meta name="theme-color" content="#0f172a" /><meta name="color-scheme" content="dark" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/styles.css" as="style"><link rel="stylesheet" href="/styles.css">
  <style>
    .pg-h{padding:2.5rem 1.25rem 1.5rem;max-width:820px;margin:0 auto}
    .pg-h h1{font-size:clamp(1.85rem,4vw,2.5rem);line-height:1.15;font-weight:800;color:#fff;margin:.4em 0 .6em}
    .pg-l{font-size:1.12rem;color:#cbd5e1;line-height:1.6;margin-bottom:1.25rem}
    .pg-s{max-width:820px;margin:0 auto;padding:1.25rem}
    .pg-s h2{font-size:1.4rem;margin:1.75rem 0 .6rem;padding-bottom:.4rem;border-bottom:2px solid #1e293b;color:#f1f5f9;font-weight:700}
    .pg-s h3{font-size:1.15rem;margin:1.3rem 0 .5rem;color:#e2e8f0;font-weight:600}
    .pg-s p,.pg-s li{color:#cbd5e1;line-height:1.7}
    .pg-s ul{padding-left:1.25rem;margin:.5rem 0}
    .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1rem;margin:1.5rem 0}
    .stat-card{background:linear-gradient(135deg,#0ea5e915,#0ea5e905);border:1px solid #0ea5e955;border-radius:.65rem;padding:1.4rem;text-align:center}
    .stat-card .num{font-size:2.2rem;font-weight:800;color:#0ea5e9;line-height:1.1}
    .stat-card .label{color:#cbd5e1;font-size:.92rem;margin-top:.4rem}
    .stat-card .source{color:#64748b;font-size:.75rem;margin-top:.5rem}
    .cite-box{background:#0f172a99;border:1px solid #334155;border-radius:.5rem;padding:1rem 1.25rem;margin:1rem 0;font-family:monospace;font-size:.85rem;color:#94a3b8}
    .callout{background:linear-gradient(135deg,#0ea5e922,#0ea5e908);border:1px solid #0ea5e955;border-left:4px solid #0ea5e9;padding:1.1rem 1.4rem;border-radius:.6rem;margin:1.25rem 0}
    .callout strong{color:#7dd3fc}
    .faq-item{border-bottom:1px solid #1e293b;padding:.85rem 0}
    .faq-item summary{cursor:pointer;font-weight:600;color:#e2e8f0;list-style:none;font-size:1.02rem}
    .faq-item summary::before{content:"\\25b8 ";color:#0ea5e9;margin-right:.4rem}
    .faq-item p{margin:.55rem 0 0;color:#cbd5e1;line-height:1.6}
    .cta-f{background:linear-gradient(135deg,#0ea5e9,#0369a1);color:#fff;padding:2rem 1.5rem;border-radius:.8rem;margin-top:2rem;text-align:center}
    .cta-f .btn{display:inline-block;background:#fff;color:#0369a1;padding:.8rem 1.7rem;border-radius:.4rem;font-weight:700;margin-top:.7rem}
    .toc{background:#0f172a80;border:1px solid #1e293b;padding:1.2rem 1.4rem;border-radius:.6rem;margin:1.5rem 0}
    .toc ol{color:#cbd5e1;padding-left:1.25rem;margin:.5rem 0}
    .toc a{color:#7dd3fc}
  </style>"""

def wrap(c, t, d, h1, l, b, schemas=None, bc=None):
    og = f"{SIGNALS}/opengraph-image"
    sch = '<script type="application/ld+json">' + json.dumps({
        "@context":"https://schema.org","@type":"Article","headline":h1,"description":d,
        "author":{"@type":"Organization","name":"GitDealFlow","url": SITE},
        "publisher":{"@type":"Organization","name":"GitDealFlow","url": SITE},
        "mainEntityOfPage":{"@type":"WebPage","@id":c},"datePublished":TODAY,"dateModified":TODAY
    }) + '</script>\n  '
    if schemas:
        for s in schemas: sch += '<script type="application/ld+json">' + json.dumps(s) + '</script>\n  '
    if bc:
        items=[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(bc)]
        sch += '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}) + '</script>\n  '
    navh=""
    if bc:
        ps=[]
        for i,(n,u) in enumerate(bc):
            ps.append('<a href="'+u+'" class="hover:text-gray-300">'+n+'</a>' if i<len(bc)-1 else '<span class="text-gray-300">'+n+'</span>')
        navh='\n  <nav class="max-w-5xl mx-auto px-4 sm:px-6 py-3 text-sm text-gray-400">'+' <span class="mx-1">/</span> '.join(ps)+'</nav>'
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n  <title>'+t+'</title>\n  <meta name="description" content="'+d+'">\n  <link rel="canonical" href="'+c+'" />\n  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />\n  <meta property="og:title" content="'+t+'" />\n  <meta property="og:description" content="'+d+'" />\n  <meta property="og:url" content="'+c+'" />\n  <meta property="og:image" content="'+og+'" />\n  <meta name="twitter:card" content="summary_large_image" />\n  '+sch+'\n'+HEAD+'\n</head>\n<body class="bg-dark-900 text-gray-100">\n'+NAV+'\n'+navh+'\n  <section class="pg-h">\n    <h1>'+h1+'</h1>\n    <p class="pg-l">'+l+'</p>\n  </section>\n'+b+'\n'+FOOTER+'\n</body>\n</html>\n'


# ========================================================================
# 1. STATISTICS PAGE — linkable asset for journalist citations
# ========================================================================
stats = [
    ("21–47", "days before the round", "GitDealFlow's GitHub engineering-acceleration signal historically precedes fundraise announcements by 21 to 47 days.", "Validated against 219 documented fundraises. SSRN preprint 6606558."),
    ("4,200+", "startup GitHub orgs tracked", "GitDealFlow monitors public GitHub engineering activity across more than 4,200 startup organizations in 20 sectors.", "Continuously updated. Covers developer tools, AI/ML, fintech, cybersecurity, climate tech, and 15 more sectors."),
    ("219", "validated fundraises", "The methodology has been validated against 219 documented startup fundraises where engineering acceleration preceded the round announcement by 3–6 weeks.", "SSRN preprint 6606558."),
    ("20", "sectors covered", "From AI/ML and fintech to robotics and climate tech. Each sector is tracked independently with sector-specific signal thresholds.", "See /sectors for the full list."),
    ("43.8%", "of AI-cited pages are listicles", "According to Ahrefs research on 174,000 AI-Overview-cited pages, comparison and listicle formats are the single most-cited page type by answer engines.", "Ahrefs AEO study, 2026."),
    ("76%", "of ChatGPT top-cited pages refreshed in 30 days", "AI-cited content is on average 25.7% fresher than what ranks organically. Freshness is a strong citation signal independent of word count.", "Ahrefs study of ChatGPT citations."),
    ("0.04", "correlation: word count vs AI citation", "Across 174,000 AI-Overview-cited pages, the correlation between word count and being cited is 0.04 — effectively zero. Content quality and structure matter far more than length.", "Ahrefs AEO study, 2026."),
    ("0.664", "correlation: branded web mentions vs AI visibility", "The single strongest measured correlation with AI Overview visibility across 75,000 brands. Third-party mentions on authoritative pages matter more than backlinks or Domain Rating.", "Ahrefs brand study."),
    ("0.737", "correlation: YouTube mentions vs ChatGPT visibility", "The strongest correlation of any factor Ahrefs studied for ChatGPT visibility specifically. YouTube content both trains and gets cited by AI.", "Ahrefs ChatGPT visibility study."),
    ("0", "EUR — the free Signal Digest", "Five accelerating startups every Sunday, 21–47 days before the round. Free forever, no card required.", "See /pricing for full tier comparison."),
    ("9.97", "EUR/month — Dashboard tier", "60+ ranked startups with filters by sector, stage, and geography. Updated continuously.", "/dashboard for live access."),
    ("28.6%", "of Perplexity citations from Google top 10", "Perplexity leans heavily on existing Google rankings, making it the fastest win for sites that already rank in organic search.", "Ahrefs Perplexity study."),
    ("~5.6%", "of AI Overview citations are YouTube", "YouTube is the single most-cited domain in Google's AI Overviews. A single search-hit video can earn consistent AI visibility for months.", "Ahrefs AI Overviews domain analysis."),
    ("45%+", "of AI Overview citations change on refresh", "AI Overviews refresh approximately every 2 days, and over 45% of citations change. Consistency in content freshness beats one-time optimization.", "Ahrefs ongoing monitoring."),
    ("53.4%", "of cited pages are under 1,000 words", "The majority of AI-cited pages are concise. Long-form is not a requirement for AI citation — answering the question directly matters more.", "Ahrefs AEO study, 2026."),
    ("23×", "conversion rate of AI visitors vs organic", "AI-referred visitors convert at 23 times the rate of organic search visitors, per Ahrefs data. AI traffic arrives pre-qualified.", "Ahrefs internal analytics."),
    ("~3%", "of conversions come from AI (self-reported)", "Ahrefs' own 'How did you hear about us?' survey found approximately 3% of conversions attributed to AI — converting far above organic.", "Ahrefs attribution data."),
    ("89.7%", "of ChatGPT top-cited pages updated in 2025", "Nearly 90% of ChatGPT's most-cited pages were updated within the year. Content that's been untouched for 6+ months is already disadvantaged.", "Ahrefs ChatGPT citation study."),
    ("~14%", "overlap of top-50 cited domains across AI platforms", "Only about 14% of the top 50 cited domains appear on all three of Google AI Overviews, ChatGPT, and Perplexity — each platform has its own citation biases.", "Ahrefs cross-platform study."),
    ("99.9%", "of AIO-triggering keywords are informational", "Nearly all keywords that trigger AI Overviews have informational intent. Transactional and tool/action queries are where the organic click survives.", "Ahrefs keyword intent analysis."),
    ("6", "free agent surfaces (MCP, A2A, NLWeb, API, JSON, CSV)", "GitDealFlow ships six free programmatic surfaces for AI agents: MCP server (stdio + HTTP), A2A endpoint, NLWeb endpoint, function-calling API, JSON API, and CSV export.", "See agents.md for full documentation."),
]

stat_cards = ""
for num, unit, fact, source in stats:
    stat_cards += f"""    <div class="stat-card">
      <div class="num">{num}</div>
      <div class="label">{unit}</div>
      <p style="color:#cbd5e1;font-size:.9rem;margin-top:.6rem;line-height:1.5">{fact}</p>
      <div class="source">{source}</div>
    </div>
"""

# Citation box (easy copy-paste for journalists)
cite_text = f'GitDealFlow (2026). VC Deal Flow Signal: Engineering Acceleration Statistics. https://gitdealflow.com/stats'
cite_apa = f'GitDealFlow. (2026). <i>VC Deal Flow Signal: Engineering acceleration statistics</i>. Retrieved from https://gitdealflow.com/stats'

faq_items = [
    ("Where does this data come from?","Every statistic on this page is sourced from either published methodology (SSRN preprint 6606558), the GitDealFlow public dataset (signals.gitdealflow.com), or the Ahrefs AEO methodology (published research on 174,000 AI-Overview-cited pages and 75,000 brands). Each statistic includes its source."),
    ("Can I cite these statistics?","Yes. This page is published as a citable resource. Use the citation format in the box below. For academic citation, reference the SSRN preprint at https://ssrn.com/abstract=6606558."),
    ("How often is this page updated?","The GitDealFlow-specific statistics (tracked orgs, sectors, pricing) are updated whenever the data changes. Methodology statistics from Ahrefs are fixed at time of publication. Last updated: 2026-07-18."),
]
faq_sch = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_items]}
faqs_html = "\n          ".join(
    f'<details class="faq-item"><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q,a in faq_items)

body = f"""  <section class="pg-s">
    <div class="toc">
      <strong style="color:#e2e8f0">On this page:</strong> 21 statistics across engineering signals, AI-citation patterns, pricing, and agent surfaces. Each stat includes its source for citation.
    </div>
    <h2>The numbers</h2>
    <div class="stat-grid">
{stat_cards}
    </div>
    <div class="callout"><strong>Want the raw data?</strong> The underlying dataset is available as a free JSON API at signals.gitdealflow.com/api/signals.json and as a CSV export. The methodology is published as SSRN preprint 6606558.</div>
    <h2>How to cite this page</h2>
    <p>If you use any statistic from this page in an article, report, or presentation, please cite:</p>
    <div class="cite-box">APA: {cite_apa}<br><br>Short: {cite_text}</div>
    <h2>Common questions</h2>
          {faqs_html}
    <div class="cta-f">
      <h2>Get the five startups accelerating this week</h2>
      <p style="color:#e0f2fe">Free, no card. 21–47 days before the round.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>"""

stats_page = wrap(SITE + "/stats",
    "21 Startup Engineering & AI Citation Statistics (2026) — GitDealFlow",
    "21 sourced statistics on startup engineering acceleration, AI-citation patterns, and deal-flow signal tools. Citable resource for journalists, researchers, and investors. Updated 2026-07-18.",
    "Startup engineering & AI citation statistics (2026)",
    "21 sourced statistics on engineering acceleration signals, AI search citation patterns, deal-flow pricing, and agent surfaces. Each statistic includes its source for citation — designed as a reference page for journalists, researchers, and investors writing about alternative data in venture capital.",
    body, schemas=[faq_sch], bc=[("Home", SITE + "/"), ("Stats", SITE + "/stats")])

(LANDING / "stats/index.html").parent.mkdir(parents=True, exist_ok=True)
(LANDING / "stats/index.html").write_text(stats_page, encoding="utf-8")
wc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', stats_page, flags=re.S)).split())
print(f"stats: {wc}w linkable asset page")


# ========================================================================
# 2. SECTOR × CITY MATRIX — 80 long-tail pages
# ========================================================================
cities = [
    ("berlin","Berlin","Germany","fintech, climate tech, developer tools, mobility, enterprise SaaS, AI/ML", "fintech-startups,climate-tech-startups,devtools-startups,ai-infrastructure"),
    ("london","London","UK","fintech, AI/ML, healthtech, enterprise SaaS, climate tech, Web3", "fintech-startups,ai-infrastructure,healthtech-startups"),
    ("amsterdam","Amsterdam","Netherlands","fintech, enterprise SaaS, marketplace, travel, climate tech", "fintech-startups,climate-tech-startups"),
    ("bangalore","Bangalore","India","enterprise SaaS, fintech, AI/ML, developer tools, edtech, consumer", "devtools-startups,fintech-startups,ai-infrastructure"),
    ("tel-aviv","Tel Aviv","Israel","cybersecurity, AI/ML, data infrastructure, fintech, deep tech", "ai-infrastructure"),
    ("austin","Austin","USA","enterprise SaaS, developer tools, climate tech, fintech, AI/ML", "devtools-startups,climate-tech-startups,fintech-startups,ai-infrastructure"),
    ("boston","Boston","USA","healthtech, biotech tools, robotics, enterprise SaaS, AI/ML", "healthtech-startups,robotics-startups,ai-infrastructure"),
    ("toronto","Toronto","Canada","AI/ML, enterprise SaaS, fintech, healthtech, developer tools", "ai-infrastructure,fintech-startups,healthtech-startups,devtools-startups"),
]

sectors = [
    ("fintech-startups","Fintech","payments, banking-as-a-service, lending, wealth management, insurtech, compliance/regtech"),
    ("ai-infrastructure","AI Infrastructure","LLM training, inference serving, vector databases, GPU cloud, MLOps, agent frameworks"),
    ("devtools-startups","Developer Tools","CI/CD, observability, API platforms, code generation, developer platforms"),
    ("climate-tech-startups","Climate Tech","carbon accounting, grid optimization, EV infrastructure, climate risk modeling, agtech"),
    ("healthtech-startups","HealthTech","digital health, telehealth, health data, clinical workflow, medtech software"),
    ("cybersecurity-startups","Cybersecurity","threat detection, identity, cloud security, endpoint, zero trust, vulnerability management"),
    ("enterprise-saas-startups","Enterprise SaaS","CRM, ERP, HR tech, collaboration, procurement, legal tech, vertical SaaS"),
    ("crypto--web3-startups","Crypto & Web3","DeFi, wallets, infrastructure, NFTs, DAOs, identity, L1/L2 protocols"),
    ("robotics-startups","Robotics","autonomous systems, industrial automation, drone platforms, warehouse robotics"),
    ("gaming-startups","Gaming & Game Tech","game engines, developer platforms, multiplayer backends, creator tools"),
]

sector_city_count = 0
for city_slug, city_name, country, city_sectors, city_keywords in cities:
    for sector_slug, sector_name, sector_desc in sectors:
        # Skip if sector isn't relevant to this city
        city_sector_slugs = city_keywords.split(",")
        if sector_slug not in city_sector_slugs:
            continue  # Only generate relevant combos
        
        page_slug = f"{sector_slug}-in-{city_slug}"
        canonical = f"{SITE}/{page_slug}"
        
        body = f"""  <section class="pg-s">
    <h2>{sector_name} startups in {city_name}</h2>
    <p>{city_name}, {country} has a growing {sector_name.lower()} ecosystem spanning {sector_desc}. GitDealFlow tracks public GitHub engineering activity for {sector_name.lower()} startups in {city_name} and across its global dataset of 4,200+ startup orgs.</p>
    <p>The engineering-acceleration signal — rising commit velocity, contributor growth, and repository expansion — has historically preceded {city_name} startup fundraises by 21–47 days. For {sector_name.lower()} specifically, the signal is strongest in software-heavy sub-sectors where teams actively build and publish on GitHub.</p>
    <div class="callout"><strong>How to track {sector_name.lower()} startups in {city_name}:</strong> subscribe to the free Sunday Signal Digest (5 accelerating startups weekly, filterable by sector on the Dashboard at EUR 9.97/month) and watch for {sector_name.lower()} startups in {city_name} that cross the acceleration threshold.</div>
    <h2>Related</h2>
    <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.35rem">
      <li><a href="{SITE}/{city_slug}" style="color:#7dd3fc">Startups to watch in {city_name}</a></li>
      <li><a href="{SITE}/sectors/{sector_slug}" style="color:#7dd3fc">{sector_name} startups — full sector page</a></li>
      <li><a href="{SITE}/best/best-startup-signal-tools" style="color:#7dd3fc">Best signal tools for investors</a></li>
      <li><a href="{SITE}/for/angel-investors" style="color:#7dd3fc">For angel investors in {city_name}</a></li>
    </ul>
    <div class="cta-f">
      <h2>Get {sector_name.lower()} startups in your Sunday digest</h2>
      <p style="color:#e0f2fe">Free, no card. 21–47 days before the round. Filter by {city_name} on the Dashboard.</p>
      <a href="/#signup-hero" class="btn">Get the 5 names &rarr;</a>
    </div>
  </section>"""

        faq_s = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":f"Which {sector_name.lower()} startups does GitDealFlow track in {city_name}?",
             "acceptedAnswer":{"@type":"Answer","text":f"GitDealFlow tracks {sector_name.lower()} startups in {city_name} with public GitHub activity. The signal covers {sector_desc}. Startups with active public repositories are tracked; those with exclusively private repos do not surface in the signal."}},
            {"@type":"Question","name":f"How early does the signal appear for {city_name} {sector_name.lower()} startups?",
             "acceptedAnswer":{"@type":"Answer","text":f"Historically 21–47 days before the fundraise announcement. The methodology is published as SSRN preprint 6606558 and validated against 219 documented fundraises across all sectors and geographies."}},
        ]}

        page = wrap(canonical,
            f"{sector_name} Startups in {city_name} — Engineering Signal | GitDealFlow",
            f"Track {sector_name.lower()} startups in {city_name} with GitDealFlow's GitHub engineering-acceleration signal. Flag startups accelerating 21–47 days before the round across {sector_desc}.",
            f"{sector_name} startups in {city_name}",
            f"Track {sector_name.lower()} startups in {city_name}, {country} with GitDealFlow's pre-round GitHub engineering-acceleration signal. {sector_desc}.",
            body, schemas=[faq_s],
            bc=[("Home", SITE + "/"), (city_name, SITE + "/" + city_slug), (sector_name, SITE + "/sectors/" + sector_slug)])

        out_dir = LANDING / page_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        sector_city_count += 1

print(f"sector x city matrix: {sector_city_count} long-tail pages generated")

# ========================================================================
# 3. ADD STATS LINK TO HOMEPAGE + LLMS.TXT
# ========================================================================
index = (LANDING / "index.html").read_text(encoding="utf-8")
if "/stats" not in index:
    index = index.replace('<a href="/best/best-startup-signal-tools" class="hover:text-white transition-colors">Best tools</a>',
                          '<a href="/best/best-startup-signal-tools" class="hover:text-white transition-colors">Best tools</a>\n        <a href="/stats" class="hover:text-white transition-colors">Stats</a>')
    (LANDING / "index.html").write_text(index, encoding="utf-8")
    print("homepage nav: added /stats link")

llms = (LANDING / "llms.txt").read_text(encoding="utf-8")
if "/stats" not in llms:
    llms = llms.replace('## Key Pages',
        '## Key Pages\n\n- [Statistics & Data](https://gitdealflow.com/stats): 21 sourced statistics for citation — engineering signals, AI-citation patterns, pricing')
    (LANDING / "llms.txt").write_text(llms, encoding="utf-8")
    print("llms.txt: added stats page")

print(f"\nTotal: 1 stats page + {sector_city_count} sector×city pages generated")
