"""Compatibility entry point for the canonical profile checker."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[1] / 'tools' / 'check-profile.py'), run_name='__main__')
