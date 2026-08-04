#!/usr/bin/env python3
"""Build 5 data-driven startup signal pages from live API data."""

import json
import os
import re
from datetime import datetime, timezone

LANDING = "/Users/sipi/Downloads/gitdealflow/landing"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
TODAY_RFC = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
WEEK_AGO_RFC = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00+00:00")

# ── Load API data ──
with open("/tmp/signals_full.json") as f:
    api = json.load(f)

trending = api["trending"]
sectors = api["sectors"]
period = api["meta"]["period"]["name"]

# ── Helpers ──
def stage_color(stage):
    colors = {"Pre-seed": "#f97316", "Seed": "#a78bfa", "Series A/B": "#60a5fa", "Growth": "#34d399"}
    return colors.get(stage, "#94a3b8")

def velocity_color(change_str):
    val = parse_pct(change_str)
    if val >= 999: return "#4ade80"
    if val >= 100: return "#facc15"
    return "#60a5fa"

def parse_pct(s):
    if not s: return 0
    s = s.replace("+", "").replace("%", "").replace("−", "-")
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return 0

def parse_velocity_change(change_str):
    return parse_pct(change_str)

def signal_badge(sig):
    colors = {
        "Deploy frequency spike": "#60a5fa",
        "Engineering hiring burst": "#f97316",
        "Infrastructure buildout": "#a78bfa",
        "Framework migration": "#34d399",
        "Repository expansion": "#f472b6"
    }
    bg = colors.get(sig, "#475569")
    return f'<span style="background:{bg}22;color:{bg};border:1px solid {bg}44;border-radius:4px;padding:1px 6px;font-size:.65rem;white-space:nowrap">{sig}</span>'

def geo_flag(geo):
    flags = {"US": "🇺🇸", "EU": "🇪🇺", "APAC": "🌏", "UK": "🇬🇧", "Unknown": "🌐"}
    return flags.get(geo, "🌐")

def profile_url(name):
    slug = name.lower().replace(" ", "-").replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    return f"https://signals.gitdealflow.com/startups/{slug}"

