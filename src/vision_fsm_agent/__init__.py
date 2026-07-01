"""
Vision FSM Agent - A lightweight Python framework for building
computer-vision-driven automation agents with finite-state-machine
control and human-in-the-loop correction.

Public modules:
    vision_fsm_agent.vision      - Template-matching based computer-vision engine
    vision_fsm_agent.fsm         - Generic finite-state-machine engine
    vision_fsm_agent.agent       - Decision agents (local rules + optional cloud)
    vision_fsm_agent.hil         - Human-in-the-loop correction (client + server)
    vision_fsm_agent.main        - Generic agent main loop (defaults to demo mode)
    vision_fsm_agent.config      - Configuration loading and validation
    vision_fsm_agent.cli         - Command-line interface
    vision_fsm_agent.envs        - Environments (DemoEnvironment, LiveEnvironment)

See README.md and docs/ for usage and safety boundaries.
"""

__version__ = "0.1.0"

# Lazy imports to avoid pulling OpenCV/numpy at package import time.
# Use ``from vision_fsm_agent import fsm`` etc. when needed.
__all__ = [
    "vision",
    "fsm",
    "agent",
    "main",
    "config",
    "cli",
    "hil",
    "envs",
    "decision",
    "actions",
    "utils",
]
