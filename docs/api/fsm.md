# FSM API Reference

## `FiniteStateMachine`

A generic finite-state machine with guards, actions, and callbacks.

### Constructor

```python
FiniteStateMachine(initial_state: str, history_limit: int = 200)
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_transition(source, event, target, *, guard=None, action=None, description="")` | `self` | Register a transition rule |
| `on_enter(state, callback)` | `self` | Register an on-enter callback |
| `on_exit(state, callback)` | `self` | Register an on-exit callback |
| `fire(event, payload=None)` | `bool` | Attempt a transition; `True` if it occurred |
| `force_state(state, payload=None)` | `None` | Directly jump to a state (for HIL/reset) |
| `reset()` | `None` | Return to initial state, clear history |
| `can_fire(event)` | `bool` | Whether an event is valid from current state |
| `available_events()` | `list[str]` | Events valid from current state |
| `blocked_count(source, event)` | `int` | Times a guard blocked this (source, event) |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `current_state` | `str` | The current state |
| `initial_state` | `str` | The initial state |
| `history` | `list[TransitionRecord]` | Past transitions |

## `Transition`

A transition rule (dataclass).

| Field | Type | Description |
|-------|------|-------------|
| `source` | `str` | Source state |
| `event` | `str` | Triggering event |
| `target` | `str` | Target state |
| `guard` | `Guard \| None` | Predicate that allows/blocks |
| `action` | `Action \| None` | Side-effect callback |
| `description` | `str` | Human-readable note |

## `TransitionRecord`

An entry in the FSM history (dataclass).

| Field | Type | Description |
|-------|------|-------------|
| `source` | `str` | Source state |
| `event` | `str` | Event that fired |
| `target` | `str` | Target state |
| `payload` | `dict` | Event payload |

## Type Aliases

```python
Guard = Callable[[FiniteStateMachine, dict], bool]
Action = Callable[[FiniteStateMachine, dict], None]
```

## Example

```python
from fsm import FiniteStateMachine

fsm = FiniteStateMachine("IDLE")
fsm.add_transition("IDLE", "START", "RUNNING",
                   guard=lambda f, p: p.get("ready"))
fsm.on_enter("RUNNING", lambda f, p: print("Started!"))

assert fsm.fire("START", {"ready": False}) is False  # blocked
assert fsm.fire("START", {"ready": True}) is True    # fires
```
