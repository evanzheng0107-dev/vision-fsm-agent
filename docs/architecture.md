# Architecture

This document describes the internal architecture of Vision FSM Agent and
how the components interact.

## Overview

The framework follows a **layered pipeline** architecture:

```
Environment → Vision → FSM → Decision → (HIL) → Action → Environment
```

Each layer is an independent module with a clear interface. The agent
loop (`src/vision_fsm_agent/main.py`) orchestrates them.

## Layers

### 1. Environment Layer

An `Environment` is anything that can:
- Produce a **frame** (a `np.ndarray` BGR image)
- **Execute an action** (e.g. `move`, `pickup`, `interact`)
- Report its **bounds** (width, height in pixels)

```python
class Environment(Protocol):
    def get_frame(self) -> np.ndarray | None: ...
    def perform_action(self, action: str, params: dict | None = None) -> None: ...
    @property
    def bounds(self) -> tuple: ...
    def close(self) -> None: ...
```

Two implementations ship with the project:

| Implementation | File | Description |
|---|---|---|
| `DemoEnvironment` | `src/vision_fsm_agent/envs/grid_world.py` | Synthetic grid world; **default**; no I/O |
| `LiveEnvironment` | `src/vision_fsm_agent/main.py` | Screen capture (`mss`) + mouse input (`pyautogui`); **opt-in** |

### 2. Vision Layer (`src/vision_fsm_agent/vision.py`)

The vision layer wraps OpenCV's `cv2.matchTemplate` with:

- **Multi-scale matching**: tries `scale_steps` evenly spaced scales
  between `scale_range[0]` and `scale_range[1]`. This makes matching
  robust to size variation.
- **`TemplateManager`**: holds a collection of named grayscale templates
  and can match one, the best, or all against a frame.
- **`MatchResult`**: structured output containing `found`, `confidence`,
  `position`, `center`, and the matched template name.

```python
mgr = TemplateManager(confidence_threshold=0.75)
mgr.load_directory("examples/visual_grid_world/assets")
results = mgr.match_all(frame)  # sorted by confidence, descending
```

The demo templates are **programmatically generated** by
`scripts/generate_demo_assets.py` using the same drawing primitives the
`DemoEnvironment` uses to render frames. This guarantees pixel-accurate
matches.

### 3. FSM Layer (`src/vision_fsm_agent/fsm.py`)

A generic, dependency-free finite-state machine:

- **States**: arbitrary strings (e.g. `"IDLE"`, `"MOVE"`)
- **Transitions**: `(source, event, target)` rules with optional **guards**
  (predicates that allow/block) and **actions** (side-effect callbacks)
- **Callbacks**: `on_enter(state, cb)` and `on_exit(state, cb)`
- **History**: a bounded deque of `TransitionRecord` for debugging/tests
- **`force_state`**: direct state jump for HIL corrections and resets
- **`reset`**: return to the initial state and clear history

```python
fsm = FiniteStateMachine("IDLE")
fsm.add_transition("IDLE", "FOUND_TARGET", "MOVE", guard=my_guard)
fsm.on_enter("MOVE", lambda fsm, p: print("now moving"))
fsm.fire("FOUND_TARGET", payload={"target": (5, 3)})
```

### 4. Decision Layer (`src/vision_fsm_agent/agent.py`)

Two interchangeable agents implementing a common `get_decision(state)`
interface:

**`LocalDecisionAgent`** (default, offline):
- Priority: `interact` > `pickup` > `move` > `wait` (on failures) > `explore`
- Deterministic and side-effect-free
- No configuration required

**`CloudDecisionAgent`** (optional, LLM-backed):
- Calls an OpenAI-compatible chat completions endpoint
- Configured via `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` env vars
- **Falls back** to `LocalDecisionAgent` when no key is set or a request
  fails — the agent loop never blocks

### 5. HIL Layer (`src/vision_fsm_agent/hil/client.py`, `src/vision_fsm_agent/hil/server.py`)

A Flask server brokers corrections between a human and the agent:

- The **agent** polls `GET /hil/get_correction` each iteration
- The **operator** pushes corrections via `POST /hil/set_correction`
- Applied corrections are forwarded via `POST /hil/send_correction` for
  "learning" (recorded for analysis)
- The agent reports its state via `POST /hil/send_status`

HIL is **fully optional**. If the server is down, the agent continues
autonomously.

### 6. Agent Loop (`src/vision_fsm_agent/main.py::AgentLoop`)

The orchestrator that ties everything together:

```
for each step:
    1. Poll HIL for corrections (if enabled)
    2. Capture a frame from the environment
    3. Match all templates (vision)
    4. Classify matches into semantic categories
    5. Build agent state
    6. Get a decision from the agent
    7. Apply the decision (fire FSM events + environment action)
    8. Resolve FSM back toward IDLE
    9. Sleep (loop_delay)
```

The loop includes **failure-retry logic**: after `max_failed_attempts`
consecutive frame-capture failures, the FSM enters `WAIT` and resets the
counter.

## Dependency Graph

```
main.py
  ├── fsm.py          (no deps)
  ├── vision.py       (opencv, numpy)
  ├── agent.py        (requests, optional)
  ├── hil_client.py   (requests)
  └── hil_server.py   (flask)

src/vision_fsm_agent/envs/grid_world.py
  └── (opencv, numpy)  — imports main.py at runtime
```

Core framework dependencies are minimal: `opencv-python`, `numpy`,
`pyyaml`, `flask`, `requests`. Heavy/optional dependencies (`mss`,
`pyautogui`, `keyboard`) are only needed for `LiveEnvironment` and are
commented out in `requirements.txt` by default.

## Design Principles

1. **Generic by default** — no domain knowledge baked into the core.
2. **Demo-first** — everything runs against the synthetic demo out of the
   box.
3. **Optional everything** — HIL, cloud decisions, and live capture are
   all opt-in.
4. **Reproducible** — the demo is seeded and deterministic.
5. **Safe** — no anti-detection, no evasion, no third-party targeting.
