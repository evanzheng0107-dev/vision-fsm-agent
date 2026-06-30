"""
Vision FSM Agent - A lightweight Python framework for building
computer-vision-driven automation agents with finite-state-machine
control and human-in-the-loop correction.

Public modules:
    vision      - Template-matching based computer-vision engine
    fsm         - Generic finite-state-machine engine
    hil_client  - Human-in-the-loop correction client
    hil_server  - Human-in-the-loop correction server (Flask)
    agent       - Decision agent (local rules + optional cloud)
    main        - Generic agent main loop (defaults to demo mode)

See README.md and docs/ for usage and safety boundaries.
"""

__version__ = "0.1.0"
__all__ = ["vision", "fsm", "hil_client", "hil_server", "agent", "main"]
