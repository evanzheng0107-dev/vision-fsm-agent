# Agent API Reference

## `DecisionAgent`

Abstract base class for decision agents.

```python
class DecisionAgent:
    def get_decision(self, agent_state: dict) -> dict: ...
```

## `LocalDecisionAgent`

A deterministic, rule-based agent. No network or API keys required.

### Constructor

```python
LocalDecisionAgent(failure_threshold: int = 3)
```

### Decision Priority

| Priority | Action | Condition |
|----------|--------|-----------|
| 1 | `interact` | An actionable element was detected |
| 2 | `pickup` | A collectible was detected |
| 3 | `move` | A navigation target was detected |
| 4 | `wait` | `failed_attempts > failure_threshold` |
| 5 | `explore` | Nothing detected, no failures |

### `get_decision(agent_state)`

```python
agent_state = {
    "match_results": {
        "interact": {"found": True/False, "confidence": float},
        "pickup": {"found": True/False, "confidence": float},
        "target": {"found": True/False, "confidence": float},
    },
    "failed_attempts": int,
    "current_state": str,  # FSM state
}

# Returns:
{"action": "move|pickup|interact|explore|wait|continue", "reason": str}
```

## `CloudDecisionAgent`

Optional LLM-backed agent. Falls back to `LocalDecisionAgent` when no
API key is set or a request fails.

### Constructor

```python
CloudDecisionAgent(fallback: DecisionAgent | None = None)
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_API_KEY` | — | API key (if unset, uses fallback) |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `LLM_MODEL` | `gpt-3.5-turbo` | Model name |

## `ACTIONS`

The canonical action vocabulary (tuple):

```python
ACTIONS = ("move", "pickup", "interact", "explore", "wait", "continue")
```

## Example

```python
from agent import LocalDecisionAgent

agent = LocalDecisionAgent(failure_threshold=3)
decision = agent.get_decision({
    "match_results": {"target": {"found": True}},
    "failed_attempts": 0,
})
# decision == {"action": "move", "reason": "navigation target detected"}
```
