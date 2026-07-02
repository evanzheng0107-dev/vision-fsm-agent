"""
Example: building a custom FSM and driving it with the vision engine.

This example demonstrates how to combine the framework's modules to build
your own agent — without using the default demo FSM. It shows:

  1. Defining a custom FSM topology (PATROL ↔ SCAN, with a WAIT fallback)
  2. Loading templates with TemplateManager
  3. Rendering frames with DemoEnvironment
  4. Using vision results to fire FSM events
  5. Reading the transition history for debugging

Run::

    python examples/custom_fsm/custom_fsm.py

Expected output (abbreviated)::

    Initial state: PATROL
    Available events: ['SPOTTED', 'STUCK']
    Loaded 3 templates: ['interact_button', 'pickup_item', 'target_goal']

      step  1 | PATROL --[SPOTTED]--> SCAN   | best=pickup_item(0.94) pos=(1,1)
      step  2 | PATROL --[SPOTTED]--> SCAN   | best=pickup_item(0.94) pos=(2,2)
      ...
      step  6 | PATROL --[STUCK]--> WAIT     | (no vision)            pos=(3,6)
      step  7 | WAIT   --[READY]--> PATROL   | (recovered)            pos=(3,6)
      step  8 | PATROL --[SPOTTED]--> SCAN   | best=pickup_item(0.94) pos=(3,7)

    Transition history (10 transitions):
      PATROL --[SPOTTED]--> SCAN
      SCAN   --[DONE]--> PATROL
      ...
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
    """A custom FSM: PATROL <-> SCAN with a WAIT fallback.

    Topology::

        SPOTTED          DONE
      PATROL ──────> SCAN ──────> PATROL
        │                              ↑
        │ STUCK                  READY │
        └─────> WAIT ──────────────────┘
    """
    fsm = FiniteStateMachine("PATROL")
    fsm.add_transition("PATROL", "SPOTTED", "SCAN", description="element detected")
    fsm.add_transition("SCAN", "DONE", "PATROL", description="scan complete")
    fsm.add_transition("SCAN", "LOST", "PATROL", description="element disappeared")
    fsm.add_transition("PATROL", "STUCK", "WAIT", description="no progress")
    fsm.add_transition("WAIT", "READY", "PATROL", description="recovered")
    return fsm


def _print_step(step: int, fsm: FiniteStateMachine, label: str, extra: str) -> None:
    """Print one step in a compact, aligned format."""
    print(f"  step {step:>2} | {label:<32} | {extra}")


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

    # 4. Run a few steps.
    #    To demonstrate the WAIT fallback, we simulate a "sensor outage"
    #    on steps 6-7: the agent skips vision and fires STUCK → READY.
    sensor_outage_steps = {6, 7}

    for step in range(1, 9):
        pos = env.agent_pos

        if step in sensor_outage_steps:
            # Simulated sensor outage: no vision, agent is stuck.
            fsm.fire("STUCK")
            _print_step(step, fsm, "PATROL --[STUCK]--> WAIT", f"(no vision) pos={pos}")
            fsm.fire("READY")
            _print_step(step, fsm, "WAIT   --[READY]--> PATROL", f"(recovered) pos={pos}")
            env.perform_action("explore")
            continue

        # Normal step: run vision.
        frame = env.get_frame()
        best = vision.match_best(frame)

        if best.found:
            fsm.fire(
                "SPOTTED", payload={"template": best.template_name, "confidence": best.confidence}
            )
            _print_step(
                step,
                fsm,
                "PATROL --[SPOTTED]--> SCAN",
                f"best={best.template_name}({best.confidence:.2f}) pos={pos}",
            )
            env.perform_action("pickup" if "pickup" in best.template_name else "move")
            fsm.fire("DONE")
            _print_step(step, fsm, "SCAN   --[DONE]--> PATROL", f"pos={env.agent_pos}")
        else:
            env.perform_action("explore")
            _print_step(step, fsm, "PATROL (no match)", f"pos={env.agent_pos}")

    # 5. Show transition history
    print(f"\nTransition history ({len(fsm.history)} transitions):")
    for rec in fsm.history:
        print(f"  {rec.source:<8} --[{rec.event}]--> {rec.target}")


if __name__ == "__main__":
    main()
