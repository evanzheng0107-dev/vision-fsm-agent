# HIL API Reference

## Client: `HilClient`

HTTP client for the HIL correction server.

### Constructor

```python
HilClient(config: dict | None = None)
```

Config keys: `hil_server_url`, `script_id`.

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_manual_correction()` | `dict \| None` | Poll for a pending correction |
| `send_status(status)` | `bool` | Report agent state to server |
| `send_correction_to_agent(correction)` | `bool` | Forward correction for learning |
| `get_agent_decision(agent_state)` | `dict \| None` | Request a learned decision |

## Server Endpoints

All endpoints are under `/hil`.

### `GET /hil/get_correction`

Pop the next pending correction (one-shot).

**Response** (correction pending):
```json
{
  "type": "correct",
  "action": "click",
  "correct_params": {"x": 150, "y": 220},
  "reason": "offset caused a miss"
}
```

**Response** (nothing pending):
```json
{"type": "none", "message": "no correction pending"}
```

### `POST /hil/set_correction`

Push a correction for the agent to consume.

**Request body:**
```json
{
  "type": "correct",
  "action": "click|stop|reset",
  "correct_params": {"x": int, "y": int},
  "reason": "string"
}
```

### `POST /hil/send_correction`

Record a correction as learning data (agent → server).

### `POST /hil/send_status`

Report agent state (agent → server).

### `POST /hil/get_decision`

Stub endpoint returning a conservative `continue` decision.

### `GET /hil/status`

Server health and counters:
```json
{
  "status": "running",
  "correction_count": 3,
  "learning_count": 2,
  "has_pending_correction": false
}
```

### `POST /hil/reset`

Clear all in-memory stores (for testing).

## Correction Actions

| Action | `correct_params` | Effect |
|--------|-------------------|--------|
| `click` | `{"x": int, "y": int}` | Agent clicks at (x, y) |
| `stop` | — | Agent stops the loop |
| `reset` | — | Agent resets FSM and counters |

## Example

```python
from hil_client import HilClient

client = HilClient({"hil_server_url": "http://localhost:8001/hil"})
correction = client.get_manual_correction()
if correction and correction.get("type") == "correct":
    print(f"Applying: {correction['action']}")
```
