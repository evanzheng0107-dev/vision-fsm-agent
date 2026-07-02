#!/usr/bin/env python3
"""
Run the Visual Grid World demo.

Usage::

    python examples/visual_grid_world/run_demo.py
    python examples/visual_grid_world/run_demo.py --steps 35
    python examples/visual_grid_world/run_demo.py --save demo_frames
"""

import os
import sys

# Ensure the package is importable when running this script directly.
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from vision_fsm_agent.envs.grid_world import run_standalone  # noqa: E402

if __name__ == "__main__":
    max_steps = 50
    save_dir = None
    args = sys.argv[1:]
    if "--save" in args:
        idx = args.index("--save")
        save_dir = args[idx + 1] if idx + 1 < len(args) else "demo_frames"
    if "--steps" in args:
        idx = args.index("--steps")
        try:
            max_steps = int(args[idx + 1])
        except (IndexError, ValueError):
            pass

    run_standalone(max_steps=max_steps, save_dir=save_dir)
