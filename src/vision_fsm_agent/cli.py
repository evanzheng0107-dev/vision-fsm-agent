"""
Command-line interface for Vision FSM Agent.

Usage::

    vision-fsm-agent --start            # demo mode (default)
    vision-fsm-agent --start --steps 30 # specify step count
    vision-fsm-agent --start --live     # live screen capture (advanced)
    vision-fsm-agent --hil              # start the HIL correction server
"""

from __future__ import annotations

import sys


def main(argv=None) -> None:
    """CLI entry: ``vision-fsm-agent [--start] [--live] [--hil] [--steps N]``."""
    argv = argv if argv is not None else sys.argv[1:]

    if "--hil" in argv:
        from .hil.server import run as run_hil

        print("Starting HIL correction server...")
        print("Endpoint: http://localhost:8001/hil")
        run_hil()
        return

    use_hil = "--hil" in argv
    live = "--live" in argv

    from .config import load_config

    config = load_config()

    max_steps = int(config.get("demo_max_steps", 50))
    if "--steps" in argv:
        idx = argv.index("--steps")
        if idx + 1 < len(argv):
            try:
                max_steps = int(argv[idx + 1])
            except ValueError:
                pass

    if live:
        from .main import run_live

        run_live(config, use_hil=use_hil)
    else:
        from .main import run_demo

        run_demo(config, max_steps=max_steps, use_hil=use_hil)


if __name__ == "__main__":  # pragma: no cover
    main()
