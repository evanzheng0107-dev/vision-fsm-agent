"""Pytest configuration: make src/ and demo_app/ importable."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for sub in ("src", "demo_app"):
    path = os.path.join(ROOT, sub)
    if path not in sys.path:
        sys.path.insert(0, path)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
