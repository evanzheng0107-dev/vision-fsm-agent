# Examples

Standalone examples showing how to use the Vision FSM Agent framework.
All examples are self-contained, require no external software, and can be
verified with `pytest tests/smoke/`.

## Quick navigation

| Example | What it shows | Command |
|---------|---------------|---------|
| [Visual Grid World](#visual_grid_world) | Full agent pipeline in a synthetic grid | `python examples/visual_grid_world/run_demo.py --steps 35` |
| [Custom FSM](#custom_fsmcustom_fsmpy) | Building your own FSM topology | `python examples/custom_fsm/custom_fsm.py` |

## Prerequisites

All examples need:
- Python 3.9+
- `pip install -r requirements.txt` (opencv-python, numpy, pyyaml, flask)
- Generated assets: `python scripts/generate_demo_assets.py`

> The demo assets are 100% programmatically generated — no downloads, no
> third-party content. See `examples/visual_grid_world/assets/README.md`.

## visual_grid_world/

The default demo — a 12×12 grid world with goals, items, and buttons.
The agent navigates, collects, and interacts — all driven by real template
matching and FSM transitions.

```bash
python examples/visual_grid_world/run_demo.py --steps 35
```

Key features:
- **Deterministic** — same seed produces the same run every time
- **Headless** — no GUI, no screen capture
- **Reproducible** — all frames rendered with OpenCV/numpy drawing primitives

See [`visual_grid_world/README.md`](visual_grid_world/README.md) for
configuration options, expected output, and frame-saving instructions.

## custom_fsm/custom_fsm.py

Demonstrates building a **custom FSM topology** (PATROL ↔ SCAN, with a WAIT
fallback) and driving it with the vision engine and the demo environment.

```bash
python examples/custom_fsm/custom_fsm.py
```

### FSM topology

```
SPOTTED          DONE
PATROL ──────> SCAN ──────> PATROL
  │                            ↑
  │ STUCK                READY │
  └─────> WAIT ────────────────┘
```

### Expected output (abbreviated)

```
Initial state: PATROL
Available events: ['SPOTTED', 'STUCK']
Loaded 3 templates: ['interact_button', 'pickup_item', 'target_goal']

  step  1 | PATROL --[SPOTTED]--> SCAN       | best=pickup_item(0.94) pos=(0, 0)
  step  1 | SCAN   --[DONE]--> PATROL        | pos=(1, 1)
  ...
  step  6 | PATROL --[STUCK]--> WAIT         | (no vision) pos=(3, 5)
  step  6 | WAIT   --[READY]--> PATROL       | (recovered) pos=(3, 5)
  step  8 | PATROL --[SPOTTED]--> SCAN       | best=pickup_item(0.94) pos=(1, 5)
  step  8 | SCAN   --[DONE]--> PATROL        | pos=(2, 6)

Transition history (16 transitions):
  PATROL   --[SPOTTED]--> SCAN
  SCAN     --[DONE]--> PATROL
  ...
  PATROL   --[STUCK]--> WAIT
  WAIT     --[READY]--> PATROL
```

### Key takeaways

- The FSM is fully configurable — you define your own states and transitions.
- `TemplateManager` loads templates from any directory.
- `DemoEnvironment` provides reproducible frames for testing.
- Vision results (`MatchResult`) can be used to fire FSM events directly.
- `fsm.history` records every transition for debugging and audit.
- The WAIT fallback demonstrates graceful degradation when vision is
  temporarily unavailable (steps 6–7 simulate a sensor outage).

## Verifying the examples

All examples are covered by smoke tests that run in CI:

```bash
pytest tests/smoke/ -v
```

This runs:
- `test_demo_run.py` — verifies the grid world demo produces expected output
- `test_custom_fsm.py` — verifies the custom FSM example runs and exercises
  both normal and fallback paths
- `test_examples_independent.py` — verifies examples run from their own
  directories and the 35-step demo completes all objectives

## More examples (planned)

- `custom_environment.py` — implementing your own `Environment`
- `hil_correction.py` — running the agent with a live HIL server
- `cloud_decision.py` — using an LLM-backed decision agent

See the [project roadmap](../../README.md#12-roadmap) and open
[issues](https://github.com/evanzheng0107-dev/vision-fsm-agent/issues)
for planned work.
