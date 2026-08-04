#!/usr/bin/env python3
"""
Add Article schema with image, datePublished, dateModified, author to ALL
HTML pages that don't already have it. Supports Google rich snippets + Discover.
"""

import os
import re
import json
import glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

LANDING = "/Users/sipi/Downloads/gitdealflow/landing"
EXCLUDE_DIRS = {".vercel", ".git", "__pycache__", "node_modules"}

# The Article schema template
# We'll fill in headline, description, image, datePublished, dateModified
ARTICLE_TEMPLATE = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "PLACEHOLDER",
    "description": "PLACEHOLDER",
    "image": "https://gitdealflow.com/og.png",
    "datePublished": "2026-07-30",
    "dateModified": "2026-07-30",
    "author": {
        "@type": "Person",
        "name": "The Data Nerd",
        "url": "https://signals.gitdealflow.com/about"
    },
    "publisher": {
        "@type": "Organization",
        "name": "GitDealFlow",
        "url": "https://gitdealflow.com/"
    }
}

# Default fallback image
DEFAULT_IMAGE = "https://gitdealflow.com/og.png"


def has_existing_article(html):
    """Check if page already has Article schema with image field."""
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            # Handle array of LD+JSON objects
            items = data if isinstance(data, list) else [data]
            for item in items:
                # Handle @graph
                if '@graph' in item:
                    for sub in item['@graph']:
                        if sub.get('@type') == 'Article' and 'image' in sub:
                            return True
                # Direct Article with image
                if item.get('@type') == 'Article' and 'image' in item:
                    return True
        except (json.JSONDecodeError, AttributeError, TypeError):
            continue
    return False


