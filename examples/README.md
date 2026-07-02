# Examples

Standalone examples showing how to use the Vision FSM Agent framework.

## custom_fsm.py

Demonstrates building a **custom FSM topology** (PATROL ↔ SCAN) and driving
it with the vision engine and the demo environment.

```bash
python examples/custom_fsm.py
```

Key takeaways:
- The FSM is fully configurable — you define your own states and transitions.
- `TemplateManager` loads templates from any directory.
- `DemoEnvironment` provides reproducible frames for testing.
- Vision results (`MatchResult`) can be used to fire FSM events directly.

## More examples (planned)

- `custom_environment.py` — implementing your own `Environment`
- `hil_correction.py` — running the agent with a live HIL server
- `cloud_decision.py` — using an LLM-backed decision agent
