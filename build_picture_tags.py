#!/usr/bin/env python3
"""
Vervang <img src="...jpg/jpeg"> tags met <picture> tags die WebP serveren
met JPG fallback. Werkt alleen op design-assets/images/ paden.

Behoudt: og:image meta tags (sociale media), CSS background-image,
schema.org JSON-LD image properties.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
IMG_DIR = ROOT / 'design-assets' / 'images'

# Welke .jpg/.jpeg bestanden hebben we een .webp van?
webp_available = set()
for f in IMG_DIR.glob('*.webp'):
    webp_available.add(f.stem)

print(f"WebP versies beschikbaar: {len(webp_available)}")

# Pattern: <img ... src="/design-assets/images/FILENAME.jpg" ... />
# Match attributes flexibel
IMG_PATTERN = re.compile(
    r'(<img\s+[^>]*?src=")(/design-assets/images/)([^"]+?)\.(jpg|jpeg)("[^>]*?/?>)',
    re.IGNORECASE
)

def replace_img_with_picture(match):
    pre = match.group(1)   # <img + attrs voor src
    path = match.group(2)  # /design-assets/images/
    name = match.group(3)  # filename zonder ext
    ext = match.group(4)   # jpg of jpeg
    post = match.group(5)  # rest van tag

    if name not in webp_available:
        return match.group(0)  # Geen webp, laat zoals het is

    img_tag = f'{pre}{path}{name}.{ext}{post}'
    return f'<picture><source srcset="{path}{name}.webp" type="image/webp">{img_tag}</picture>'


total_replaced = 0
files_changed = 0

for html_file in ROOT.rglob('*.html'):
    # Skip extractie folder
    if '_extracted' in str(html_file):
        continue

    text = html_file.read_text(encoding='utf-8')
    new_text, count = IMG_PATTERN.subn(replace_img_with_picture, text)
    if count > 0:
        html_file.write_text(new_text, encoding='utf-8')
        files_changed += 1
        total_replaced += count
        rel = html_file.relative_to(ROOT)
        print(f"  ✓ {rel}: {count} img-tags → picture")

print(f"\n==== Resultaat ====")
print(f"Bestanden aangepast: {files_changed}")
print(f"Totaal img→picture: {total_replaced}")
