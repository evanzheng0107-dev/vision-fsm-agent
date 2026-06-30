# Safety Boundaries

> **This document defines what Vision FSM Agent is and is not for. All
> contributors and users must read and respect these boundaries.**

## Statement of Purpose

Vision FSM Agent is a **research and education** framework for studying
computer-vision-driven automation, finite-state-machine control, and
human-in-the-loop correction. It is designed to be **safe, reproducible,
and self-contained**.

## Permitted Uses

- ✅ Running the **synthetic demo** (`demo_app/visual_grid_world.py`) for
  learning and experimentation
- ✅ Studying and extending the FSM, vision, and HIL components
- ✅ Building **your own** environments for systems **you own or are
  authorised to control** (e.g. your own test applications, your own
  automation workflows)
- ✅ Using the framework as a teaching tool in courses or workshops
- ✅ Contributing improvements that keep the framework generic and safe

## Prohibited Uses

- ❌ **Cheating** in games or circumventing anti-cheat systems
- ❌ **Botting** or automating third-party services without explicit
  permission
- ❌ **Bypassing** platform rules, terms of service, or access controls
- ❌ **Evading detection** — the project deliberately includes no
  anti-detection, human-mimicry, or timing-randomisation features designed
  to evade monitoring
- ❌ **Automating** any system in violation of applicable laws or
  regulations
- ❌ **Scraping** or extracting data from third-party services without
  authorisation

## Default Behaviour: Local Synthetic Demo

By default, the project runs against a **local synthetic environment**:

| Aspect | Default behaviour |
|--------|-------------------|
| Screen capture | ❌ None — frames are generated in memory |
| Mouse/keyboard input | ❌ None — actions update the synthetic world state |
| Network access | ❌ None (except optional local HIL server on localhost) |
| External software | ❌ None — no dependency on any game, emulator, or service |
| Real imagery | ❌ None — all templates are programmatically generated |

This means you can clone, install, and run the demo on any machine without
touching any external system.

## Optional Live Mode (Advanced)

The `LiveEnvironment` class (`src/main.py`) can capture a screen region
via `mss` and perform mouse input via `pyautogui`. This mode is:

- **Opt-in only** — never activated by default
- **Requires explicit configuration** — you must set `environment: "live"`
  and provide a `capture_region` in `config.yaml`
- **Guarded by PyAutoGUI's failsafe** — `pyautogui.FAILSAFE` remains
  `True` (default), so moving the mouse to a screen corner instantly
  aborts all input
- **Accompanied by a warning** — the environment logs a safety warning on
  initialisation

**Use live mode only on systems you own or are explicitly authorised to
control.** If you are unsure whether you have authorisation, you do not.

## What We Deliberately Do NOT Include

The original project (before this refactor) contained features that are
**not** included in Vision FSM Agent and **will not be accepted** as
contributions:

1. **Anti-detection / human mimicry**: random click jitter, timing
   randomisation, and mouse-movement patterns designed to evade detection
   systems. These have been removed.
2. **Game-specific logic**: window management for specific emulators,
   template images from commercial games, and decision logic tuned for a
   specific game. These have been removed or generalised.
3. **Unattended long-running operation**: the framework is not designed for
   unattended long-running automation. The demo terminates after a fixed
   number of steps.

## Contribution Policy

Contributions that add any of the following will be **rejected**:

- Features whose primary purpose is evasion, detection-avoidance, or
  circumvention of security controls
- Code that targets specific commercial games or services
- Real screenshots or assets from third-party software
- Functionality intended to violate terms of service

If you are unsure whether a contribution falls within the safety
boundaries, **open an issue and discuss it first**.

## Reporting Misuse

If you become aware of this project being used in a way that violates
these safety boundaries, please report it by opening a private issue or
contacting the maintainers. We take misuse seriously.

## Summary

| | |
|---|---|
| **Intended for** | Local demos, research, education |
| **Not intended for** | Cheating, botting, bypassing rules |
| **Default environment** | Synthetic, in-memory, no I/O |
| **Live capture** | Opt-in, explicit config, failsafe-enabled |
| **Anti-detection** | None, by design |