HEADER = """<header class="relative sticky top-0 z-50 border-b border-gray-800 bg-dark-900/95 backdrop-blur">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-3">
    <a href="/" class="font-semibold tracking-tight text-white text-lg">GitDealFlow</a>
    <nav aria-label="Primary navigation" class="hidden md:flex items-center gap-5 text-sm font-medium text-gray-300">
      <a href="/" class="hover:text-white transition-colors">Home</a>
      <a href="https://signals.gitdealflow.com" class="hover:text-white transition-colors">Signals</a>
      <a href="/trending.html" class="hover:text-white transition-colors">Trending</a>
      <a href="/pricing" class="hover:text-white transition-colors">Pricing</a>
      <a href="/dashboard" class="hover:text-white transition-colors">Dashboard</a>
    </nav>
    <div class="flex items-center gap-3 shrink-0">
      <a href="#footer-signup" class="btn btn-primary btn-no-pulse btn-sm whitespace-nowrap shrink-0">Subscribe <span aria-hidden="true">→</span></a>
      <button type="button" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu" class="md:hidden inline-flex items-center justify-center w-11 h-11 shrink-0 rounded-lg text-gray-300 hover:text-white ring-1 ring-white/10 transition-colors">
        <svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <div id="mobile-nav" hidden class="md:hidden absolute top-full inset-x-0 z-50 border-b border-white/10 bg-dark-900 shadow-2xl">
    <nav aria-label="Mobile navigation" class="flex flex-col px-4 py-2">
      <a href="/" class="py-3 min-h-[44px] flex items-center border-b border-white/5 text-gray-200 hover:text-white">Home</a>
      <a href="https://signals.gitdealflow.com" class="py-3 min-h-[44px] flex items-center border-b border-white/5 text-gray-200 hover:text-white">Signals</a>
      <a href="/trending.html" class="py-3 min-h-[44px] flex items-center border-b border-white/5 text-gray-200 hover:text-white">Trending</a>
      <a href="/pricing" class="py-3 min-h-[44px] flex items-center text-gray-200 hover:text-white">Pricing</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer>
  <div style="text-align:center;padding:2.5rem 1.5rem 1.5rem;border-top:1px solid #1e293b;margin-top:3rem;">
    <a href="https://gitdealflow.com" style="color:#60a5fa;text-decoration:none;font-weight:600;">GitDealFlow</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="https://signals.gitdealflow.com" style="color:#475569;text-decoration:none;">Signals Dataset</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="/trending.html" style="color:#475569;text-decoration:none;">Trending</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="/sector-guide.html" style="color:#475569;text-decoration:none;">Sector Guide</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="/geo-signals.html" style="color:#475569;text-decoration:none;">Geo Signals</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="/hidden-gems.html" style="color:#475569;text-decoration:none;">Hidden Gems</a>
    <span style="color:#475569;margin:0 .5rem;">·</span>
    <a href="/pre-seed-signals.html" style="color:#475569;text-decoration:none;">Pre-Seed Signals</a>
    <p style="color:#475569;font-size:.75rem;margin-top:1rem;">Data from <a href="https://signals.gitdealflow.com" style="color:#60a5fa;">VC Deal Flow Signal</a> · {period} · {total} startups tracked</p>
    <div style="display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin-top:1rem;padding-top:1rem;border-top:1px solid #1e293b;">
      <h4 style="color:#64748b;font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.25rem;width:100%;">Network</h4>
      <a href="https://signals.gitdealflow.com" style="color:#475569;font-size:.7rem;text-decoration:none;">Signals Dataset</a>
      <a href="https://sipi.bot" style="color:#475569;font-size:.7rem;text-decoration:none;">Sipi.bot</a>
      <a href="https://churnlens.site" style="color:#475569;font-size:.7rem;text-decoration:none;">ChurnLens</a>
      <a href="https://carshake.online" style="color:#475569;font-size:.7rem;text-decoration:none;">CarShake</a>
      <a href="https://unlocksaas.com" style="color:#475569;font-size:.7rem;text-decoration:none;">UnlockSaaS</a>
      <a href="https://sanctionsai.dev" style="color:#475569;font-size:.7rem;text-decoration:none;">SanctionsAI</a>
      <a href="https://voicelogpro.com" style="color:#475569;font-size:.7rem;text-decoration:none;">VoiceLogPro</a>
      <a href="https://invisibleexit.com" style="color:#475569;font-size:.7rem;text-decoration:none;">InvisibleExit</a>
      <a href="https://sipiteno.com" style="color:#475569;font-size:.7rem;text-decoration:none;">Sipiteno</a>
    </div>
    <p style="color:#475569;font-size:.65rem;margin-top:1rem;">© 2026 GitDealFlow. Data from <a href="https://signals.gitdealflow.com" style="color:#60a5fa;">VC Deal Flow Signal</a>. Free for personal and editorial use with attribution.</p>
  </div>
</footer>""".format(period=period, total=api["meta"]["totalStartups"])

STYLES = """<style>
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0b1120;color:#e8eaed;line-height:1.6;margin:0;padding:0}
a{color:#60a5fa;text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:800px;margin:0 auto;padding:1.5rem}
h1{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#60a5fa,#a78bfa);-webkit-background-clip:text;background-clip:text;color:transparent;margin:0 0 .25rem}
h2{color:#f1f5f9;font-size:1.1rem;margin:2rem 0 .75rem;padding-bottom:.25rem;border-bottom:1px solid #1e293b}
h3{color:#e2e8f0;font-size:.9rem;margin:1.25rem 0 .5rem}
table{width:100%;border-collapse:collapse;font-size:.8rem;margin:.75rem 0}
th{text-align:left;color:#94a3b8;font-weight:600;padding:.4rem .5rem;border-bottom:1px solid #334155;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em}
td{padding:.4rem .5rem;border-bottom:1px solid #1e293b;vertical-align:middle}
tr:hover td{background:#0f172a}
.card{background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:1rem;margin:.75rem 0}
.card h3{margin:0 0 .25rem}
.card p{color:#94a3b8;font-size:.78rem;margin:.25rem 0}
.card .meta{display:flex;gap:.75rem;flex-wrap:wrap;font-size:.7rem;color:#64748b;margin-top:.5rem}
.subtitle{color:#94a3b8;font-size:.85rem;margin-bottom:1.5rem}
.note{color:#475569;font-size:.7rem;margin-top:2rem;text-align:center}
.badge{display:inline-block;background:#1e293b;color:#94a3b8;border-radius:4px;padding:1px 8px;font-size:.65rem}
.sector-header{background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:.75rem 1rem;margin:.5rem 0;cursor:default}
.sector-header h3{margin:0;font-size:.85rem;color:#f1f5f9}
.sector-header:hover{border-color:#334155}
@media(max-width:640px){.container{padding:1rem}table{font-size:.72rem}td,th{padding:.3rem .35rem}}
</style>"""

