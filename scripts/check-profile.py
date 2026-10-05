"""Validate local profile assets and owned repository links without network calls."""
import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repos-root", type=Path, default=Path.home() / "Developer/personal")
args = parser.parse_args()
for asset in (root / "assets").rglob("*.svg"):
    ET.parse(asset)
readme = (root / "README.md").read_text()
for name in sorted(set(re.findall(r"https://github.com/nickromney/([A-Za-z0-9_.-]+)", readme))):
    sibling = args.repos_root / name
    if not (sibling / ".git").exists():
        raise SystemExit(f"Repository link has no local evidence: {name}")
    remote = subprocess.check_output(["git", "-C", str(sibling), "remote", "get-url", "origin"], text=True).strip()
    if not remote.endswith(f"nickromney/{name}.git") and not remote.endswith(f"nickromney/{name}"):
        raise SystemExit(f"Repository link differs from local remote: {name}")
print("Local SVG and owned repository link evidence passed; live website status not claimed.")
