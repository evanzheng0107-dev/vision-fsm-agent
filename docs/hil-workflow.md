# HIL Workflow

Human-in-the-Loop (HIL) is the mechanism by which a human operator can
**override** or **correct** an autonomous agent in real time. This
document describes the protocol, API, and usage patterns.

## Concept

```
┌────────────┐                        ┌──────────────┐                        ┌──────────────┐
│   Human    │  POST /set_correction  │  HIL Server  │  GET /get_correction   │    Agent     │
│  Operator  │ ─────────────────────> │   (Flask)    │ <───────────────────── │    Loop      │
└────────────┘                        └──────────────┘                        └──────────────┘
                                            ▲                                       │
                                            │  POST /send_correction (learn)        │
                                            └───────────────────────────────────────┘
```

1. The **operator** pushes a correction to the HIL server.
2. The **agent** polls the server on each loop iteration.
3. If a correction is pending, the agent **applies it immediately** and
   **forwards it** to the decision agent for learning.
4. Corrections are **one-shot**: once consumed, they are cleared.

## Starting the HIL Server

```bash
python run.py --hil
# HIL server available at http://localhost:8001/hil
```

The server binds to `0.0.0.0:8001` by default. In a shared environment,
restrict access via firewall or reverse proxy.

## API Reference

All endpoints are under `/hil`.

### `GET /hil/status`

Returns server health and counters.

```json
{
  "status": "running",
  "timestamp": 1719600000.0,
  "correction_count": 3,
  "learning_count": 2,
  "status_count": 150,
  "has_pending_correction": false
}
```

### `POST /hil/set_correction`

Push a correction for the agent to consume on its next poll.

**Request body:**
```json
{
  "type": "correct",
  "action": "click",
  "scene": "demo_grid",
  "correct_params": {"x": 150, "y": 220},
  "reason": "offset caused a miss"
}
```

**Required fields:** `type`, `action`, `correct_params`

**Supported actions:**
| Action | `correct_params` | Effect |
|--------|-------------------|--------|
| `click` | `{"x": int, "y": int}` | Agent performs a click at (x, y) |
| `stop` | — | Agent stops the loop |
| `reset` | — | Agent resets its FSM and failure counters |

**Response:** `{"status": "success", "message": "correction stored"}`

### `GET /hil/get_correction`

Pop the next pending correction (one-shot).

- If a correction is pending: returns the correction object and clears it.
- If none: returns `{"type": "none", "message": "no correction pending"}`

### `POST /hil/send_correction`

Forward an applied correction to the decision agent for learning
(agent → server). The correction is recorded in the learning history.

**Request body:**
```json
{
  "type": "manual_correction",
  "script_id": "vision_fsm_agent",
  "correction": { ... },
  "timestamp": 1719600000.0
}
```

### `POST /hil/send_status`

Report the agent's current state (agent → server). Recorded for
monitoring and analysis.

### `POST /hil/get_decision`

Stub endpoint. Returns a conservative `continue` decision. In a real
deployment, this could consult recorded learning data or an external
model.

### `POST /hil/reset`

Clear all in-memory stores (corrections, learning data, status history).
Useful for tests.

## Enabling HIL in the Agent

HIL is **disabled by default**. To enable it, pass `use_hil=True` to the
`AgentLoop`, or use `--hil` flag conceptually (the HIL server and agent
run as separate processes):

```python
from main import AgentLoop, load_config
from visual_grid_world import DemoEnvironment

config = load_config()
env = DemoEnvironment(config)
loop = AgentLoop(env, config, use_hil=True)  # enables HIL polling
loop.run(max_steps=50)
```

When HIL is enabled but the server is not running, the agent logs a
debug message and continues autonomously — it never blocks.

## Correction Validation

The `HilClient` validates incoming corrections:

- `type: "none"` is always valid (no-op)
- `type: "correct"` requires `action` and `correct_params`
- `action: "click"` requires `x` and `y` in `correct_params`

Malformed corrections are logged and discarded.

## Testing HIL

The HIL server can be tested without a live HTTP server using Flask's
test client:

```python
from hil_server import app

with app.test_client() as client:
    client.post("/hil/set_correction", json={
        "type": "correct", "action": "click",
        "correct_params": {"x": 10, "y": 20}
    })
    resp = client.get("/hil/get_correction")
    assert resp.get_json()["action"] == "click"
```

See `tests/integration/test_hil.py` for the full test suite.