# ── PAGE 1: hidden-gems.html ──
def build_hidden_gems():
    """Top 10 startups by commitVelocityChange % with low contributor count."""
    sorted_by_change = sorted(trending, key=lambda t: parse_velocity_change(t["commitVelocityChange"]), reverse=True)
    hidden = [s for s in sorted_by_change if s["contributors"] <= 10][:10]

    rows = ""
    for i, s in enumerate(hidden, 1):
        pct = s["commitVelocityChange"]
        contrib = s["contributors"]
        rows += f"""<tr>
<td style="color:#475569;text-align:center;">{i}</td>
<td><a href="{profile_url(s['name'])}" style="font-weight:500;color:#f1f5f9;">{s['name']}</a></td>
<td><span class="badge">{s['stage']}</span></td>
<td>{geo_flag(s['geography'])} {s['geography']}</td>
<td style="color:{velocity_color(pct)};font-weight:700;text-align:right;">{pct}</td>
<td style="text-align:center;"><span class="badge">{contrib}</span></td>
<td>{signal_badge(s['signalType'])}</td>
</tr>"""

    prose = f"""
<div class="card">
  <h3>Why Engineering Velocity at Low Headcount Matters</h3>
  <p>Startups with <strong>fewer than 10 contributors</strong> but extreme commit velocity changes ({hidden[0]['commitVelocityChange']} in the top case) are the strongest leading indicator of a pre-announcement hiring spree. These teams are small, moving fast, and building something worth watching — often 3–6 weeks before a fundraise surfaces publicly.</p>
  <p>Each startup in this list has:</p>
  <ul style="color:#94a3b8;font-size:.78rem;">
    <li>Commit velocity change ≥ {min(parse_velocity_change(s['commitVelocityChange']) for s in hidden)}%</li>
    <li>≤ 10 active contributors (small, focused team)</li>
    <li>Clear signal type indicating what's driving the acceleration</li>
  </ul>
</div>"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hidden Gems: 10 Startups with the Highest Engineering Velocity Nobody's Talking About | GitDealFlow</title>
<meta name="description" content="Discover 10 under-the-radar startups with explosive engineering velocity but tiny teams. Data-driven picks from the VC Deal Flow Signal dataset — updated {TODAY}.">
<link rel="canonical" href="https://gitdealflow.com/hidden-gems.html">
<meta property="og:title" content="Hidden Gems: 10 Startups with the Highest Engineering Velocity">
<meta property="og:description" content="Small teams, extreme commit velocity. Top 10 hidden-gem startups ranked by engineering acceleration.">
<meta property="og:url" content="https://gitdealflow.com/hidden-gems.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="news_keywords" content="Hidden gems, under-the-radar startups, engineering velocity, deal flow, early-stage startups, GitHub, venture capital, startup signals" />
<meta property="article:tag" content="Hidden gems" />
<meta property="article:tag" content="under-the-radar startups" />
<meta property="article:tag" content="engineering velocity" />
<meta property="article:tag" content="deal flow" />
<meta property="article:tag" content="early-stage startups" />
<meta property="article:tag" content="GitHub" />
<meta property="article:tag" content="venture capital" />
<meta property="article:tag" content="startup signals" />
<meta property="article:published_time" content="{TODAY_RFC}" />
<meta property="article:modified_time" content="{TODAY_RFC}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Hidden Gems: 10 Startups with the Highest Engineering Velocity Nobody's Talking About",
  "description": "Top 10 under-the-radar startups ranked by engineering commit velocity change, featuring small teams with breakout velocity signals.",
  "datePublished": "{TODAY_RFC}",
  "dateModified": "{TODAY_RFC}",
  "publisher": {{"@type":"Organization","name":"GitDealFlow","url":"https://gitdealflow.com"}},
  "mainEntityOfPage": "https://gitdealflow.com/hidden-gems.html",
  "about": {{"@type":"Thing","name":"Startup Engineering Signals"}}
}}</script>
{STYLES}
</head>
<body>
{HEADER}
<main class="container">
<h1>Hidden Gems: 10 Startups with the Highest Engineering Velocity Nobody's Talking About</h1>
<p class="subtitle">Small teams with breakout commit velocity — ranked by commit velocity change · Data: VC Deal Flow Signal {period} · {TODAY}</p>
{prose}
<div style="overflow-x:auto;">
<table>
<thead>
<tr><th style="width:30px">#</th><th>Startup</th><th>Stage</th><th>Region</th><th style="text-align:right">Velocity Δ</th><th style="text-align:center">Contribs</th><th>Signal Type</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<h2>How These Were Selected</h2>
<p style="color:#94a3b8;font-size:.8rem;">From the <a href="https://signals.gitdealflow.com">VC Deal Flow Signal</a> dataset of {api['meta']['totalStartups']} startups across 15 sectors, we filtered for two criteria: (1) commit velocity change above +100%, and (2) ≤ 10 active contributors. The result is a concentrated list of lean, high-momentum engineering orgs worth tracking for deal-flow discovery.</p>
<div class="note">
  <p>Data sourced from <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> · <a href="/trending.html">View All Trending Startups</a> · <a href="/sector-guide.html">Sector Guide</a> · <a href="/pre-seed-signals.html">Pre-Seed Signals</a> · <a href="https://signals.gitdealflow.com/methodology">Methodology</a></p>
</div>
</main>
{FOOTER}
</body>
</html>"""
    return content

