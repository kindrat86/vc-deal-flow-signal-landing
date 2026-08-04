#!/usr/bin/env python3
"""
Interlinking Network Builder for gitdealflow.com (~1500 landing pages)

Scans every .html file, classifies each page by its URL pattern, 
and inserts a contextual "Related Pages" section before the footer.
"""

import os
import re
import random

random.seed(42)

LANDING_DIR = "/Users/sipi/Downloads/gitdealflow/landing"
EXCLUDE_DIRS = {".vercel", ".git", ".well-known", "__pycache__", "node_modules", "assets", "api", "badge", "brand-assets"}
SKIP_FILES = {"widget.html", "yandex_f3f5891cbff0b50f.html", "googlea30bb998b91eb6ac.html",
              "22df6d8f.txt", "22dfd6f8f816469b8c216bc7eaf8b936.txt", "7e74219f6f5444589470e663f0bd1392.txt",
              "97927552035549f482c81cdcaf24b511.txt", "BingSiteAuth.xml", ".gitignore", ".env.local",
              "_headers", "apple-touch-icon.png"}

# Known sectors
SECTORS = [
    "healthcare", "enterprise-saas", "fintech", "edtech", "ecommerce-infrastructure",
    "data-infrastructure", "agtech", "gaming", "hr-tech", "legal-tech", "proptech",
    "robotics", "social-community", "space-tech", "supply-chain", "web3",
    "ai--machine-learning", "climate--energy", "cybersecurity", "biotech",
    "ai-infrastructure",
]

# Known cities for geo pages
CITIES = [
    "san-francisco", "new-york", "london", "berlin", "austin", "bangalore",
    "boston", "toronto", "amsterdam", "tel-aviv",
]

# Known countries/regions
REGIONS = ["united-states", "united-kingdom", "europe", "apac", "latam", "canada"]

# Signal types
SIGNALS = ["hiring-burst", "deploy-spike", "framework-migration", "infra-buildout"]

# What-is terms
WHAT_IS_PAGES = [
    "what-is-engineering-velocity",
    "what-is-scout-score", 
    "what-is-deal-flow-signal",
    "what-is-startup-velocity-benchmark",
    "what-is-vc-deal-flow",
]

# Velocity pages
VELOCITY_PAGES = [
    "accelerating-startups",
    "high-velocity-startups",
    "velocity-index",
    "startup-velocity-report-2026",
]

# Stage pages
STAGE_PAGES = [
    "startups-pre-seed",
    "startups-seed",
    "startups-series-a",
    "startups-series-b",
    "pre-seed-signals",
]

# Tool pages
TOOL_PAGES = [
    "check-velocity",
    "scout",
    "benchmark",
    "trending-this-week",
    "tools",
]

# Audience pages
AUDIENCE_PAGES = [
    "for-venture-capital",
    "for-angel-investors", 
    "for-founders",
    "for-recruiters",
    "for-ai-agents",
]

# Top sector pages
TOP_SECTORS = [
    "top/agtech", "top/data-infrastructure", "top/ecommerce-infrastructure",
    "top/edtech", "top/enterprise-saas", "top/gaming", "top/healthcare",
    "top/hr-tech", "top/legal-tech", "top/proptech", "top/robotics",
    "top/social-community", "top/space-tech", "top/supply-chain", "top/web3",
]


def url_path(file_path):
    """Convert file path to URL path."""
    rel = os.path.relpath(file_path, LANDING_DIR)
    if rel.endswith(".html"):
        rel = rel[:-5]  # strip .html
    if rel == "index" or rel == "." or rel == "":
        return "/"
    # Handle subdirectory index files: vs/crunchbase/index -> /vs/crunchbase
    if rel.endswith("/index"):
        rel = rel[:-6]
        if rel == "":
            return "/"
    return "/" + rel


