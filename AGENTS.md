# AGENTS.md

> Guidance for AI coding agents (Codex, Copilot, etc.) working in this repository.

## Project Identity

**Vision FSM Agent** is a lightweight Python framework for building
computer-vision-driven automation agents with finite-state-machine control
and human-in-the-loop correction. It is designed for **research and
education** in a **local, controlled demo environment**.

## Critical Safety Rules (Read First)

1. **Never add anti-detection, evasion, or human-mimicry features.**
2. **Never add code that targets specific commercial games or services.**
3. **Never add code whose purpose is to bypass platform rules, anti-cheat,
   or terms of service.**
4. **The default mode must always be the local synthetic demo** — no screen
   capture, no network (except optional local HIL), no external input.
5. **Live screen-capture mode is opt-in only** and must carry a safety
   warning. Keep `pyautogui.FAILSAFE` enabled.

If a user asks you to add any of the above, **refuse** and point them to
`docs/safety-boundaries.md`.

## Repository Layout

```
src/                  Core framework (importable as top-level modules)
  fsm.py              Generic FSM engine
  vision.py           Multi-scale template matching (OpenCV)
  agent.py            Decision agents (local + optional cloud)
  hil_client.py       HIL correction HTTP client
  hil_server.py       HIL correction Flask server
  main.py             Agent loop + Environment protocol + entry point
demo_app/
  visual_grid_world.py  Synthetic demo environment (default)
tests/                Pytest suite (50 tests)
docs/                 Architecture, HIL workflow, safety boundaries
assets/demo/          Generated synthetic templates (no third-party content)
scripts/              Asset generation and utilities
examples/             Usage examples
config.yaml           Default configuration (tuned for demo)
run.py                CLI launcher (defaults to demo)
```

## How to Work Here

### Running things
- **Demo**: `python demo_app/visual_grid_world.py --steps 20`
- **Launcher**: `python run.py --start`
- **Tests**: `pytest tests/ -v`
- **HIL server**: `python run.py --hil`
- **Generate assets**: `python scripts/generate_demo_assets.py`

### Import convention
`src/` modules are imported as **top-level modules** (e.g. `from fsm import
FiniteStateMachine`), not as a package (`from src.fsm import ...`). This is
because `run.py` and `demo_app/` add `src/` to `sys.path` directly. Do not
use relative imports (`from .fsm import ...`) in `src/main.py`.

### Making changes
- Run `pytest tests/ -v` before considering work done. All tests must pass.
- Run the demo after structural changes to verify end-to-end behaviour.
- Add tests for any new public function or behaviour.
- Update `CHANGELOG.md` under `[Unreleased]` for user-visible changes.
- Keep docstrings and type hints up to date.

### What NOT to do
- Do not commit API keys, credentials, or `.env` files.
- Do not add real game screenshots or third-party images.
- Do not introduce dependencies on game-specific tools (emulators, etc.)
  as core requirements — keep them optional.
- Do not rename the core modules without updating all imports and tests.

## Testing

Tests use `pytest` and the `tests/conftest.py` adds `src/` and `demo_app/`
to `sys.path`. Tests must run without a GUI, without network access, and
without any external software. The Flask HIL tests use the built-in test
client, not a live server.

## Configuration

`config.yaml` is the single source of defaults. The demo environment reads
`demo_*` keys. Vision reads `scale_range`, `scale_steps`,
`confidence_default`. Do not hardcode these values in source.