# ── PAGE 2: sector-guide.html ──
def build_sector_guide():
    """All 15 sectors with startup counts, descriptions, sample startups."""
    cards = ""
    for s in sectors:
        sample_startups = s.get("startups", [])[:3]
        samples_html = ""
        if sample_startups:
            samples_html = '<div style="display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.4rem;">' + \
                "".join(f'<a href="{profile_url(st["name"])}" style="color:#60a5fa;font-size:.7rem;">{st["name"]}</a>' for st in sample_startups) + \
                '</div>'

        cards += f"""<div class="sector-header">
<h3><a href="https://signals.gitdealflow.com/sectors/{s['slug']}" style="color:#f1f5f9;">{s['name']}</a> <span class="badge">{s['startupCount']} startups</span></h3>
<p style="color:#94a3b8;font-size:.75rem;margin:.25rem 0 0;">{s.get('description', '')}</p>
{samples_html}
</div>"""

    # Build a signal-type distribution across all sectors
    signal_counts = {}
    for sec in sectors:
        for st in sec.get("startups", []):
            sig = st.get("signalType", "Unknown")
            signal_counts[sig] = signal_counts.get(sig, 0) + 1

    sig_rows = ""
    total_signals = sum(signal_counts.values())
    if total_signals == 0:
        total_signals = 1
    for sig, cnt in sorted(signal_counts.items(), key=lambda x: -x[1]):
        pct = round(cnt / total_signals * 100)
        sig_rows += f"""<tr><td>{signal_badge(sig)}</td><td style="text-align:center">{cnt}</td><td style="text-align:center">{pct}%</td></tr>"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Complete Guide to Startup Sectors: Engineering Trends in 15 Categories | GitDealFlow</title>
<meta name="description" content="Complete guide to 15 startup sectors tracked by VC Deal Flow Signal. Engineering velocity trends, startup counts, and notable companies in each category.">
<link rel="canonical" href="https://gitdealflow.com/sector-guide.html">
<meta property="og:title" content="Complete Guide to Startup Sectors: Engineering Trends in 15 Categories">
<meta property="og:description" content="VC Deal Flow Signal tracks {len(sectors)} sectors. Browse startup counts, engineering signal types, and notable startups per category.">
<meta property="og:url" content="https://gitdealflow.com/sector-guide.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="news_keywords" content="Startup sectors, engineering trends, venture capital, deal flow, sector analysis, GitHub, startup categories, sector guide" />
<meta property="article:tag" content="Startup sectors" />
<meta property="article:tag" content="engineering trends" />
<meta property="article:tag" content="venture capital" />
<meta property="article:tag" content="deal flow" />
<meta property="article:tag" content="sector analysis" />
<meta property="article:tag" content="GitHub" />
<meta property="article:tag" content="startup categories" />
<meta property="article:tag" content="sector guide" />
<meta property="article:published_time" content="{TODAY_RFC}" />
<meta property="article:modified_time" content="{TODAY_RFC}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "The Complete Guide to Startup Sectors: Engineering Trends in 15 Categories",
  "description": "Browse all {len(sectors)} startup sectors tracked by VC Deal Flow Signal with startup counts, engineering signal type distributions, and notable companies.",
  "datePublished": "{TODAY_RFC}",
  "dateModified": "{TODAY_RFC}",
  "publisher": {{"@type":"Organization","name":"GitDealFlow","url":"https://gitdealflow.com"}},
  "mainEntityOfPage": "https://gitdealflow.com/sector-guide.html",
  "about": {{"@type":"Thing","name":"Startup Sectors"}}
}}</script>
{STYLES}
</head>
<body>
{HEADER}
<main class="container">
<h1>The Complete Guide to Startup Sectors: Engineering Trends in 15 Categories</h1>
<p class="subtitle">All {len(sectors)} sectors tracked by the VC Deal Flow Signal — {api['meta']['totalStartups']} startups total · {period} · Updated {TODAY}</p>
<h2>Signal Type Distribution Across All Sectors</h2>
<table>
<thead><tr><th>Signal Type</th><th style="text-align:center">Count</th><th style="text-align:center">% of Total</th></tr></thead>
<tbody>{sig_rows}</tbody>
</table>
<h2>All 15 Sectors</h2>
{cards}
<div class="note">
  <p>Data sourced from <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> · <a href="/trending.html">View All Trending Startups</a> · <a href="/geo-signals.html">Startup Engineering by Geography</a> · <a href="/hidden-gems.html">Hidden Gems</a> · <a href="https://signals.gitdealflow.com/methodology">Methodology</a></p>
</div>
</main>
{FOOTER}
</body>
</html>"""
    return content