def classify_page(file_path, url):
    """Classify a page and return its type and metadata."""
    basename = os.path.basename(file_path)
    name_no_ext = re.sub(r'\.html$', '', basename)
    
    # Pages in subdirectories
    rel_dir = os.path.dirname(os.path.relpath(file_path, LANDING_DIR))
    
    # Competitive set pages in a/
    if rel_dir == "a" and name_no_ext.startswith("startups-like-"):
        slug = name_no_ext[len("startups-like-"):]
        return ("competitive_set", {"slug": slug})
    
    # Geo×Sector pages in g/
    if rel_dir == "g":
        # Pattern: {sector}-startups-in-{geo}.html
        return ("geo_x_sector", {"filename": name_no_ext})
    
    # Geo×Signal pages in s/
    if rel_dir == "s":
        # Pattern: {signal}-{geo}.html
        return ("geo_x_signal", {"filename": name_no_ext})
    
    # Top sector pages
    if rel_dir == "top":
        return ("top_sector", {"sector": name_no_ext})
    
    # vs/ pages
    if rel_dir.startswith("vs"):
        return ("vs_page", {"slug": name_no_ext})
    
    # Tool pages
    if name_no_ext in TOOL_PAGES:
        return ("tool", {"slug": name_no_ext})
    
    # Velocity pages
    if name_no_ext in VELOCITY_PAGES:
        return ("velocity", {"slug": name_no_ext})
    
    # Stage pages
    if name_no_ext in STAGE_PAGES:
        return ("stage", {"slug": name_no_ext})
    
    # What-is pages
    if name_no_ext.startswith("what-is-"):
        return ("what_is", {"term": name_no_ext[len("what-is-"):]})
    
    # Audience pages
    if name_no_ext in AUDIENCE_PAGES:
        return ("audience", {"slug": name_no_ext})
    
    # Signal type pages
    if name_no_ext == "startups-hiring-burst":
        return ("signal", {"signal": "hiring-burst"})
    if name_no_ext == "startups-deploy-spike":
        return ("signal", {"signal": "deploy-spike"})
    
    # Sector pages
    if name_no_ext.startswith("sector-"):
        sector = name_no_ext[len("sector-"):]
        return ("sector", {"sector": sector})
    
    # City pages: startups-in-{city}.html where city is a specific city
    if name_no_ext.startswith("startups-in-"):
        location = name_no_ext[len("startups-in-"):]
        if location in CITIES:
            return ("city", {"city": location})
        elif location in REGIONS:
            return ("region", {"region": location})
        else:
            return ("city", {"city": location})
    
    # FAQ pages
    if name_no_ext.startswith("faq-"):
        return ("faq", {"sector": name_no_ext[len("faq-"):]})
    
    # Default
    return ("other", {"slug": name_no_ext})


def extract_title(html):
    """Extract the title from an HTML document."""
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Clean up common patterns
        title = re.sub(r'\s*\|\s*GitDealFlow.*$', '', title)
        title = re.sub(r'\s*\|.*$', '', title)
        return title.strip()
    return ""


def build_link_href(url, label):
    """Build an anchor tag."""
    return f'<a href="{url}" style="color:#60a5fa;text-decoration:none;font-size:0.85rem">{label}</a>'


def title_to_label(title, fallback):
    """Convert a full title to a short label."""
    if title:
        # Use first part of title
        short = re.sub(r'\s*[—–-]\s*.*$', '', title).strip()
        short = re.sub(r'\s*\|\s*.*$', '', short).strip()
        if len(short) > 60:
            short = short[:57] + "..."
        return short
    return fallback


def nice_sector_name(sector):
    """Convert sector-slug to nice name."""
    names = {
        "healthcare": "Healthcare",
        "enterprise-saas": "Enterprise SaaS",
        "fintech": "Fintech",
        "edtech": "EdTech", 
        "ecommerce-infrastructure": "E-Commerce Infrastructure",
        "data-infrastructure": "Data Infrastructure",
        "agtech": "AgTech",
        "gaming": "Gaming",
        "hr-tech": "HR Tech",
        "legal-tech": "Legal Tech",
        "proptech": "PropTech",
        "robotics": "Robotics",
        "social-community": "Social & Community",
        "space-tech": "Space Tech",
        "supply-chain": "Supply Chain",
        "web3": "Web3",
        "ai--machine-learning": "AI & Machine Learning",
        "climate--energy": "Climate & Energy",
        "cybersecurity": "Cybersecurity",
        "biotech": "Biotech",
        "ai-infrastructure": "AI Infrastructure",
    }
    return names.get(sector, sector.replace("-", " ").title())


def nice_city_name(city):
    """Convert city slug to nice name."""
    names = {
        "san-francisco": "San Francisco",
        "new-york": "New York",
        "london": "London",
        "berlin": "Berlin",
        "austin": "Austin",
        "bangalore": "Bangalore",
        "boston": "Boston",
        "toronto": "Toronto",
        "amsterdam": "Amsterdam",
        "tel-aviv": "Tel Aviv",
    }
    return names.get(city, city.replace("-", " ").title())


def nice_region_name(region):
    names = {
        "united-states": "United States",
        "united-kingdom": "United Kingdom",
        "europe": "Europe",
        "apac": "APAC",
        "latam": "LATAM",
        "canada": "Canada",
    }
    return names.get(region, region.replace("-", " ").title())


