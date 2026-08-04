#!/usr/bin/env python3
"""Fix remaining SEO gaps: sitemap_index, blog index metadata, knowledge graph, opensearch"""
import os, re

ROOT = '/Users/sipi/Downloads/gitdealflow/landing'

# ===== 1. SITEMAP INDEX XML =====
sitemap_index = '''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://gitdealflow.com/sitemap-pages.xml</loc>
    <lastmod>2026-07-29T12:00:00+00:00</lastmod>
  </sitemap>
</sitemapindex>
'''

with open(os.path.join(ROOT, 'sitemap_index.xml'), 'w') as f:
    f.write(sitemap_index)
print("1. sitemap_index.xml built")

# ===== 2. FIX BLOG INDEX PAGE =====
fpath = os.path.join(ROOT, 'blog', 'index.html')
with open(fpath) as f:
    html = f.read()

if 'article:published_time' not in html:
    # Add WebPage + Blog schema to blog index
    blog_schema = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": ["Blog", "CollectionPage"],
  "name": "VC Deal Flow Signal Blog",
  "description": "Startup engineering velocity analysis, GitHub momentum signals, and VC deal flow insights from The Data Nerd.",
  "url": "https://gitdealflow.com/blog",
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://gitdealflow.com"},
      {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://gitdealflow.com/blog"}
    ]
  }
}
</script>'''
    html = html.replace('</head>', blog_schema + '</head>')
    
    # Add discover meta tags
    discover_meta = '<meta property="article:published_time" content="2026-07-29T12:00:00+00:00" />\n<meta property="article:modified_time" content="2026-07-29T12:00:00+00:00" />'
    html = html.replace('</head>', discover_meta + '</head>')
    
    with open(fpath, 'w') as f:
        f.write(html)
    print("2. Blog index page fixed with Blog schema + published_time")
else:
    print("2. Blog index already has published_time")

# ===== 3. KNOWLEDGE GRAPH JSON =====
kg = {
    "@context": {
        "@vocab": "https://schema.org/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
    },
    "@graph": [
        {
            "@id": "https://gitdealflow.com/#organization",
            "@type": "Organization",
            "name": "GitDealFlow",
            "legalName": "VC Deal Flow Signal (GitDealFlow)",
            "url": "https://gitdealflow.com",
            "sameAs": [
                "https://signals.gitdealflow.com",
                "https://x.com/data_nerd",
                "https://www.linkedin.com/company/gitdealflow",
                "https://www.wikidata.org/wiki/Q139376302",
                "https://ssrn.com/abstract=6606558",
                "https://www.npmjs.com/package/@gitdealflow/mcp-signal",
                "https://github.com/kindrat86/mcp-deal-flow-signal",
                "https://t.me/gitdealflow"
            ],
            "knowsAbout": ["GitHub commit velocity", "venture capital alternative data", "startup engineering acceleration"],
            "foundingDate": "2025",
            "email": "signals@gitdealflow.com"
        },
        {
            "@id": "https://signals.gitdealflow.com/about#person",
            "@type": "Person",
            "name": "The Data Nerd",
            "url": "https://signals.gitdealflow.com/about",
            "worksFor": {"@id": "https://gitdealflow.com/#organization"},
            "sameAs": [
                "https://orcid.org/0009-0002-2222-4112",
                "https://x.com/data_nerd",
                "https://github.com/kindrat86",
                "https://news.ycombinator.com/user?id=the_data_nerd"
            ]
        },
        {
            "@id": "https://signals.gitdealflow.com/#website",
            "@type": "WebSite",
            "name": "VC Deal Flow Signal",
            "alternateName": "GitDealFlow",
            "url": "https://signals.gitdealflow.com",
            "publisher": {"@id": "https://gitdealflow.com/#organization"}
        },
        {
            "@id": "https://gitdealflow.com/#datasets",
            "@type": "Dataset",
            "name": "VC Deal Flow Signal Dataset",
            "description": "Startup engineering velocity data from public GitHub activity across 313 startups in 15 sectors",
            "url": "https://signals.gitdealflow.com",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "publisher": {"@id": "https://gitdealflow.com/#organization"}
        }
    ]
}

import json as j
with open(os.path.join(ROOT, 'knowledge-graph.json'), 'w') as f:
    j.dump(kg, f, indent=2)
print("3. knowledge-graph.json built")

# ===== 4. OPENSEARCH XML =====
opensearch = '''<?xml version="1.0" encoding="UTF-8"?>
<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
  <ShortName>GitDealFlow</ShortName>
  <Description>Search startup engineering velocity data and VC deal flow signals</Description>
  <InputEncoding>UTF-8</InputEncoding>
  <Image height="16" width="16" type="image/x-icon">https://gitdealflow.com/favicon.ico</Image>
  <Url type="text/html" template="https://gitdealflow.com/search?q={searchTerms}"/>
  <Url type="application/opensearchdescription+xml" rel="self" template="https://gitdealflow.com/opensearch.xml"/>
</OpenSearchDescription>
'''

with open(os.path.join(ROOT, 'opensearch.xml'), 'w') as f:
    f.write(opensearch)
print("4. opensearch.xml built")

# ===== 5. ADD SEARCH LINKS TO INDEX.HTML =====
fpath = os.path.join(ROOT, 'index.html')
with open(fpath) as f:
    html = f.read()

if 'opensearch' not in html:
    search_links = '<link rel="search" type="application/opensearchdescription+xml" href="https://gitdealflow.com/opensearch.xml" title="GitDealFlow" />\n<link rel="alternate" type="application/ld+json" href="https://gitdealflow.com/knowledge-graph.json" title="Knowledge Graph" />'
    html = html.replace('</head>', search_links + '</head>')
    with open(fpath, 'w') as f:
        f.write(html)
    print("5. Search links added to index.html")
else:
    print("5. Index.html already has search links")

# ===== 6. UPDATE VERCEL.JSON FOR NEW STATIC FILES =====
v_path = os.path.join(ROOT, 'vercel.json')
with open(v_path) as f:
    v = j.load(f)

# Add rewrites for new files
new_rewrites = {
    '/sitemap_index.xml': '/sitemap_index.xml',
    '/knowledge-graph.json': '/knowledge-graph.json',
    '/opensearch.xml': '/opensearch.xml'
}
for src, dest in new_rewrites.items():
    if not any(r['source'] == src for r in v.get('rewrites', [])):
        v['rewrites'].insert(0, {'source': src, 'destination': dest})

with open(v_path, 'w') as f:
    j.dump(v, f, indent=2)
print("6. vercel.json updated")

print("\nDone! All gaps fixed.")