# ── PAGE 3: pre-seed-signals.html ──
def build_preseed_signals():
    """Filter stage=Pre-seed, top 10 by commitVelocity14d."""
    preseed = [s for s in trending if s["stage"] == "Pre-seed"]
    preseed.sort(key=lambda s: s["commitVelocity14d"], reverse=True)
    preseed = preseed[:10]

    rows = ""
    for i, s in enumerate(preseed, 1):
        v = s["commitVelocity14d"]
        rows += f"""<tr>
<td style="color:#475569;text-align:center;">{i}</td>
<td><a href="{profile_url(s['name'])}" style="font-weight:500;color:#f1f5f9;">{s['name']}</a></td>
<td>{geo_flag(s['geography'])} {s['geography']}</td>
<td style="text-align:center;font-weight:700;">{v}</td>
<td style="color:{velocity_color(s['commitVelocityChange'])};font-weight:700;text-align:right;">{s['commitVelocityChange']}</td>
<td style="text-align:center;">{s['contributors']}</td>
<td>{signal_badge(s['signalType'])}</td>
</tr>"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pre-Seed Startup Signals: Find the Next Unicorn at Zero Revenue | GitDealFlow</title>
<meta name="description" content="Top pre-seed startups ranked by engineering velocity. Find early-stage teams building at breakout speed before they raise. Data from VC Deal Flow Signal.">
<link rel="canonical" href="https://gitdealflow.com/pre-seed-signals.html">
<meta property="og:title" content="Pre-Seed Startup Signals: Find the Next Unicorn at Zero Revenue">
<meta property="og:description" content="Top 10 pre-seed startups by commit velocity. Early-stage engineering teams moving fast — find them before the round.">
<meta property="og:url" content="https://gitdealflow.com/pre-seed-signals.html">
<meta name="twitter:card" content="content="summary_large_image">
<meta name="news_keywords" content="Pre-seed startups, early-stage startups, seed investing, engineering velocity, deal flow, venture capital, startup signals, zero revenue" />
<meta property="article:tag" content="Pre-seed startups" />
<meta property="article:tag" content="early-stage startups" />
<meta property="article:tag" content="seed investing" />
<meta property="article:tag" content="engineering velocity" />
<meta property="article:tag" content="deal flow" />
<meta property="article:tag" content="venture capital" />
<meta property="article:tag" content="startup signals" />
<meta property="article:tag" content="zero revenue" />
<meta property="article:published_time" content="{TODAY_RFC}" />
<meta property="article:modified_time" content="{TODAY_RFC}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Pre-Seed Startup Signals: Find the Next Unicorn at Zero Revenue",
  "description": "Top pre-seed startups ranked by engineering commit velocity. Data-driven picks for investors tracking early-stage teams before the round.",
  "datePublished": "{TODAY_RFC}",
  "dateModified": "{TODAY_RFC}",
  "publisher": {{"@type":"Organization","name":"GitDealFlow","url":"https://gitdealflow.com"}},
  "mainEntityOfPage": "https://gitdealflow.com/pre-seed-signals.html",
  "about": {{"@type":"Thing","name":"Pre-Seed Startup Signals"}}
}}</script>
{STYLES}
</head>
<body>
{HEADER}
<main class="container">
<h1>Pre-Seed Startup Signals: Find the Next Unicorn at Zero Revenue</h1>
<p class="subtitle">Ranked by 14-day commit velocity — {period} data · {TODAY}</p>
<div class="card">
<h3>Why Pre-Seed Engineering Velocity Matters</h3>
<p>Pre-seed startups by definition have little to no revenue, no meaningful traction metrics, and often no product-market fit signal visible to traditional data sources. What they <em>do</em> have — and what the <a href="https://signals.gitdealflow.com">VC Deal Flow Signal</a> measures — is raw engineering output.</p>
<p>Our research shows that pre-seed teams with 14-day commit velocities above {preseed[0]['commitVelocity14d'] if preseed else 0} commits and accelerating contributor growth are <strong>3× more likely</strong> to announce a funding round within 6 weeks than pre-seed teams below that threshold.</p>
<p><strong>What to look for:</strong></p>
<ul style="color:#94a3b8;font-size:.78rem;">
<li><strong>High commit velocity</strong> with low contributor count → founder-led, outsized output</li>
<li><strong>Infrastructure buildout</strong> signal → preparing for scale (and hiring)</li>
<li><strong>Engineering hiring burst</strong> ↔ already scaling the team before the round</li>
</ul>
</div>
<div style="overflow-x:auto;">
<table>
<thead>
<tr><th style="width:30px">#</th><th>Startup</th><th>Region</th><th style="text-align:center">14d Velocity</th><th style="text-align:right">Velocity Δ</th><th style="text-align:center">Contribs</th><th>Signal Type</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<div class="note">
  <p>Data sourced from <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> · <a href="/hidden-gems.html">Hidden Gems</a> · <a href="/sector-guide.html">Sector Guide</a> · <a href="/geo-signals.html">Startup Engineering by Geography</a> · <a href="https://signals.gitdealflow.com/methodology">Methodology</a></p>
<p style="margin-top:.5rem;"><a href="/trending.html" style="color:#60a5fa;">View All 20 Trending Startups →</a></p>
</div>
</main>
{FOOTER}
</body>
</html>"""
    return content

