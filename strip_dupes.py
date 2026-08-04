#!/usr/bin/env python3
"""Remove all related-pages sections from HTML files. Simple regex approach."""
import os
import re

LANDING_DIR = "/Users/sipi/Downloads/gitdealflow/landing"
EXCLUDE_DIRS = {".vercel", ".git", ".well-known", "__pycache__", "node_modules", "assets", "api", "badge", "brand-assets"}
PATTERN = re.compile(r'<div class="related-pages"[^>]*>.*?</div>\s*</div>', re.DOTALL)

count = 0
for root, dirs, files in os.walk(LANDING_DIR):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        file_path = os.path.join(root, f)
        try:
            with open(file_path, 'r', encoding='utf-8') as fh:
                html = fh.read()
        except:
            continue
        if 'related-pages' not in html:
            continue
        stripped, n = PATTERN.subn('', html)
        if n > 0:
            with open(file_path, 'w', encoding='utf-8') as fh:
                fh.write(stripped)
            count += 1

print(f"Cleaned {count} files")
