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

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def main() -> None:
    src_path = os.path.join(os.path.dirname(__file__), "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    if "--hil" in sys.argv:
        from hil_server import run as run_hil

        print("Starting HIL correction server...")
        print("Endpoint: http://localhost:8001/hil")
        run_hil()
        return

    # Default: demo mode
    from main import main as agent_main

    agent_main(sys.argv[1:])


if __name__ == "__main__":
    main()