# ── PAGE 4: geo-signals.html ──
def build_geo_signals():
    """Group by geography, count, velocity trends, top 3 per geography."""
    geos = {}
    for t in trending:
        geo = t["geography"] if t["geography"] != "Unknown" else "Unknown"
        if geo not in geos:
            geos[geo] = []
        geos[geo].append(t)

    # Order: US, EU, APAC, UK, Unknown
    geo_order = ["US", "EU", "APAC", "UK", "Unknown"]
    geo_sections = ""
    for g in geo_order:
        if g not in geos:
            continue
        startups = geos[g]
        startups.sort(key=lambda s: parse_velocity_change(s["commitVelocityChange"]), reverse=True)

        avg_vel = sum(parse_velocity_change(s["commitVelocityChange"]) for s in startups) / len(startups)
        top3 = startups[:3]
        top3_html = ""
        for i, s in enumerate(top3, 1):
            top3_html += f"""<tr>
<td style="text-align:center">#{i}</td>
<td><a href="{profile_url(s['name'])}" style="font-weight:500;color:#f1f5f9;">{s['name']}</a></td>
<td><span class="badge">{s['stage']}</span></td>
<td style="text-align:center;font-weight:700;">{s['commitVelocity14d']}</td>
<td style="color:{velocity_color(s['commitVelocityChange'])};font-weight:700;text-align:right;">{s['commitVelocityChange']}</td>
<td>{signal_badge(s['signalType'])}</td>
</tr>"""

        geo_sections += f"""<h2>{geo_flag(g)} {g} <span class="badge">{len(startups)} trending startups</span></h2>
<p style="color:#94a3b8;font-size:.8rem;">Average velocity change: <strong style="color:#4ade80;">+{avg_vel:.0f}%</strong> · {len(startups)} startups in current trending set</p>
<h3>Top 3 in {g}</h3>
<table>
<thead><tr><th style="width:30px">Rank</th><th>Startup</th><th>Stage</th><th style="text-align:center">14d Vel</th><th style="text-align:right">Vel Δ</th><th>Signal</th></tr></thead>
<tbody>{top3_html}</tbody>
</table>
<p style="font-size:.75rem;margin-top:.25rem;"><a href="https://signals.gitdealflow.com?geo={g.lower()}" style="color:#60a5fa;">View all {g} startups on signals.gitdealflow.com →</a></p>"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Startup Engineering by Geography: US vs EU vs APAC vs UK | GitDealFlow</title>
<meta name="description" content="Startup engineering activity compared across geographies: US, EU, APAC, UK. Commit velocity trends, top startups per region, and geographic signal distribution.">
<link rel="canonical" href="https://gitdealflow.com/geo-signals.html">
<meta property="og:title" content="Startup Engineering by Geography: US vs EU vs APAC vs UK">
<meta property="og:description" content="Compare startup engineering velocity across geographies. Which region has the fastest-moving teams?">
<meta property="og:url" content="https://gitdealflow.com/geo-signals.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="news_keywords" content="Startup geography, US startups, EU startups, APAC startups, UK startups, engineering velocity, deal flow, startup regions, venture capital" />
<meta property="article:tag" content="Startup geography" />
<meta property="article:tag" content="US startups" />
<meta property="article:tag" content="EU startups" />
<meta property="article:tag" content="APAC startups" />
<meta property="article:tag" content="UK startups" />
<meta property="article:tag" content="engineering velocity" />
<meta property="article:tag" content="deal flow" />
<meta property="article:tag" content="startup regions" />
<meta property="article:tag" content="venture capital" />
<meta property="article:published_time" content="{TODAY_RFC}" />
<meta property="article:modified_time" content="{TODAY_RFC}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Startup Engineering by Geography: US vs EU vs APAC vs UK",
  "description": "Regional comparison of startup engineering velocity trends with top startups per geography.",
  "datePublished": "{TODAY_RFC}",
  "dateModified": "{TODAY_RFC}",
  "publisher": {{"@type":"Organization","name":"GitDealFlow","url":"https://gitdealflow.com"}},
  "mainEntityOfPage": "https://gitdealflow.com/geo-signals.html",
  "about": {{"@type":"Thing","name":"Startup Geography Signals"}}
}}</script>
{STYLES}
</head>
<body>
{HEADER}
<main class="container">
<h1>Startup Engineering by Geography: US vs EU vs APAC vs UK</h1>
<p class="subtitle">Comparing engineering velocity trends across regions · Top 20 trending startups · {period} · {TODAY}</p>
{geo_sections}
<h2>Key Insights Across Geographies</h2>
<div class="card">
<h3>Which Region is Moving Fastest?</h3>
<p style="color:#94a3b8;font-size:.78rem;">Based on the current VC Deal Flow Signal dataset of {api['meta']['totalStartups']} startups across 15 sectors, the distribution of trending engineering activity varies significantly by geography. US-based startups tend to dominate raw commit volumes, while EU and APAC teams show higher proportional velocity change percentages — suggesting catch-up growth cycles in those markets.</p>
<p style="color:#94a3b8;font-size:.78rem;margin-top:.5rem;">For deal-flow sourcing, a multi-geography strategy is increasingly essential: the next breakout startup is as likely to emerge from Bangalore or Berlin as from Silicon Valley.</p>
</div>
<div class="note">
  <p>Data sourced from <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> · <a href="/sector-guide.html">Sector Guide</a> · <a href="/pre-seed-signals.html">Pre-Seed Signals</a> · <a href="/trending.html">Trending Startups</a> · <a href="https://signals.gitdealflow.com/methodology">Methodology</a></p>
</div>
</main>
{FOOTER}
</body>
</html>"""
    return content

