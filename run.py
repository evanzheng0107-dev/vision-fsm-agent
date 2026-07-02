#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vision FSM Agent - launcher.

Default mode runs the synthetic demo environment (no external software
or screen capture required).

Usage::

    python run.py --start            # run the demo (default)
    python run.py --start --steps 30 # run N demo steps
    python run.py --start --live     # live screen capture (advanced)
    python run.py --hil              # start the HIL correction server
"""

import os
import sys

# Ensure src/ is on the path for direct execution.
src_path = os.path.join(os.path.dirname(__file__), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from vision_fsm_agent.cli import main as cli_main


if __name__ == "__main__":
    cli_main(sys.argv[1:])