def extract_meta(html):
    """Extract title, description, og:image, article:published_time from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Title
    title_tag = soup.find('title')
    title = title_tag.string.strip() if title_tag and title_tag.string else "GitDealFlow"
    
    # Meta description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag.get('content', '').strip() if desc_tag else ""
    
    # og:image
    og_image_tag = soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'})
    og_image = og_image_tag.get('content', '').strip() if og_image_tag else ""
    
    # twitter:image fallback
    if not og_image:
        tw_img = soup.find('meta', attrs={'name': 'twitter:image'})
        og_image = tw_img.get('content', '').strip() if tw_img else ""
    
    # article:published_time
    pub_time_tag = soup.find('meta', property='article:published_time')
    published_time = pub_time_tag.get('content', '').strip() if pub_time_tag else ""
    
    # article:modified_time
    mod_time_tag = soup.find('meta', property='article:modified_time')
    modified_time = mod_time_tag.get('content', '').strip() if mod_time_tag else ""
    
    return title, description, og_image, published_time, modified_time


def extract_date_from_str(s):
    """Try to extract a date from various formats."""
    if not s:
        return None
    # Try ISO format: 2026-07-30T08:00:00+00:00
    m = re.search(r'(\d{4}-\d{2}-\d{2})', s)
    if m:
        return m.group(1)
    return None


def build_article_schema(title, description, og_image, published_time, modified_time, file_mtime):
    """Build the Article schema dict with extracted data."""
    article = dict(ARTICLE_TEMPLATE)  # shallow copy
    article["headline"] = title
    
    # Description
    if description:
        article["description"] = description
    else:
        article["description"] = f"{title} — Learn more at GitDealFlow"
    
    # Image
    article["image"] = og_image if og_image else DEFAULT_IMAGE
    
    # datePublished
    pub_date = extract_date_from_str(published_time)
    if pub_date:
        article["datePublished"] = pub_date
    else:
        article["datePublished"] = "2026-07-30"
    
    # dateModified
    mod_date = extract_date_from_str(modified_time)
    if mod_date:
        article["dateModified"] = mod_date
    else:
        # Use file modification time
        mtime_dt = datetime.fromtimestamp(file_mtime, tz=timezone.utc)
        article["dateModified"] = mtime_dt.strftime("%Y-%m-%d")
    
    return article


def add_article_to_html(html, article_schema):
    """Insert Article schema into the HTML's JSON-LD block."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find existing LD+JSON scripts
    scripts = soup.find_all('script', type='application/ld+json')
    
    article_node = {
        "@type": "Article",
        "headline": article_schema["headline"],
        "description": article_schema["description"],
        "image": article_schema["image"],
        "datePublished": article_schema["datePublished"],
        "dateModified": article_schema["dateModified"],
        "author": article_schema["author"],
        "publisher": article_schema["publisher"]
    }
    
    if scripts:
        # Try to add Article to existing JSON-LD blocks
        added = False
        for script in scripts:
            try:
                data = json.loads(script.string)
                
                # CASE 1: Array of LD+JSON objects (common on this site)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@graph' in item:
                            item['@graph'].append(article_node)
                            added = True
                            break
                    if not added:
                        # Check if any item has @type that isn't Article
                        # If we have WebPage or similar, append Article to the array
                        data.append(article_node)
                        added = True
                    if added:
                        script.string = json.dumps(data, indent=2)
                        break
                
                # CASE 2: Object with @graph
                elif isinstance(data, dict) and '@graph' in data:
                    data['@graph'].append(article_node)
                    script.string = json.dumps(data, indent=2)
                    added = True
                    break
                
                # CASE 3: Standalone object (WebPage, BreadcrumbList, etc.)
                # Wrap into @graph
                elif isinstance(data, dict) and '@type' in data:
                    # Don't modify if it's already Article
                    if data['@type'] == 'Article':
                        continue
                    graph_data = {
                        "@context": "https://schema.org",
                        "@graph": [data, article_node]
                    }
                    script.string = json.dumps(graph_data, indent=2)
                    added = True
                    break
                    
            except (json.JSONDecodeError, AttributeError, TypeError):
                continue
        
        if not added:
            # If we still haven't added, append as new script
            new_script = soup.new_tag('script', type='application/ld+json')
            new_script.string = json.dumps({
                "@context": "https://schema.org",
                "@graph": [article_node]
            }, indent=2)
            # Add before </head>
            head = soup.find('head')
            if head:
                head.append(new_script)
    else:
        # No JSON-LD exists — create new script before </head>
        new_script = soup.new_tag('script', type='application/ld+json')
        new_script.string = json.dumps({
            "@context": "https://schema.org",
            "@graph": [article_node]
        }, indent=2)
        head = soup.find('head')
        if head:
            head.append(new_script)
    
    return str(soup)


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()
    
    # Check if already has Article with image
    if has_existing_article(html):
        return False, "Already has Article schema with image"
    
    # Extract metadata
    title, description, og_image, published_time, modified_time = extract_meta(html)
    
    # Get file mtime
    file_mtime = os.path.getmtime(filepath)
    
    # Build article schema
    article = build_article_schema(title, description, og_image, published_time, modified_time, file_mtime)
    
    # Add to HTML
    new_html = add_article_to_html(html, article)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    return True, f"Added Article: {article['headline'][:60]}..."


def find_html_files():
    """Find all .html files recursively excluding certain directories."""
    files = []
    for root, dirs, filenames in os.walk(LANDING):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))
    return files


def main():
    print("=" * 60)
    print("Article Schema Inserter — GitDealFlow Landing Pages")
    print("=" * 60)
    
    files = find_html_files()
    print(f"\nFound {len(files)} HTML files to process")
    
    added = 0
    skipped = 0
    errors = 0
    already_have = 0
    
    for i, filepath in enumerate(files):
        rel_path = os.path.relpath(filepath, LANDING)
        try:
            result, msg = process_file(filepath)
            if result:
                added += 1
                if added <= 3 or added % 100 == 0:
                    print(f"  [+] {rel_path}: {msg}")
            else:
                already_have += 1
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  [!] ERROR {rel_path}: {e}")
        
        # Progress indicator every 200 files
        if (i + 1) % 200 == 0:
            print(f"\n  ... processed {i+1}/{len(files)} files ({added} added, {already_have} skipped, {errors} errors) ...\n")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Total HTML files: {len(files)}")
    print(f"  Article schema added: {added}")
    print(f"  Already had Article: {already_have}")
    print(f"  Errors: {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