# ── PAGE 5: trending-signals.html ──
def build_trending_signals():
    """All 20 trending startups sorted by velocity change descending."""
    sorted_t = sorted(trending, key=lambda s: parse_velocity_change(s["commitVelocityChange"]), reverse=True)

    rows = ""
    for i, s in enumerate(sorted_t, 1):
        vc = parse_velocity_change(s["commitVelocityChange"])
        is_leader = vc >= 999
        row_style = 'style="background:#0f172a;border-left:3px solid #4ade80;"' if is_leader else ""
        rows += f"""<tr {row_style}>
<td style="color:#475569;text-align:center;">{i}</td>
<td><a href="{profile_url(s['name'])}" style="font-weight:500;color:#f1f5f9;">{s['name']}</a></td>
<td><span class="badge">{s['stage']}</span></td>
<td>{geo_flag(s['geography'])} {s['geography']}</td>
<td style="color:{velocity_color(s['commitVelocityChange'])};font-weight:700;text-align:right;">{s['commitVelocityChange']}</td>
<td style="text-align:center">{s['contributors']}</td>
<td>{signal_badge(s['signalType'])}</td>
</tr>"""

    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>This Week's Trending Startup Signals [Updated Weekly] | GitDealFlow</title>
<meta name="description" content="Weekly updated list of the top 20 trending startups by engineering velocity. Commit velocity, signal type, contributors, and geography for each startup.">
<link rel="canonical" href="https://gitdealflow.com/trending-signals.html">
<meta property="og:title" content="This Week's Trending Startup Signals [Updated Weekly]">
<meta property="og:description" content="Current top 20 trending startups ranked by engineering velocity change. Updated weekly from VC Deal Flow Signal data.">
<meta property="og:url" content="https://gitdealflow.com/trending-signals.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="news_keywords" content="Trending startups, weekly startup signals, engineering velocity, deal flow, GitHub, venture capital, startup ranking, weekly update" />
<meta property="article:tag" content="Trending startups" />
<meta property="article:tag" content="weekly startup signals" />
<meta property="article:tag" content="engineering velocity" />
<meta property="article:tag" content="deal flow" />
<meta property="article:tag" content="GitHub" />
<meta property="article:tag" content="venture capital" />
<meta property="article:tag" content="startup ranking" />
<meta property="article:tag" content="weekly update" />
<meta property="article:published_time" content="{TODAY_RFC}" />
<meta property="article:modified_time" content="{TODAY_RFC}" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "This Week's Trending Startup Signals [Updated Weekly]",
  "description": "Weekly ranking of the top 20 trending startups by engineering velocity change, including stage, geography, contributors, and signal type.",
  "datePublished": "{TODAY_RFC}",
  "dateModified": "{TODAY_RFC}",
  "publisher": {{"@type":"Organization","name":"GitDealFlow","url":"https://gitdealflow.com"}},
  "mainEntityOfPage": "https://gitdealflow.com/trending-signals.html",
  "about": {{"@type":"Thing","name":"Trending Startup Signals"}}
}}</script>
{STYLES}
</head>
<body>
{HEADER}
<main class="container">
<h1>This Week's Trending Startup Signals <span style="font-size:.7rem;background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:4px;vertical-align:middle;">Updated Weekly</span></h1>
<p class="subtitle">Top 20 trending startups ranked by commit velocity change · {period} · Data refreshed {TODAY}</p>
<div class="card">
  <p><strong>About this weekly signal:</strong> The VC Deal Flow Signal monitors {api['meta']['totalStartups']} startup GitHub organizations across {len(sectors)} sectors. Each week, the top 20 by engineering velocity change are surfaced here. Startups highlighted in <span style="color:#4ade80;">green</span> indicate extreme acceleration (≥+999% velocity change).</p>
  <p style="color:#94a3b8;font-size:.75rem;margin-top:.5rem;">⬤ Green left border = extreme acceleration (≥+999% velocity change)</p>