def related_pages_section(links):
    """Build the Related Pages HTML section."""
    if not links:
        return ""
    
    links_html = "\n".join(f'      {link}' for link in links)
    
    return f'''
<div class="related-pages" style="margin-top:2rem;padding-top:1.5rem;border-top:1px solid #1e293b">
  <h3 style="color:#e2e8f0;font-size:1rem;margin-bottom:0.75rem">Related Pages</h3>
  <div class="related-links" style="display:flex;gap:1rem;flex-wrap:wrap">
{links_html}
  </div>
</div>
'''


def add_related_section(file_path, html, links):
    """Insert a Related Pages section before </footer> or </body>."""
    section = related_pages_section(links)
    if not section:
        return html
    
    # Insert before </footer>
    if "</footer>" in html:
        html = html.replace("</footer>", section + "\n  </footer>", 1)
    elif "</body>" in html:
        html = html.replace("</body>", section + "\n  </body>", 1)
    else:
        # No footer or body - append at end
        html += section
    
    return html


def generate_links(page_type, metadata, page_index, all_info):
    """Generate contextual links for a page based on its type."""
    links = []
    
    if page_type == "sector":
        sector = metadata["sector"]
        # Link to 5 other sector pages
        other_sectors = [s for s in SECTORS if s != sector]
        random.shuffle(other_sectors)
        for os in other_sectors[:5]:
            url = f"/sector-{os}"
            label = f"{nice_sector_name(os)} Startups"
            links.append(build_link_href(url, label))
        # Link to trending + benchmark
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        # Link to a city page
        city = random.choice(CITIES)
        links.append(build_link_href(f"/startups-in-{city}", f"Startups in {nice_city_name(city)}"))
        
    elif page_type == "city":
        city = metadata["city"]
        # Link to 3 other city pages
        other_cities = [c for c in CITIES if c != city]
        random.shuffle(other_cities)
        for oc in other_cities[:3]:
            url = f"/startups-in-{oc}"
            label = f"Startups in {nice_city_name(oc)}"
            links.append(build_link_href(url, label))
        # Link to a relevant country/region
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        # Link to a few sectors
        for sector in random.sample(SECTORS, 2):
            links.append(build_link_href(f"/sector-{sector}", f"{nice_sector_name(sector)} Startups"))
        
    elif page_type == "region":
        region = metadata["region"]
        # Link to 3 other regions
        other_regions = [r for r in REGIONS if r != region]
        random.shuffle(other_regions)
        for or_ in other_regions[:3]:
            url = f"/startups-in-{or_}"
            label = f"Startups in {nice_region_name(or_)}"
            links.append(build_link_href(url, label))
        # Link to cities
        for city in random.sample(CITIES, min(2, len(CITIES))):
            links.append(build_link_href(f"/startups-in-{city}", f"Startups in {nice_city_name(city)}"))
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        
    elif page_type == "competitive_set":
        slug = metadata["slug"]
        # Link to 3 other competitive set pages
        comp_pages = page_index.get("competitive_set", [])
        other_comp = [c for c in comp_pages if c["slug"] != slug]
        random.shuffle(other_comp)
        for oc in other_comp[:3]:
            url = f"/a/startups-like-{oc['slug']}"
            label = title_to_label(oc.get("title", ""), f"Startups like {oc['slug']}")
            links.append(build_link_href(url, label))
        # Link to sector page + benchmark
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        
    elif page_type == "signal":
        signal = metadata["signal"]
        # Link to other signal pages
        other_signals = [s for s in SIGNALS if s != signal] if signal in SIGNALS else SIGNALS
        for s in other_signals[:3]:
            if s == "hiring-burst":
                links.append(build_link_href("/startups-hiring-burst", "Startups with Hiring Burst"))
            elif s == "deploy-spike":
                links.append(build_link_href("/startups-deploy-spike", "Startups with Deploy Spikes"))
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        # Link to relevant sectors
        for sector in random.sample(SECTORS, 2):
            links.append(build_link_href(f"/sector-{sector}", f"{nice_sector_name(sector)} Startups"))
        
    elif page_type == "velocity":
        slug = metadata["slug"]
        # Link to other velocity pages
        other_v = [v for v in VELOCITY_PAGES if v != slug]
        for ov in other_v[:3]:
            nice = ov.replace("-", " ").title()
            links.append(build_link_href(f"/{ov}", nice))
        links.append(build_link_href("/check-velocity", "Check Startup Velocity"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        
    elif page_type == "what_is":
        term = metadata["term"]
        # Link to other what-is pages
        other_w = [w for w in WHAT_IS_PAGES if w != f"what-is-{term}"]
        for ow in other_w[:4]:
            nice = ow.replace("what-is-", "").replace("-", " ").title()
            links.append(build_link_href(f"/{ow}", f"What Is {nice}?"))
        # Link to tools
        links.append(build_link_href("/check-velocity", "Check Startup Velocity"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        
    elif page_type == "geo_x_sector":
        filename = metadata["filename"]
        # Extract sector from filename pattern: {sector}-startups-in-{geo}
        parts = filename.split("-startups-in-")
        sector_slug = parts[0] if len(parts) > 1 else ""
        geo_part = parts[1] if len(parts) > 1 else ""
        
        # Link to sector page
        if sector_slug and sector_slug in SECTORS:
            links.append(build_link_href(f"/sector-{sector_slug}", f"{nice_sector_name(sector_slug)} Startups"))
        
        # Link to other geo×sector pages with same sector
        geo_pages = page_index.get("geo_x_sector", [])
        same_sector = [g for g in geo_pages if g["filename"].startswith(sector_slug) and g["filename"] != filename]
        random.shuffle(same_sector)
        for gs in same_sector[:2]:
            links.append(build_link_href(f"/g/{gs['filename']}", title_to_label(gs.get("title", ""), gs['filename'])))
        
        # Link to city page if geo_part is a city
        if geo_part in CITIES:
            links.append(build_link_href(f"/startups-in-{geo_part}", f"Startups in {nice_city_name(geo_part)}"))
        elif geo_part in REGIONS:
            links.append(build_link_href(f"/startups-in-{geo_part}", f"Startups in {nice_region_name(geo_part)}"))
        
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        
    elif page_type == "geo_x_signal":
        filename = metadata["filename"]
        # Pattern: {signal}-{geo}.html — find geo×sector pages for same geo
        signal_parts = filename.split("-")
        # Try to extract geo (last part after last -)
        geo_candidates = []
        for g in CITIES + REGIONS:
            g_short = g.replace("united-", "").replace("-", "")
            if g_short in filename.replace("-", ""):
                geo_candidates.append(g)
        
        # Link to geo×sector pages
        geo_sector_pages = page_index.get("geo_x_sector", [])
        if geo_candidates:
            target_geo = geo_candidates[0]
            related_geo = [g for g in geo_sector_pages if target_geo.replace("-", "") in g["filename"].replace("-", "")]
            random.shuffle(related_geo)
            for rg in related_geo[:3]:
                links.append(build_link_href(f"/g/{rg['filename']}", title_to_label(rg.get("title", ""), rg['filename'])))
        
        # Link to other geo×signal pages
        signal_pages = page_index.get("geo_x_signal", [])
        others = [s for s in signal_pages if s["filename"] != filename]
        random.shuffle(others)
        for os_ in others[:2]:
            links.append(build_link_href(f"/s/{os_['filename']}", title_to_label(os_.get("title", ""), os_['filename'])))
        
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/startups-hiring-burst", "Hiring Burst Signals"))
        links.append(build_link_href("/startups-deploy-spike", "Deploy Spike Signals"))
        
    elif page_type == "top_sector":
        sector = metadata["sector"]
        # Link to other top sector pages
        other_top = [t for t in TOP_SECTORS if t != f"top/{sector}"]
        random.shuffle(other_top)
        for ot in other_top[:5]:
            label = f"Top 10 {nice_sector_name(ot.split('/')[1])} Startups"
            links.append(build_link_href(f"/{ot}", label))
        links.append(build_link_href(f"/sector-{sector}", f"{nice_sector_name(sector)} Sector"))
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        
    elif page_type == "stage":
        slug = metadata["slug"]
        # Link to other stage pages
        other_stages = [s for s in STAGE_PAGES if s != slug]
        for os_ in other_stages[:4]:
            nice = os_.replace("startups-", "").replace("-", " ").title()
            if os_ == "pre-seed-signals":
                nice = "Pre-Seed Signals"
            links.append(build_link_href(f"/{os_}", nice))
        # Link to sectors
        for sector in random.sample(SECTORS, 2):
            links.append(build_link_href(f"/sector-{sector}", f"{nice_sector_name(sector)} Startups"))
        
    elif page_type == "audience":
        slug = metadata["slug"]
        # Link to other audience pages
        other_aud = [a for a in AUDIENCE_PAGES if a != slug]
        for oa in other_aud[:3]:
            nice = oa.replace("for-", "For ").replace("-", " ").title()
            links.append(build_link_href(f"/{oa}", nice))
        # Link to tools
        links.append(build_link_href("/check-velocity", "Check Startup Velocity"))
        links.append(build_link_href("/scout", "Scout Score"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        
    elif page_type == "tool":
        slug = metadata["slug"]
        other_tools = [t for t in TOOL_PAGES if t != slug]
        for ot in other_tools[:4]:
            nice = ot.replace("-", " ").title()
            links.append(build_link_href(f"/{ot}", nice))
        # Link to trending + popular
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/startups-hiring-burst", "Startups Hiring Burst"))
        
    elif page_type == "faq":
        sector = metadata["sector"]
        if sector in SECTORS:
            links.append(build_link_href(f"/sector-{sector}", f"{nice_sector_name(sector)} Startups"))
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        for other_sector in random.sample([s for s in SECTORS if s != sector], min(3, len(SECTORS)-1)):
            links.append(build_link_href(f"/sector-{other_sector}", f"{nice_sector_name(other_sector)} Startups"))
        
    elif page_type == "vs_page":
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        links.append(build_link_href("/tools", "All Tools"))
        links.append(build_link_href("/sector-healthcare", f"{nice_sector_name('healthcare')} Startups"))
        links.append(build_link_href("/startups-hiring-burst", "Startups with Hiring Burst"))
        
    else:  # other
        links.append(build_link_href("/trending-this-week", "Trending This Week"))
        links.append(build_link_href("/benchmark", "Startup Velocity Benchmark"))
        links.append(build_link_href("/sector-healthcare", f"{nice_sector_name('healthcare')} Startups"))
        links.append(build_link_href("/startups-hiring-burst", "Startups with Hiring Burst"))
        links.append(build_link_href("/check-velocity", "Check Startup Velocity"))
    
    # Deduplicate links (keep first occurrence)
    seen_urls = set()
    unique_links = []
    for link in links:
        url_match = re.search(r'href="([^"]+)"', link)
        if url_match:
            url = url_match.group(1)
            if url not in seen_urls:
                seen_urls.add(url)
                unique_links.append(link)
        else:
            unique_links.append(link)
    
    # Limit to max 8 links
    return unique_links[:8]


def main():
    # First pass: collect all HTML files and their titles
    all_files = []
    page_index = {}  # type -> list of dicts
    
    for root, dirs, files in os.walk(LANDING_DIR):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for f in files:
            if not f.endswith(".html"):
                continue
            if f in SKIP_FILES:
                continue
            # Skip root-level index.html only, not subdirectory ones
            if root == LANDING_DIR and f == "index.html":
                continue
            
            file_path = os.path.join(root, f)
            url = url_path(file_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as fh:
                    html = fh.read()
            except Exception as e:
                print(f"  ERROR reading {file_path}: {e}")
                continue
            
            title = extract_title(html)
            page_type, metadata = classify_page(file_path, url)
            
            info = {
                "path": file_path,
                "url": url,
                "title": title,
                "type": page_type,
                "metadata": metadata,
                "html": html,
            }
            all_files.append(info)
            
            if page_type not in page_index:
                page_index[page_type] = []
            page_index[page_type].append({
                "slug": metadata.get("slug") or metadata.get("sector") or metadata.get("city") or metadata.get("region") or metadata.get("term") or metadata.get("filename") or os.path.basename(file_path),
                "title": title,
                "filename": os.path.basename(file_path),
                "path": file_path,
                "url": url,
                **metadata,
            })
    
    print(f"Found {len(all_files)} HTML files to process")
    print(f"Page type distribution:")
    for pt, pages in sorted(page_index.items()):
        print(f"  {pt}: {len(pages)}")
    
    # Second pass: add Related Pages sections
    modified = 0
    skipped_no_footer = 0
    
    for info in all_files:
        page_type = info["type"]
        metadata = info["metadata"]
        html = info["html"]
        file_path = info["path"]
        
        links = generate_links(page_type, metadata, page_index, all_info=None)
        
        if not links:
            print(f"  SKIP {file_path} — no links generated")
            continue
        
        # Skip if already has a related-pages section (re-run safe)
        if "related-pages" in html:
            continue
        
        new_html = add_related_section(file_path, html, links)
        
        if new_html != html:
            with open(file_path, 'w', encoding='utf-8') as fh:
                fh.write(new_html)
            modified += 1
            if modified % 100 == 0:
                print(f"  ... modified {modified} files so far")
        else:
            skipped_no_footer += 1
    
    print(f"\nDone! Modified {modified} files")
    print(f"Skipped (no change): {skipped_no_footer}")


if __name__ == "__main__":
    main()
