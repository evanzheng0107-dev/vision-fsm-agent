#!/usr/bin/env python3
"""
Generate the synthetic demo template assets used by the Visual Grid World.

These are 100% programmatically generated images (no third-party content).
They are drawn with the same primitives the demo environment uses to
render its frames, guaranteeing that template matching succeeds.

Usage::

    python scripts/generate_demo_assets.py
    python scripts/generate_demo_assets.py --out examples/visual_grid_world/assets

Outputs (into examples/visual_grid_world/assets/ by default):
    target_goal.png      - green crosshair navigation target
    pickup_item.png      - gold circle collectible
    interact_button.png  - blue square interactable
"""

from __future__ import annotations

import os
import sys

# Ensure src/ is importable.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import cv2  # noqa: E402

from vision_fsm_agent.envs.grid_world import (  # noqa: E402
    make_button_template,
    make_goal_template,
    make_item_template,
)


def main() -> None:
    out_dir = os.path.join(ROOT, "examples", "visual_grid_world", "assets")
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        out_dir = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else out_dir
    os.makedirs(out_dir, exist_ok=True)

    assets = {
        "target_goal.png": make_goal_template(),
        "pickup_item.png": make_item_template(),
        "interact_button.png": make_button_template(),
    }
    for name, img in assets.items():
        path = os.path.join(out_dir, name)
        cv2.imwrite(path, img)
        print(f"  wrote {path}  ({img.shape[1]}x{img.shape[0]})")

    print(f"\nDone. {len(assets)} templates generated in {out_dir}/")


if __name__ == "__main__":
    main()
