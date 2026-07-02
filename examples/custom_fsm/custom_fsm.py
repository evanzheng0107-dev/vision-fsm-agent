"""
Example: building a custom FSM and driving it with the vision engine.

This example demonstrates how to combine the framework's modules to build
your own agent — without using the default demo FSM. It shows:

  1. Defining a custom FSM topology (a simple PATROL <-> SCAN loop)
  2. Loading templates with TemplateManager
  3. Rendering frames with DemoEnvironment
  4. Using vision results to fire FSM events

Run::

    python examples/custom_fsm/custom_fsm.py
"""

import os
import sys

# Ensure src/ is importable.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from vision_fsm_agent.envs.grid_world import DemoEnvironment  # noqa: E402
from vision_fsm_agent.fsm import FiniteStateMachine  # noqa: E402
from vision_fsm_agent.vision import TemplateManager  # noqa: E402


def build_patrol_fsm() -> FiniteStateMachine:
    """A custom FSM: PATROL <-> SCAN with a WAIT fallback."""
    fsm = FiniteStateMachine("PATROL")
    fsm.add_transition("PATROL", "SPOTTED", "SCAN", description="element detected")
    fsm.add_transition("SCAN", "DONE", "PATROL", description="scan complete")
    fsm.add_transition("SCAN", "LOST", "PATROL", description="element disappeared")
    fsm.add_transition("PATROL", "STUCK", "WAIT", description="no progress")
    fsm.add_transition("WAIT", "READY", "PATROL", description="recovered")
    return fsm


def main() -> None:
    # 1. Custom FSM
    fsm = build_patrol_fsm()
    print(f"Initial state: {fsm.current_state}")
    print(f"Available events: {fsm.available_events()}")

    # 2. Vision
    vision = TemplateManager(confidence_threshold=0.7)
    assets_dir = os.path.join(ROOT, "examples", "visual_grid_world", "assets")
    vision.load_directory(assets_dir)
    print(f"Loaded {len(vision)} templates: {vision.names}")

    # 3. Environment
    env = DemoEnvironment({"demo_seed": 7})

    # 4. Run a few steps
    for step in range(8):
        frame = env.get_frame()
        best = vision.match_best(frame)

        if best.found:
            fsm.fire(
                "SPOTTED", payload={"template": best.template_name, "confidence": best.confidence}
            )
            env.perform_action("pickup" if "pickup" in best.template_name else "move")
            fsm.fire("DONE")
        else:
            env.perform_action("explore")
            if step > 3:
                fsm.fire("STUCK")
                fsm.fire("READY")

        print(
            f"  step {step + 1}: state={fsm.current_state:<8} "
            f"best={best.template_name}({best.confidence:.2f}) "
            f"pos={env.agent_pos}"
        )

    # 5. Show transition history
    print(f"\nTransition history ({len(fsm.history)} transitions):")
    for rec in fsm.history:
        print(f"  {rec.source} --[{rec.event}]--> {rec.target}")


if __name__ == "__main__":
    main()
