#!/usr/bin/env python3
"""Check local profile assets and owned repository links without network calls.

External links remain a dated owner review; this script never fetches them.
"""
import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repos-root', type=Path, default=Path.home() / 'Developer/personal')
args = parser.parse_args()

readme = (root / 'README.md').read_text()
images = re.findall(r'<img\b[^>]*src="([^"]+)"', readme)
assert images, 'Profile must have its local header image'
for image in images:
    if '://' not in image:
        target = (root / image).resolve()
        assert target.is_relative_to(root), image
        assert target.is_file(), image

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
    if not remote.endswith(f'nickromney/{name}.git') and not remote.endswith(f'nickromney/{name}'):
        raise SystemExit(f'Repository link differs from local remote: {name}')

print(f'Local profile assets verified: {len(images)} image references, SVG XML parsed, owned repository links matched local remotes. External claims/links were not live-certified.')
