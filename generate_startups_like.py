#!/usr/bin/env python3
"""Generate startups-like-{slug}.html pages for every startup in the dataset."""
import json
import os
import re
import math

LANDING_DIR = os.path.expanduser("~/Downloads/gitdealflow/landing")
OUT_DIR = os.path.join(LANDING_DIR, "a")
JSON_PATH = "/tmp/signals.json"

os.makedirs(OUT_DIR, exist_ok=True)

with open(JSON_PATH) as f:
    data = json.load(f)

# Build lookup: startup_name -> dict
all_startups = {}
sector_map = {}  # startup_slug -> sector
for sector in data["sectors"]:
    for su in sector["startups"]:
        # Extract slug from profileUrl
        slug = su["profileUrl"].rsplit("/", 1)[-1] if su.get("profileUrl") else None
        if not slug:
            # Fallback: try github org name
            if su.get("githubUrl"):
                slug = su["githubUrl"].rstrip("/").split("/")[-1]
            else:
                slug = su["name"].lower().replace(" ", "-").replace("--", "-")
        su["_slug"] = slug
        su["_sector"] = sector
        all_startups[slug] = su
        sector_map[slug] = sector

print(f"Total startups: {len(all_startups)}")
print(f"Total sectors: {len(data['sectors'])}")

# Helper: format velocity change with color
def fmt_velocity_change(chg_str):
    """Return (label, style) for velocity change."""
    if not chg_str:
        return ("—", "color:#64748b")
    try:
        val = int(chg_str.replace("+", "").replace("%", ""))
    except (ValueError, AttributeError):
        return (chg_str, "color:#64748b")
    if val > 0:
        return (f"▲ +{val}%", "color:#4ade80")
    elif val < 0:
        return (f"▼ {val}%", "color:#f87171")
    else:
        return (f"▸ {val}%", "color:#64748b")

def fmt_contributor_growth(chg_str):
    if not chg_str:
        return "—"
    return chg_str

