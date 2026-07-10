# Vision FSM Agent

> A lightweight Python framework for building computer-vision-driven automation agents with finite-state-machine control and human-in-the-loop correction.

一个用于研究和教学的 **计算机视觉 + 有限状态机 + HIL 人工纠正** Agent 框架。

[![Tests](https://github.com/evanzheng0107-dev/vision-fsm-agent/actions/workflows/test.yml/badge.svg)](https://github.com/evanzheng0107-dev/vision-fsm-agent/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## Table of Contents

1. [What is this?](#1-what-is-this)
2. [Who is it for?](#2-who-is-it-for)
3. [What it is NOT for](#3-what-it-is-not-for)
4. [Quick Start](#4-quick-start)
5. [Demo Environment](#5-demo-environment)
6. [Architecture](#6-architecture)
7. [FSM States](#7-fsm-states)
8. [HIL Workflow](#8-hil-workflow)
9. [Development Setup](#9-development-setup)
10. [Testing](#10-testing)
11. [Safety Boundaries](#11-safety-boundaries)
12. [Roadmap](#12-roadmap)
13. [Contributing](#13-contributing)

---

## 1. What is this?

**Vision FSM Agent** is a minimal, dependency-light framework that combines
three classic automation building blocks:

| Building block | Module | What it does |
|---|---|---|
| **Computer Vision** | `vision_fsm_agent.vision` | Multi-scale OpenCV template matching with configurable thresholds |
| **Finite-State Machine** | `vision_fsm_agent.fsm` | Generic FSM with guards, actions, callbacks, and transition history |
| **Human-in-the-Loop** | `vision_fsm_agent.hil` | HTTP-based correction channel so a human can override the agent in real time |

These are wired together by a generic **agent loop** (`vision_fsm_agent.main`)
that drives an **Environment** — an interface you can implement for any
target. The project ships with a **synthetic demo environment** so you can
run the entire pipeline with zero external setup.

## 2. Who is it for?

- **Students and educators** learning about CV-based automation, FSM
  design, or human-in-the-loop systems.
- **Researchers** prototyping vision-driven agents in a reproducible,
  controlled setting.
- **Developers** who want a clean, readable starting point for building
  their own CV+FSM automation — and want to understand every line.

## 3. What it is NOT for

> **Read this before using the project.**

This project is **not** intended for:

- ❌ Cheating in games or circumventing anti-cheat systems
- ❌ Botting or automating third-party services without permission
- ❌ Bypassing platform rules, terms of service, or access controls
- ❌ Any activity that violates applicable laws or regulations

The default demo runs against a **local synthetic environment** — it does
not capture your screen, send input to external software, or access the
network (except the optional local HIL server). See
[Safety Boundaries](#11-safety-boundaries) and
[`docs/safety-boundaries.md`](docs/safety-boundaries.md).

## 4. Quick Start

**Run the demo in under a minute** — no game, no screen capture, no
external software required:

```bash
git clone https://github.com/evanzheng0107-dev/vision-fsm-agent.git
cd vision-fsm-agent
pip install -r requirements.txt
python scripts/generate_demo_assets.py
python examples/visual_grid_world/run_demo.py --steps 15
```

You should see output like:

```
[demo] World: 12x12, goals=[(3, 2), (6, 5)], items=3, buttons=1
[demo] Running 15 steps...

  step   1 | fsm=IDLE     pos=(1, 1) | items[...] buttons[.]
  step   2 | fsm=IDLE     pos=(2, 2) | items[...] buttons[.]
  step   3 | fsm=IDLE     pos=(3, 2) | items[...] buttons[.]
  ...
  step   8 | fsm=IDLE     pos=(7, 2) | items[...] buttons[B]
  ...
  step  15 | fsm=IDLE     pos=(3, 8) | items[I..] buttons[B]

[demo] Final status: done=False, items_collected=1/3, buttons_pressed=1/1
```

The agent navigates a 12×12 grid world, collecting items and pressing
buttons — all driven by real template matching and FSM transitions.

### More thorough setup

If you plan to develop or contribute, install with dev dependencies:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

Then use the Makefile for common tasks:

```bash
make test      # Run the test suite (66 tests)
make demo      # Run the demo
make lint      # Run the linter
make check     # Run the readiness check
```

### Launcher

```bash
python run.py --start            # demo mode (default)
python run.py --start --steps 30 # specify step count
python run.py --hil              # start the HIL correction server
```

### Next steps

- [`docs/demo.md`](docs/demo.md) — detailed demo walkthrough and configuration
- [`examples/custom_fsm/`](examples/custom_fsm/) — build your own FSM topology
- [`docs/architecture.md`](docs/architecture.md) — framework architecture deep dive
- [`docs/troubleshooting.md`](docs/troubleshooting.md) — common issues and solutions

## 5. Demo Environment

The demo (`examples/visual_grid_world/run_demo.py`) is a **fully synthetic,
headless, reproducible** environment:

- A 12×12 grid world rendered to a BGR image with OpenCV/numpy
- **Goals** (green crosshairs) — navigation targets
- **Items** (gold circles) — collectibles
- **Buttons** (blue squares) — interactable elements
- An **agent** (red diamond) that moves, collects, and interacts

Each frame uses the **same drawing primitives** that generate the template
images in `examples/visual_grid_world/assets/`. This guarantees that template
matching actually finds the elements — making the demo a genuine end-to-end
test of the vision pipeline.

The world is **deterministic** given the same seed (`demo_seed: 42` by
default), so runs are reproducible. Edit
`examples/visual_grid_world/config.yaml` to change the grid size, random seed,
or confidence threshold.

```bash
# Save frames as PNGs for inspection
python examples/visual_grid_world/run_demo.py --save demo_frames --steps 20

# Generate fresh template assets
python scripts/generate_demo_assets.py
```

## 6. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Environment Layer                        │
│   ┌─────────────────────┐    ┌──────────────────────────┐   │
│   │ DemoEnvironment     │    │ LiveEnvironment (opt.)   │   │
│   │ (synthetic grid)    │    │ (screen capture + input) │   │
│   └─────────────────────┘    └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓ frame (np.ndarray)
┌─────────────────────────────────────────────────────────────┐
│                   Vision Layer (vision)                      │
│        Multi-scale template matching (OpenCV)                │
│        TemplateManager → MatchResult[]                       │
└─────────────────────────────────────────────────────────────┘
                              ↓ match results
┌─────────────────────────────────────────────────────────────┐
│                   FSM Layer (fsm)                            │
│   IDLE ↔ MOVE ↔ PICKUP ↔ INTERACT ↔ WAIT ↔ EXPLORE         │
└─────────────────────────────────────────────────────────────┘
                              ↓ events
┌─────────────────────────────────────────────────────────────┐
│                Decision Layer (agent)                        │
│   ┌──────────────────┐      ┌──────────────────────┐        │
│   │ LocalDecisionAgent│      │ CloudDecisionAgent   │        │
│   │ (rule-based)      │      │ (LLM, optional)      │        │
│   └──────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓ action
┌─────────────────────────────────────────────────────────────┐
│              HIL Layer (hil)                                 │
│        Human corrections over HTTP (Flask)                   │
│        get_correction → apply → send_correction (learn)     │
└─────────────────────────────────────────────────────────────┘
                              ↓ action
                      back to Environment
```

See [`docs/architecture.md`](docs/architecture.md) for a deep dive.

## 7. FSM States

The demo agent uses the following state machine:

| State | Description | Entry event | Exit event |
|-------|-------------|-------------|------------|
| `IDLE` | Scanning for elements | (initial) | `FOUND_TARGET`, `FOUND_PICKUP`, `FOUND_INTERACT`, `NO_TARGET` |
| `MOVE` | Navigating toward a goal | `FOUND_TARGET` | `ARRIVED`, `LOST_TARGET` |
| `PICKUP` | Collecting an item | `FOUND_PICKUP` | `COLLECTED` |
| `INTERACT` | Pressing a button | `FOUND_INTERACT` | `INTERACT_DONE` |
| `WAIT` | Pausing (scene settling / retry budget) | `INTERACT_DONE`, `TOO_MANY_FAILURES` | `READY` |
| `EXPLORE` | Blind exploration (no targets) | `NO_TARGET`, `LOST_TARGET` | `EXPLORED`, `FOUND_TARGET` |

The FSM is fully configurable — see `vision_fsm_agent.main::build_demo_fsm()`
and `vision_fsm_agent.fsm` for how to define your own topology. Also check
out the custom FSM example at [`examples/custom_fsm/`](examples/custom_fsm/).

## 8. HIL Workflow

Human-in-the-Loop (HIL) lets a human **override** the agent in real time:

```
┌──────────┐  POST /hil/set_correction  ┌──────────────┐  GET /hil/get_correction  ┌──────────┐
│  Human   │ ─────────────────────────> │ HIL Server   │ ────────────────────────> │  Agent   │
│ Operator │                            │ (Flask)      │                           │  Loop    │
└──────────┘                            └──────────────┘                           └──────────┘
                                             ↑                                         │
                                             │  POST /hil/send_correction (learn)      │
                                             └─────────────────────────────────────────┘
```

1. **Operator** pushes a correction (e.g. "click at x,y") via the HIL server.
2. **Agent** polls for corrections each loop iteration.
3. If a correction exists, the agent **applies it immediately** and
   **forwards it to the decision agent** for "learning" (recorded for later analysis).
4. Corrections support `click`, `stop`, and `reset` actions.

Start the HIL server:

```bash
python run.py --hil
# Available at http://localhost:8001/hil
```

See [`docs/hil-workflow.md`](docs/hil-workflow.md) for the full API.

## 9. Development Setup

### Quick setup with Make

```bash
git clone https://github.com/evanzheng0107-dev/vision-fsm-agent.git
cd vision-fsm-agent
make install   # installs package + dev dependencies
make assets    # generates demo templates
make test      # verifies everything works
```

### Manual setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -e ".[dev]"
python scripts/generate_demo_assets.py
```

### Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
```

This enables ruff linting/formatting, mypy type checking, and standard
whitespace/EOF checks before each commit.

### Dev Container

Open in VS Code with the Dev Containers extension for a pre-configured
environment (see [`.devcontainer/`](.devcontainer/devcontainer.json)).

### Useful commands

| Command | Description |
|---------|-------------|
| `make test` | Run pytest (66 tests) |
| `make test-cov` | Run pytest with coverage |
| `make demo` | Run the synthetic demo |
| `make lint` | Run ruff linter |
| `make check` | Run readiness check |
| `make clean` | Remove build artifacts |

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full development guide.

## 10. Testing

```bash
# Run the full test suite (no GUI, no network required)
pytest tests/ -v

# Run a specific module
pytest tests/unit/test_fsm.py -v
pytest tests/unit/test_vision.py -v
```

The suite covers:
- **FSM engine**: transitions, guards, actions, callbacks, history, reset
- **Vision engine**: multi-scale matching, template loading, classification
- **HIL system**: server endpoints, client validation, correction flow
- **Decision agent**: priority rules, failure handling, cloud fallback
- **Demo environment**: end-to-end agent loop, reproducibility, completion

CI runs automatically on every push and pull request via
[GitHub Actions](.github/workflows/test.yml).

## 11. Safety Boundaries

> **This project is for local, controlled demo environments, research, and
> education.**

- It is **not** intended for cheating, botting, bypassing platform rules,
  or automating third-party services without permission.
- The **default demo** runs against a local synthetic environment —
  no screen capture, no external input, no network (except optional local
  HIL).
- The optional **live mode** captures a screen region you explicitly
  configure. Use it **only** on systems you own or are authorised to
  control. `pyautogui.FAILSAFE` remains enabled so you can abort by moving
  the mouse to a screen corner.
- No anti-detection, evasion, or human-mimicry features are included or
  will be accepted as contributions.

See [`docs/safety-boundaries.md`](docs/safety-boundaries.md) for full
details and [`SECURITY.md`](SECURITY.md) for vulnerability reporting.

## 12. Roadmap

### v0.1.x (current)
- ✅ Core FSM + Vision + HIL framework
- ✅ Synthetic demo environment
- ✅ Local + optional cloud decision agents
- ✅ 66-test pytest suite with CI
- ✅ Custom FSM example with fallback path demonstration
- ✅ Standard Python package layout (src/vision_fsm_agent/)

### v0.2.0 (planned)
- Additional demo scenarios (multi-agent, dynamic obstacles) — [#7](https://github.com/evanzheng0107-dev/vision-fsm-agent/issues/7)
- Configurable FSM topologies via YAML — [#5](https://github.com/evanzheng0107-dev/vision-fsm-agent/issues/5)
- Vision pipeline extensions (edge detection, feature matching) — [#6](https://github.com/evanzheng0107-dev/vision-fsm-agent/issues/6)
- HIL correction persistence (SQLite backend) — [#10](https://github.com/evanzheng0107-dev/vision-fsm-agent/issues/10)

### v0.3.0+ (future)
- Plugin system for custom environments
- Performance benchmarking harness
- Educational lab exercises

## 13. Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md)
before opening a pull request.

**Key rules:**
- Tests must pass (`pytest tests/ -v`)
- No game-specific content or anti-detection features
- Keep the framework generic and the demo reproducible
- Follow the [safety boundaries](#11-safety-boundaries)

### Project Structure

```
vision-fsm-agent/
├── src/vision_fsm_agent/        Core framework package
│   ├── __init__.py              Public API + __version__
│   ├── fsm.py                   Generic FSM engine
│   ├── vision.py                Multi-scale OpenCV template matching
│   ├── agent.py                 Decision agents (local + optional cloud)
│   ├── main.py                  Agent loop (environment-agnostic)
│   ├── config.py                Configuration loader
│   ├── cli.py                   CLI entry point
│   ├── hil/                     Human-in-the-Loop subpackage
│   │   ├── client.py            HIL HTTP client
│   │   └── server.py            HIL Flask server
│   ├── envs/                    Environments subpackage
│   │   └── grid_world.py        Synthetic demo environment
│   ├── decision/                Decision re-exports
│   ├── actions/                 Actions (placeholder)
│   └── utils/                   Utilities (placeholder)
├── examples/
│   ├── visual_grid_world/       Demo runner + config + assets
│   └── custom_fsm/              Custom FSM topology example
├── tests/
│   ├── unit/                    FSM, vision, agent, config tests
│   ├── integration/             HIL, demo end-to-end tests
│   └── smoke/                   Demo + custom FSM smoke tests
├── config/
│   ├── default.yaml             Default framework configuration
│   └── demo.yaml                Demo-specific configuration
├── docs/                        User documentation
│   ├── api/                     API reference
│   ├── releases/                Release notes
│   └── maintainer/              Maintainer docs + agent_ledger/
├── scripts/                     OSS check, asset generator
├── .github/                     CI, issue/PR templates, CODEOWNERS
├── README.md
├── pyproject.toml
├── run.py                       Thin launcher → vision_fsm_agent.cli
└── ...                          LICENSE, CHANGELOG, CONTRIBUTING, etc.
```

## License

This project is licensed under the [MIT License](LICENSE).
