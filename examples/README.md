# Examples

Standalone examples showing how to use the Vision FSM Agent framework.

## custom_fsm/custom_fsm.py

Demonstrates building a **custom FSM topology** (PATROL ↔ SCAN, with a WAIT
fallback) and driving it with the vision engine and the demo environment.

```bash
python examples/custom_fsm/custom_fsm.py
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

## visual_grid_world/

The default demo — a 12×12 grid world with goals, items, and buttons.
See [`visual_grid_world/README.md`](visual_grid_world/README.md) for details.

```bash
python examples/visual_grid_world/run_demo.py --steps 35
```

## More examples (planned)

- `custom_environment.py` — implementing your own `Environment`
- `hil_correction.py` — running the agent with a live HIL server
- `cloud_decision.py` — using an LLM-backed decision agent
