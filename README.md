# Vision FSM Agent

> A lightweight Python framework for building computer-vision-driven automation agents with finite-state-machine control and human-in-the-loop correction.

一个用于研究和教学的 **计算机视觉 + 有限状态机 + HIL 人工纠正** Agent 框架。

[![Tests](https://github.com/evanzheng0107-dev/sword-legend-explorer/actions/workflows/test.yml/badge.svg)](https://github.com/evanzheng0107-dev/sword-legend-explorer/actions/workflows/test.yml)
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
9. [Testing](#9-testing)
10. [Safety Boundaries](#10-safety-boundaries)
11. [Roadmap](#11-roadmap)
12. [Contributing](#12-contributing)

---

## 1. What is this?

**Vision FSM Agent** is a minimal, dependency-light framework that combines
three classic automation building blocks:

| Building block | Module | What it does |
|---|---|---|
| **Computer Vision** | `src/vision.py` | Multi-scale OpenCV template matching with configurable thresholds |
| **Finite-State Machine** | `src/fsm.py` | Generic FSM with guards, actions, callbacks, and transition history |
| **Human-in-the-Loop** | `src/hil_*.py` | HTTP-based correction channel so a human can override the agent in real time |

These are wired together by a generic **agent loop** (`src/main.py`) that
drives an **Environment** — an interface you can implement for any target.
The project ships with a **synthetic demo environment** so you can run the
entire pipeline with zero external setup.

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
[Safety Boundaries](#10-safety-boundaries) and
[`docs/safety-boundaries.md`](docs/safety-boundaries.md).

## 4. Quick Start

```bash
# 1. Clone
git clone https://github.com/evanzheng0107-dev/sword-legend-explorer.git
cd sword-legend-explorer

# 2. Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Generate the synthetic demo assets (programmatic, no downloads)
python scripts/generate_demo_assets.py

# 4. Run the demo
python demo_app/visual_grid_world.py --steps 20
```

You should see the agent navigate a grid world, collect items, and press
buttons — all driven by real template matching and FSM transitions.

### Using the launcher

```bash
python run.py --start            # demo mode (default)
python run.py --start --steps 30 # specify step count
python run.py --hil              # start the HIL correction server
```

## 5. Demo Environment

The demo (`demo_app/visual_grid_world.py`) is a **fully synthetic,
headless, reproducible** environment:

- A 12×12 grid world rendered to a BGR image with OpenCV/numpy
- **Goals** (green crosshairs) — navigation targets
- **Items** (gold circles) — collectibles
- **Buttons** (blue squares) — interactable elements
- An **agent** (red diamond) that moves, collects, and interacts

Each frame is rendered using the **same drawing primitives** that
generate the template images in `assets/demo/`. This guarantees that
template matching actually finds the elements — making the demo a genuine
end-to-end test of the vision pipeline.

The world is **deterministic** given the same seed (`demo_seed: 42` by
default), so runs are reproducible.

```
[demo] World: 12x12, goals=[(3, 2), (6, 5)], items=3, buttons=1
  step   1 | fsm=IDLE  pos=(1, 1) | items[...] buttons[.]
  ...
  step  19 | fsm=IDLE  pos=(3,10) | items[III] buttons[B]
[demo] All items collected and buttons pressed. Done!
```

Save frames as PNGs for inspection:

```bash
python demo_app/visual_grid_world.py --save demo_frames --steps 20
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
│                   Vision Layer (src/vision.py)               │
│        Multi-scale template matching (OpenCV)                │
│        TemplateManager → MatchResult[]                       │
└─────────────────────────────────────────────────────────────┘
                              ↓ match results
┌─────────────────────────────────────────────────────────────┐
│                   FSM Layer (src/fsm.py)                      │
│   IDLE ↔ MOVE ↔ PICKUP ↔ INTERACT ↔ WAIT ↔ EXPLORE         │
└─────────────────────────────────────────────────────────────┘
                              ↓ events
┌─────────────────────────────────────────────────────────────┐
│                Decision Layer (src/agent.py)                  │
│   ┌──────────────────┐      ┌──────────────────────┐        │
│   │ LocalDecisionAgent│      │ CloudDecisionAgent   │        │
│   │ (rule-based)      │      │ (LLM, optional)      │        │
│   └──────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                              ↓ action
┌─────────────────────────────────────────────────────────────┐
│              HIL Layer (src/hil_client.py / hil_server.py)   │
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

The FSM is fully configurable — see `src/main.py::build_demo_fsm()` and
`src/fsm.py` for how to define your own topology.

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
3. If a correction exists, the **agent applies it immediately** (e.g.
   performs the click) and **forwards it to the decision agent** for
   "learning" (recorded for later analysis).
4. Corrections support `click`, `stop`, and `reset` actions.

Start the HIL server:

```bash
python run.py --hil
# Available at http://localhost:8001/hil
```

See [`docs/hil-workflow.md`](docs/hil-workflow.md) for the full API.

## 9. Testing

```bash
# Run the full test suite (no GUI, no network required)
pytest tests/ -v

# Run a specific module
pytest tests/test_fsm.py -v
pytest tests/test_vision.py -v
```

The suite covers:
- **FSM engine**: transitions, guards, actions, callbacks, history, reset
- **Vision engine**: multi-scale matching, template loading, classification
- **HIL system**: server endpoints, client validation, correction flow
- **Decision agent**: priority rules, failure handling, cloud fallback
- **Demo environment**: end-to-end agent loop, reproducibility, completion

CI runs automatically on every push and pull request via
[GitHub Actions](.github/workflows/test.yml).

## 10. Safety Boundaries

> **This project is for local, controlled demo environments, research, and
> education.**

- It is **not** intended for cheating, botting, bypassing platform rules,
  or automating third-party services without permission.
- The **default demo** runs against a local synthetic UI environment —
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

## 11. Roadmap

### v0.1.0 (current)
- ✅ Core FSM + Vision + HIL framework
- ✅ Synthetic demo environment
- ✅ Local + optional cloud decision agents
- ✅ 50-test pytest suite with CI

### v0.2.0 (planned)
- Additional demo scenarios (multi-agent, dynamic obstacles)
- Configurable FSM topologies via YAML
- Vision pipeline extensions (edge detection, feature matching)
- Web dashboard for HIL corrections

### v0.3.0+ (future)
- Plugin system for custom environments
- Performance benchmarking harness
- Educational lab exercises

## 12. Contributing

Contributions are welcome! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md)
before opening a pull request.

**Key rules:**
- Tests must pass (`pytest tests/ -v`)
- No game-specific content or anti-detection features
- Keep the framework generic and the demo reproducible
- Follow the [safety boundaries](#10-safety-boundaries)

### License

This project is licensed under the [MIT License](LICENSE).