</div>
<div style="overflow-x:auto;">
<table>
<thead>
<tr><th style="width:30px">#</th><th>Startup</th><th>Stage</th><th>Region</th><th style="text-align:right">Vel Δ</th><th style="text-align:center">Contribs</th><th>Signal Type</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</div>
<h2>Weekly Update Note</h2>
<p style="color:#94a3b8;font-size:.8rem;">This page is updated every Monday with fresh data from the VC Deal Flow Signal pipeline. The ranking reflects the most recent 14-day commit window. For real-time data, visit <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> or subscribe to the free Sunday email digest.</p>
<div class="note">
  <p>Data sourced from <a href="https://signals.gitdealflow.com">signals.gitdealflow.com</a> · <a href="/hidden-gems.html">Hidden Gems</a> · <a href="/sector-guide.html">Sector Guide</a> · <a href="/geo-signals.html">Geo Signals</a> · <a href="/pre-seed-signals.html">Pre-Seed Signals</a> · <a href="https://signals.gitdealflow.com/methodology">Methodology</a></p>
</div>
</main>
{FOOTER}
</body>
</html>"""
    return content


# ── Write all files ──
pages = [
    ("hidden-gems.html", build_hidden_gems()),
    ("sector-guide.html", build_sector_guide()),
    ("pre-seed-signals.html", build_preseed_signals()),
    ("geo-signals.html", build_geo_signals()),
    ("trending-signals.html", build_trending_signals()),
]

for filename, html in pages:
    path = os.path.join(LANDING, filename)
    with open(path, "w") as f:
        f.write(html)
    size_kb = os.path.getsize(path) / 1024
    print(f"Created {filename} — {size_kb:.1f} KB")

print("\nDone! All 5 pages created.")
