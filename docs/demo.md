# Demo: Visual Grid World

This document explains the synthetic demo environment shipped with Vision
FSM Agent — what it is, how to run it, what to expect, and how to
configure it.

## Overview

The **Visual Grid World** (`demo_app/visual_grid_world.py`) is a fully
synthetic, headless, reproducible environment. It lets you run the
complete agent pipeline — vision → FSM → decision → action — **without
any external software, screen capture, or network access**.

The world is a grid where each cell may contain:
- A **goal** (green crosshair) — navigation target
- An **item** (gold circle) — collectible
- A **button** (blue square) — interactable element

An **agent** (red diamond) starts at the top-left and must navigate,
collect, and interact — driven entirely by template matching and FSM
transitions.

## Prerequisites

- Python 3.9+
- `pip install -r requirements.txt` (installs opencv-python, numpy,
  pyyaml, flask, requests, pytest)

No game, emulator, or GUI is required.

## Running the Demo

### Quick run

```bash
python demo_app/visual_grid_world.py --steps 20
```

### Using the launcher

```bash
python run.py --start              # demo mode (default, 50 steps)
python run.py --start --steps 30   # specify step count
```

### Command-line options

| Option | Default | Description |
|--------|---------|-------------|
| `--steps N` | 50 | Maximum number of steps before stopping |
| `--save DIR` | (none) | Save each frame as `frame_XXX.png` in DIR |

### Generate demo assets

The demo requires template images in `assets/demo/`. Generate them with:

```bash
python scripts/generate_demo_assets.py
```

These are 100% programmatically generated (no downloads). The script
creates three 40×40 PNG files using the same drawing primitives the demo
uses to render frames, guaranteeing template matching succeeds.

## Expected Output

A successful run looks like this:

```
[demo] Loaded 3 templates
[demo] World: 12x12, goals=[(3, 2), (6, 5)], items=3, buttons=1
[demo] Running 35 steps...

  step   1 | fsm=IDLE  pos=(1, 1) | items[...] buttons[.]
  step   2 | fsm=IDLE  pos=(2, 2) | items[...] buttons[.]
  step   3 | fsm=IDLE  pos=(3, 3) | items[...] buttons[.]
  step   4 | fsm=IDLE  pos=(4, 4) | items[...] buttons[.]
  step   5 | fsm=IDLE  pos=(4, 4) | items[I..] buttons[.]
  step   6 | fsm=IDLE  pos=(3, 5) | items[I..] buttons[.]
  ...
  step  13 | fsm=IDLE  pos=(3,10) | items[III] buttons[.]
  ...
  step  19 | fsm=IDLE  pos=(3,10) | items[III] buttons[B]

[demo] All items collected and buttons pressed. Done!

[demo] Final status: {'agent_pos': (3, 10), 'step_count': 19,
  'items_collected': 3, 'items_total': 3,
  'buttons_pressed': 1, 'buttons_total': 1, 'done': True}
```

**Reading the progress bar:**
- `items[III]` — 3 items collected (I = collected, . = pending)
- `buttons[B]` — 1 button pressed (B = pressed, . = pending)
- `done: True` — all objectives complete

## What's Happening Each Step

Each iteration of the agent loop performs:

1. **Frame capture** — `DemoEnvironment.get_frame()` renders the current
   world state to a BGR numpy array using OpenCV drawing primitives.
2. **Template matching** — `TemplateManager.match_all()` runs multi-scale
   `cv2.matchTemplate` against all templates (goal, item, button).
3. **Classification** — Results are classified into semantic categories
   (`target`, `pickup`, `interact`) by template name prefix.
4. **Decision** — `LocalDecisionAgent` picks an action by priority:
   `interact` > `pickup` > `move` > `wait` > `explore`.
5. **FSM transition** — The FSM fires events (`FOUND_PICKUP`, `ARRIVED`,
   etc.) and transitions states (`IDLE → PICKUP → IDLE`).
6. **Action execution** — `DemoEnvironment.perform_action()` advances
   the world: the agent moves toward targets, collects adjacent items,
   presses adjacent buttons.

## Demo Configuration

The demo reads from `config.yaml`. Key settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `demo_grid_w` | 12 | Grid width in cells |
| `demo_grid_h` | 12 | Grid height in cells |
| `demo_cell_px` | 40 | Pixels per cell |
| `demo_seed` | 42 | RNG seed for reproducible world layout |
| `demo_max_steps` | 50 | Max steps when using `run.py --start` |
| `confidence_default` | 0.75 | Template match confidence threshold |
| `scale_range` | [0.6, 1.4] | Multi-scale matching range |
| `scale_steps` | 10 | Number of scale steps |
| `loop_delay` | [0.3, 0.6] | Delay between iterations (seconds) |
| `max_failed_attempts` | 3 | Failures before entering WAIT |

### Changing the world layout

Edit `demo_seed` in `config.yaml` to get a different arrangement of
goals, items, and buttons. The same seed always produces the same
layout — useful for reproducible testing.

### Changing difficulty

Increase `demo_grid_w`/`demo_grid_h` for a larger world. Lower
`confidence_default` for more lenient matching (may increase false
positives).

## Saving Frames

To inspect what the agent "sees" each step:

```bash
python demo_app/visual_grid_world.py --save demo_frames --steps 20
```

Frames are saved as `demo_frames/frame_000.png`, `frame_001.png`, etc.
You can open them in any image viewer or use OpenCV to create a video.

> `demo_frames/` is in `.gitignore` and won't be committed.

## Troubleshooting

### "No templates found"

Run `python scripts/generate_demo_assets.py` first. The demo needs
template images in `assets/demo/`.

### Demo runs but agent doesn't move

Check `confidence_default` in `config.yaml`. If it's too high, template
matching may not find elements. Try lowering to `0.6`.

### `cv2.error` on Windows

Ensure `opencv-python` is installed in your virtual environment:
```bash
pip install opencv-python --force-reinstall
```

### Demo doesn't complete in 50 steps

Some random seeds produce harder layouts. Increase `--steps` or try a
different `demo_seed`.

> A full troubleshooting guide is planned for Day 2
> (`docs/troubleshooting.md`).
