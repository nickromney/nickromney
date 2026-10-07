#!/usr/bin/env python3
"""Check local profile images; external links remain a dated owner review."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
readme = (root / 'README.md').read_text()
images = re.findall(r'<img\b[^>]*src="([^"]+)"', readme)
assert images, 'Profile must have its local header image'
for image in images:
    if '://' not in image:
        target = (root / image).resolve()
        assert target.is_relative_to(root), image
        assert target.is_file(), image
print(f'Local profile assets verified: {len(images)} image references. External claims/links were not live-certified.')
