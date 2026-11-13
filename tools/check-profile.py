#!/usr/bin/env python3
"""Check local profile assets and owned repository links without network calls.

External links remain a dated owner review; this script never fetches them.
"""
import argparse
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repos-root', type=Path, default=Path.home() / 'Developer/personal')
args = parser.parse_args()

readme = (root / 'README.md').read_text()
class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append(dict(attrs).get('src', ''))


image_parser = ImageParser()
image_parser.feed(readme)
images = image_parser.images
local_images = 0
for image in images:
    url = urlsplit(image)
    if not url.scheme and not url.netloc:
        target = (root / unquote(url.path)).resolve()
        if not image or not target.is_relative_to(root) or not target.is_file():
            raise SystemExit(f'Local image is missing or outside the profile: {image}')
        local_images += 1
if not local_images:
    raise SystemExit('Profile must have its local header image')

for asset in sorted((root / 'assets').rglob('*.svg')):
    try:
        ET.parse(asset)
    except ET.ParseError as error:
        raise SystemExit(f'SVG is not well-formed XML: {asset.relative_to(root)}: {error}')

for name in sorted(set(re.findall(r'https://github.com/nickromney/([A-Za-z0-9_.-]+)', readme))):
    sibling = args.repos_root / name
    if not (sibling / '.git').exists():
        raise SystemExit(f'Repository link has no local evidence: {name}')
    try:
        remote = subprocess.check_output(['git', '-C', str(sibling), 'remote', 'get-url', 'origin'], text=True).strip()
    except subprocess.CalledProcessError:
        raise SystemExit(f'Repository has no origin remote: {name}')
    expected = f'nickromney/{name}'
    if remote.startswith('git@github.com:'):
        remote_path = remote.removeprefix('git@github.com:')
    else:
        remote_url = urlsplit(remote)
        remote_path = remote_url.path.lstrip('/') if remote_url.hostname == 'github.com' and remote_url.scheme in {'https', 'ssh', 'git'} else ''
    if remote_path.removesuffix('.git') != expected:
        raise SystemExit(f'Repository link differs from local remote: {name}')

print(f'Local profile assets verified: {len(images)} image references, SVG XML parsed, owned repository links matched local remotes. External claims/links were not live-certified.')
