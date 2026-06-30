# API Reference

This section documents the public API of Vision FSM Agent's core modules.

## Modules

| Module | Description | Key Classes |
|--------|-------------|-------------|
| [`fsm`](fsm.md) | Generic finite-state-machine engine | `FiniteStateMachine`, `Transition`, `TransitionRecord` |
| [`vision`](vision.md) | Multi-scale OpenCV template matching | `TemplateManager`, `MatchResult`, `multi_scale_match` |
| [`agent`](agent.md) | Decision agents (local + cloud) | `DecisionAgent`, `LocalDecisionAgent`, `CloudDecisionAgent` |
| [`hil`](hil.md) | Human-in-the-loop correction | `HilClient`, HIL server endpoints |

## Import Convention

The framework uses flat imports (modules are added to `sys.path`):

```python
from fsm import FiniteStateMachine
from vision import TemplateManager, MatchResult
from agent import LocalDecisionAgent
from hil_client import HilClient
```

## Version

```python
import src
print(src.__version__)  # "0.1.0"
```

## Quick Example

```python
from fsm import FiniteStateMachine
from vision import TemplateManager
from agent import LocalDecisionAgent

# Build an FSM
fsm = FiniteStateMachine("IDLE")
fsm.add_transition("IDLE", "FOUND", "ACTIVE")

# Load templates
vision = TemplateManager(confidence_threshold=0.75)
vision.load_directory("assets/demo")

# Decide
agent = LocalDecisionAgent()
results = vision.match_all(frame)
decision = agent.get_decision({"match_results": {...}})
```

See each module's page for full API details.