def make_safe(s):
    """Escape text for HTML."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")

def truncate_desc(desc, max_words=25):
    words = desc.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return desc

def get_geography_slug(geo):
    mapping = {
        "US": "united-states", "UK": "united-kingdom", "EU": "europe",
        "APAC": "apac", "LATAM": "latam", "Unknown": ""
    }
    return mapping.get(geo, geo.lower().replace(" ", "-") if geo else "")

def generate_page(slug, startup, sector_startups):
    """Generate HTML for one startups-like-{slug} page."""
    name = startup["name"]
    sector = startup["_sector"]
    sector_name = sector["name"]
    sector_slug = sector["slug"]
    desc = startup.get("description", "").strip()
    stage = startup.get("stage", "Unknown")
    geo = startup.get("geography", "Unknown")
    velocity = startup.get("commitVelocity14d", 0)
    vel_change = startup.get("commitVelocityChange", "")
    contributors = startup.get("contributors", 0)
    contr_growth = startup.get("contributorGrowth", "")
    signal_type = startup.get("signalType", "")
    github_url = startup.get("githubUrl", "")
    website_url = startup.get("websiteUrl", "")

    if desc:
        desc_snippet = truncate_desc(desc, 20)
    else:
        desc_snippet = f"a {sector_name} startup"

    # Sort sector startups by velocity descending
    sorted_startups = sorted(sector_startups, key=lambda x: x.get("commitVelocity14d", 0), reverse=True)

    # Compute sector average velocity
    sector_velocities = [s.get("commitVelocity14d", 0) for s in sector_startups]
    avg_velocity = sum(sector_velocities) / len(sector_velocities) if sector_velocities else 0
    rank = next((i+1 for i, s in enumerate(sorted_startups) if s["_slug"] == slug), 0)

    # Page info
    display_name = make_safe(name)
    sector_name_safe = make_safe(sector_name)
    sector_startup_count = len(sector_startups)
    desc_snippet_safe = make_safe(desc_snippet)

    title = f"{display_name} Competitors — Similar Startups Like {display_name} (2026) | GitDealFlow"
    meta_desc = f"Find startups like {display_name}. Compare {display_name}'s engineering velocity against {sector_startup_count} similar {sector_name_safe} startups. Free GitHub-based signals."
    canonical = f"https://gitdealflow.com/a/startups-like-{slug}"

    # Build comparison table rows
    table_rows = ""
    for i, s in enumerate(sorted_startups):
        s_slug = s["_slug"]
        s_name = make_safe(s["name"])
        s_stage = s.get("stage", "—")
        s_geo = s.get("geography", "—")
        s_vel = s.get("commitVelocity14d", 0)
        s_vel_chg_label, s_vel_chg_style = fmt_velocity_change(s.get("commitVelocityChange", ""))
        s_signal = s.get("signalType", "—")

        table_rows += f"""<div class="row"><span class="r">{i+1}</span><a href="/startups/{s_slug}" class="n">{s_name}</a><span class="s">{s_stage}</span><span class="v">{s_vel}</span><span class="g" style="{s_vel_chg_style}">{s_vel_chg_label}</span><span class="sig">{make_safe(s_signal)}</span></div>\n"""

    # How "X" compares section
    if velocity >= avg_velocity:
        comparison_text = f"{display_name} is shipping <strong>above the {sector_name_safe} sector average</strong> of {avg_velocity:.0f} commits/14d, ranking #{rank} out of {sector_startup_count} startups in the sector."
    else:
        comparison_text = f"{display_name} ships at <strong>{velocity} commits/14d</strong>, which is below the {sector_name_safe} sector average of {avg_velocity:.0f} commits/14d. It ranks #{rank} out of {sector_startup_count} startups."

    # Build sector startup links
    sector_links = ""
    for s in sorted_startups[:15]:
        s_slug = s["_slug"]
        s_name = make_safe(s["name"])
        sector_links += f"""<a href="/startups/{s_slug}" class="sector-link">{s_name}</a>\n"""

    # Build related competitive set pages (other startups in same sector)
    related_pages = ""
    related = [s for s in sorted_startups if s["_slug"] != slug][:10]
    for s in related:
        s_slug = s["_slug"]
        s_name = make_safe(s["name"])
        related_pages += f"""<a href="/a/startups-like-{s_slug}" class="related-link">{s_name}</a>\n"""

    # Build FAQ based on startup
    faq_q1 = f"What are the best alternatives to {display_name}?"
    faq_a1 = f"Based on engineering velocity data from GitDealFlow Q3 2026, the top comparable startups in the {sector_name_safe} space include {', '.join(make_safe(s['name']) for s in sorted_startups[:5])} and others ranked by commit velocity and engineering team growth."

    faq_q2 = f"How does {display_name} compare to other {sector_name_safe} startups on engineering velocity?"
    faq_a2 = f"{display_name} ranks #{rank} out of {sector_startup_count} startups in the {sector_name_safe} sector with {velocity} commits in the last 14 days. The sector average is {avg_velocity:.0f} commits/14d."

    faq_q3 = f"How does GitDealFlow track engineering velocity for startups like {display_name}?"
    faq_a3 = "We analyze public GitHub activity across all startups in our dataset. Metrics include 14-day commit velocity, velocity change percentage, contributor count and growth, and signal type classification (e.g., deploy frequency spike, engineering hiring burst, framework migration, infrastructure buildout)."

    # Geography filter URL
    geo_slug = get_geography_slug(geo) if geo else ""
    geo_url = f"/locations/{geo_slug}" if geo_slug else ""

    # Build the HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://gitdealflow.com/opengraph-image.png">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@data_nerd">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="news_keywords" content="{display_name} competitors, startups like {display_name}, {sector_name_safe}, engineering velocity, GitDealFlow" />
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{title}","description":"{meta_desc}","url":"{canonical}"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://gitdealflow.com/"}},{{"@type":"ListItem","position":2,"name":"Startups Like {display_name}","item":"{canonical}"}}]}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{{"@type":"Question","name":"{faq_q1}","acceptedAnswer":{{"@type":"Answer","text":"{faq_a1}"}}}},
{{"@type":"Question","name":"{faq_q2}","acceptedAnswer":{{"@type":"Answer","text":"{faq_a2}"}}}},
{{"@type":"Question","name":"{faq_q3}","acceptedAnswer":{{"@type":"Answer","text":"{faq_a3}"}}}}
]}}
</script>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0b1120;color:#e8eaed;line-height:1.6;margin:0;padding:0}}
a{{color:#60a5fa}}
.container{{max-width:720px;margin:0 auto;padding:1.5rem}}
header{{text-align:center;padding:2rem 1.5rem;border-bottom:1px solid #1e293b}}
header h1{{font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#60a5fa,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;margin:0}}
header p{{color:#94a3b8;font-size:.85rem;margin-top:.5rem}}
.row{{display:grid;grid-template-columns:24px 1fr 90px 60px 85px 110px;gap:.25rem;align-items:center;padding:.35rem 0;border-bottom:1px solid #1e293b;font-size:.75rem}}
.r{{color:#475569}}
.n{{color:#f1f5f9;font-weight:500;text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.s{{color:#64748b;font-size:.7rem}}
.v{{font-weight:700;text-align:right;color:#60a5fa}}
.g{{text-align:right;font-size:.65rem}}
.sig{{color:#64748b;font-size:.65rem;text-align:right}}
.sig::before{{content:"[";color:#475569}}
.sig::after{{content:"]";color:#475569}}
h2{{color:#e2e8f0;font-size:1.1rem;margin-top:2rem;border-left:3px solid #60a5fa;padding-left:.75rem}}
h3{{color:#94a3b8;font-size:.95rem;margin-top:1.5rem}}
.faq-item{{border-bottom:1px solid #1e293b;padding:1rem 0}}
.faq-q{{color:#e2e8f0;font-weight:600;font-size:.9rem;margin-bottom:.3rem}}
.faq-a{{color:#94a3b8;font-size:.8rem;line-height:1.5}}
.why-section{{background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:1.25rem;margin:1.5rem 0}}
.why-section p{{color:#94a3b8;font-size:.85rem;margin:.5rem 0}}
.why-section h3{{color:#e2e8f0;font-size:1rem;margin-top:0;margin-bottom:.5rem}}
.footer-links{{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem}}
.footer-links a{{color:#475569;font-size:.75rem;text-decoration:none}}
.portfolio{{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid #1e293b;text-align:center}}
.portfolio h4{{color:#64748b;font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.75rem}}
.portfolio-links{{display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap}}
.portfolio-links a{{color:#475569;font-size:.75rem;text-decoration:none}}
.sector-link{{display:inline-block;padding:.25rem .5rem;margin:.15rem;background:#0f172a;border:1px solid #1e293b;border-radius:4px;color:#60a5fa;font-size:.75rem;text-decoration:none;transition:border-color .2s}}
.sector-link:hover{{border-color:#60a5fa}}
.related-link{{display:inline-block;padding:.2rem .4rem;margin:.1rem;color:#94a3b8;font-size:.75rem;text-decoration:none;transition:color .2s}}
.related-link:hover{{color:#60a5fa}}
.compared{{background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:1.25rem;margin:1.5rem 0}}
.compared p{{color:#94a3b8;font-size:.85rem;margin:.5rem 0}}
.compared strong{{color:#e2e8f0}}
.section-label{{font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:#475569;margin-top:1rem;margin-bottom:.5rem}}
.breadcrumb{{font-size:.75rem;color:#475569;padding:1rem 0;margin-bottom:0}}
.breadcrumb a{{color:#64748b;text-decoration:none}}
.breadcrumb a:hover{{color:#60a5fa}}
@media (max-width:640px){{.row{{grid-template-columns:20px 1fr 65px 50px 70px 80px;font-size:.7rem;gap:.15rem}}.container{{padding:1rem}}}}
</style>
</head>
<body>
<div class="container breadcrumb">
<a href="/">Home</a> › <a href="/startups">Startups</a> › <span style="color:#64748b">Startups Like {display_name}</span>
</div>
<header>
<h1>Startups Like {display_name}</h1>
<p>{sector_name_safe} sector engineering velocity rankings — Q3 2026</p>
</header>
<main class="container">

<div class="why-section">
<h3>About {display_name}</h3>
<p>{display_name} is {desc_snippet_safe}. This page shows similar startups in the <strong>{sector_name_safe}</strong> sector based on engineering velocity, team growth, and development patterns tracked by GitDealFlow.</p>
</div>

<div class="section-label">Top {sector_startup_count} {sector_name_safe} Startups Ranked by Commit Velocity</div>
<div class="row" style="border-bottom:2px solid #1e293b;font-size:.7rem;color:#64748b;text-transform:uppercase;letter-spacing:.05em;padding-bottom:.5rem">
<span class="r">#</span><span>Name</span><span>Stage</span><span style="text-align:right">14d Cmt</span><span style="text-align:right">Chg</span><span style="text-align:right">Signal</span>
</div>
{table_rows}

<div class="compared">
<h3>How {display_name} Compares</h3>
<p>{comparison_text}</p>
<p>{display_name} has <strong>{contributors} contributors</strong> (growth: {fmt_contributor_growth(contr_growth)}) and a signal type of <strong>{make_safe(signal_type)}</strong>.</p>
</div>

<div class="section-label">Other {sector_name_safe} Startups</div>
<div class="sector-links">
{sector_links}
</div>

<h2>Related Competitive Set Pages</h2>
<div class="related-links">
{related_pages}
</div>

<h2>Frequently Asked Questions</h2>
<div class="faq-item">
<div class="faq-q">{faq_q1}</div>
<div class="faq-a">{faq_a1}</div>
</div>
<div class="faq-item">
<div class="faq-q">{faq_q2}</div>
<div class="faq-a">{faq_a2}</div>
</div>
<div class="faq-item">
<div class="faq-q">{faq_q3}</div>
<div class="faq-a">{faq_a3}</div>
</div>

<p style="color:#475569;font-size:.7rem;margin-top:1.5rem">
<a href="/sectors/{sector_slug}">All {sector_name_safe} startups</a> &middot;
<a href="/sectors">All sectors</a> &middot;
<a href="/startups">All startups</a> &middot;
<a href="/signal">Signals</a>
</p>
</main>

<footer style="border-top:1px solid #1e293b;padding:2rem;text-align:center;color:#64748b;font-size:.8rem">
<div class="footer-links">
<a href="https://gitdealflow.com">GitDealFlow</a> &middot;
<a href="https://signals.gitdealflow.com">Signals</a> &middot;
<a href="/trending-this-week">Trending</a> &middot;
<a href="/scout-leaderboard">Scout Leaderboard</a> &middot;
<a href="/high-velocity-startups">High Velocity</a> &middot;
<a href="/startups">All Startups</a>
</div>
<div class="portfolio">
<h4>Network</h4>
<div class="portfolio-links">
<a href="https://signals.gitdealflow.com">Signals Dataset</a>
<a href="https://sipi.bot">Sipi.bot</a>
<a href="https://churnlens.site">ChurnLens</a>
<a href="https://carshake.online">CarShake</a>
<a href="https://unlocksaas.com">UnlockSaaS</a>
<a href="https://sanctionsai.dev">SanctionsAI</a>
<a href="https://voicelogpro.com">VoiceLogPro</a>
<a href="https://invisibleexit.com">InvisibleExit</a>
<a href="https://sipiteno.com">Sipiteno</a>
</div>
</div>
</footer>
</body>
</html>"""
    return html

# Generate all pages
generated = 0
errors = []
for slug, startup in all_startups.items():
    sector = startup["_sector"]
    sector_startups = sector["startups"]
    try:
        html = generate_page(slug, startup, sector_startups)
        filepath = os.path.join(OUT_DIR, f"startups-like-{slug}.html")
        with open(filepath, "w") as f:
            f.write(html)
        generated += 1
        if generated % 50 == 0:
            print(f"  Generated {generated}...")
    except Exception as e:
        errors.append((slug, str(e)))
        print(f"  ERROR generating {slug}: {e}")

print(f"\nDone! Generated {generated} pages in {OUT_DIR}")
print(f"Errors: {len(errors)}")
for slug, err in errors[:10]:
    print(f"  {slug}: {err}")

# Verify
import glob
files = glob.glob(os.path.join(OUT_DIR, "startups-like-*.html"))
print(f"\nFiles on disk: {len(files)}")
assert len(files) == generated, f"File count mismatch: {len(files)} != {generated}"
print("✓ All files verified")
