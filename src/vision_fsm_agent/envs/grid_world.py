"""
Visual Grid World - a synthetic demo environment for the Vision FSM Agent.

This module provides a fully self-contained, headless, reproducible
environment so the entire agent loop (vision -> FSM -> decision -> action)
can run **without any real application, window, or game**.

The world is a grid. Each cell is either empty or holds one of:
  * a **goal**    - green crosshair, the navigation target
  * an **item**   - gold circle, a collectible
  * a **button**  - blue square, an interactable element

The environment renders itself to a BGR ``np.ndarray`` each frame using
the same drawing primitives that produce the matching templates in
``assets/demo/``. This guarantees that template matching actually finds
the elements, making the demo a genuine end-to-end test of the framework.

Run standalone::

    python demo_app/visual_grid_world.py            # run the demo
    python demo_app/visual_grid_world.py --save out  # save frames as PNGs

Safety note
-----------
This is a local synthetic environment. It does not capture any screen,
send any input to third-party software, or access the network. It exists
purely for reproducible research and education.
"""

from __future__ import annotations

import os
import random
import sys
from typing import Any

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------
# These are shared between the environment (which renders full frames) and
# the asset generator (which renders individual templates). Keeping them in
# one place guarantees pixel-identical matches.

CELL = 40  # pixels per grid cell


def _new_canvas(width: int, height: int, color: tuple[int, int, int] = (32, 32, 32)) -> np.ndarray:
    """Create a solid-color BGR canvas."""
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas[:] = color
    return canvas


def render_goal(canvas: np.ndarray, cx: int, cy: int, size: int = 28) -> None:
    """Draw a green crosshair goal marker centered at (cx, cy)."""
    green = (0, 200, 80)  # BGR
    half = size // 2
    # outer ring
    cv2.circle(canvas, (cx, cy), half, green, 2)
    # crosshair lines
    cv2.line(canvas, (cx - half, cy), (cx + half, cy), green, 2)
    cv2.line(canvas, (cx, cy - half), (cx, cy + half), green, 2)


def render_item(canvas: np.ndarray, cx: int, cy: int, size: int = 24) -> None:
    """Draw a gold collectible circle centered at (cx, cy)."""
    gold = (40, 200, 240)  # BGR (gold-ish)
    cv2.circle(canvas, (cx, cy), size // 2, gold, -1)  # filled
    cv2.circle(canvas, (cx, cy), size // 2, (255, 255, 255), 1)  # outline


def render_button(canvas: np.ndarray, cx: int, cy: int, size: int = 28) -> None:
    """Draw a blue interactable button centered at (cx, cy)."""
    blue = (180, 90, 40)  # BGR
    half = size // 2
    cv2.rectangle(
        canvas,
        (cx - half, cy - half),
        (cx + half, cy + half),
        blue,
        -1,
    )
    cv2.rectangle(
        canvas,
        (cx - half, cy - half),
        (cx + half, cy + half),
        (255, 255, 255),
        1,
    )


def render_agent(canvas: np.ndarray, cx: int, cy: int, size: int = 26) -> None:
    """Draw the agent (a red diamond) centered at (cx, cy)."""
    red = (40, 40, 220)  # BGR
    half = size // 2
    pts = np.array(
        [[cx, cy - half], [cx + half, cy], [cx, cy + half], [cx - half, cy]],
        dtype=np.int32,
    )
    cv2.fillPoly(canvas, [pts], red)
    cv2.polylines(canvas, [pts], True, (255, 255, 255), 1)


# Standalone template renderers (for asset generation)
def make_goal_template() -> np.ndarray:
    """Return a standalone goal template image (CELL x CELL)."""
    canvas = _new_canvas(CELL, CELL, (32, 32, 32))
    render_goal(canvas, CELL // 2, CELL // 2)
    return canvas


def make_item_template() -> np.ndarray:
    """Return a standalone item template image (CELL x CELL)."""
    canvas = _new_canvas(CELL, CELL, (32, 32, 32))
    render_item(canvas, CELL // 2, CELL // 2)
    return canvas


def make_button_template() -> np.ndarray:
    """Return a standalone button template image (CELL x CELL)."""
    canvas = _new_canvas(CELL, CELL, (32, 32, 32))
    render_button(canvas, CELL // 2, CELL // 2)
    return canvas


# ---------------------------------------------------------------------------
# The demo environment
# ---------------------------------------------------------------------------
class DemoEnvironment:
    """A synthetic grid-world environment implementing the Environment protocol.

    The agent starts at the top-left and can navigate, collect items, and
    press buttons. Each ``perform_action`` advances the world by one step.
    ``get_frame`` renders the current world state to a BGR image.

    The world is deterministic given the same seed, making runs reproducible.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        config = config or {}
        self.grid_w = int(config.get("demo_grid_w", 12))
        self.grid_h = int(config.get("demo_grid_h", 12))
        self.cell = int(config.get("demo_cell_px", CELL))
        self.seed = config.get("demo_seed", 42)
        self._rng = random.Random(self.seed)

        # Agent starts at top-left.
        self.agent_pos: tuple[int, int] = (0, 0)

        # World contents (grid coordinates).
        self.goals: list[tuple[int, int]] = self._scatter(2)
        self.items: list[tuple[int, int]] = self._scatter(3, avoid=self.goals)
        self.buttons: list[tuple[int, int]] = self._scatter(1, avoid=self.goals + self.items)

        # Mutable state.
        self.collected: set = set()  # indices into self.items
        self.pressed: set = set()  # indices into self.buttons
        self.step_count = 0
        self.action_log: list[str] = []

    # -- helpers --
    def _scatter(self, n: int, avoid: list[tuple[int, int]] | None = None) -> list[tuple[int, int]]:
        """Place ``n`` elements at random non-overlapping grid positions."""
        avoid = avoid or []
        placed: list[tuple[int, int]] = []
        occupied = set(avoid) | {(0, 0)}  # keep start clear
        attempts = 0
        while len(placed) < n and attempts < 200:
            gx = self._rng.randint(2, self.grid_w - 1)
            gy = self._rng.randint(2, self.grid_h - 1)
            if (gx, gy) not in occupied:
                occupied.add((gx, gy))
                placed.append((gx, gy))
            attempts += 1
        return placed

    def _grid_to_pixel(self, gx: int, gy: int) -> tuple[int, int]:
        """Convert grid coords to pixel center of the cell."""
        return (gx * self.cell + self.cell // 2, gy * self.cell + self.cell // 2)

    # -- Environment protocol --
    @property
    def bounds(self) -> tuple:
        return (self.grid_w * self.cell, self.grid_h * self.cell)

    def get_frame(self) -> np.ndarray:
        """Render the current world state to a BGR image."""
        w, h = self.bounds
        canvas = _new_canvas(w, h, (32, 32, 32))

        # Grid lines (subtle)
        for gx in range(0, self.grid_w + 1):
            cv2.line(canvas, (gx * self.cell, 0), (gx * self.cell, h), (50, 50, 50), 1)
        for gy in range(0, self.grid_h + 1):
            cv2.line(canvas, (0, gy * self.cell), (w, gy * self.cell), (50, 50, 50), 1)

        # Goals
        for gx, gy in self.goals:
            px, py = self._grid_to_pixel(gx, gy)
            render_goal(canvas, px, py)

        # Items (skip collected)
        for i, (gx, gy) in enumerate(self.items):
            if i in self.collected:
                continue
            px, py = self._grid_to_pixel(gx, gy)
            render_item(canvas, px, py)

        # Buttons (skip pressed)
        for i, (gx, gy) in enumerate(self.buttons):
            if i in self.pressed:
                continue
            px, py = self._grid_to_pixel(gx, gy)
            render_button(canvas, px, py)

        # Agent
        ax, ay = self.agent_pos
        px, py = self._grid_to_pixel(ax, ay)
        render_agent(canvas, px, py)

        # Step counter overlay (top-left)
        cv2.putText(
            canvas,
            f"step {self.step_count}",
            (6, 16),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (200, 200, 200),
            1,
        )
        return canvas

    def perform_action(self, action: str, params: dict[str, Any] | None = None) -> None:
        """Advance the world by one step in response to an agent action."""
        params = params or {}
        self.step_count += 1
        self.action_log.append(action)

        if action == "move":
            self._move_towards_nearest_goal()
        elif action == "pickup":
            self._try_pickup()
        elif action == "interact":
            self._try_interact()
        elif action == "explore":
            self._random_walk()
        elif action == "wait":
            pass  # no-op
        elif action == "click":
            # HIL-driven click; for the demo just advance the world.
            self._random_walk()
        elif action == "continue":
            pass
        # unknown actions are ignored

    def close(self) -> None:
        pass

    # -- action implementations --
    def _move_towards_nearest_goal(self) -> None:
        if not self.goals:
            return
        target = min(self.goals, key=lambda g: self._dist(self.agent_pos, g))
        self._step_towards(target)

    def _step_towards(self, target: tuple[int, int]) -> None:
        ax, ay = self.agent_pos
        tx, ty = target
        if ax < tx:
            ax += 1
        elif ax > tx:
            ax -= 1
        if ay < ty:
            ay += 1
        elif ay > ty:
            ay -= 1
        self.agent_pos = (ax, ay)

    def _try_pickup(self) -> None:
        """Walk toward the nearest uncollected item; collect it when adjacent."""
        nearest, nearest_i = None, -1
        for i, (gx, gy) in enumerate(self.items):
            if i in self.collected:
                continue
            if nearest is None or self._dist(self.agent_pos, (gx, gy)) < self._dist(
                self.agent_pos, nearest
            ):
                nearest, nearest_i = (gx, gy), i
        if nearest is None:
            return
        if self._dist(self.agent_pos, nearest) <= 1:
            self.collected.add(nearest_i)
        else:
            self._step_towards(nearest)

    def _try_interact(self) -> None:
        """Walk toward the nearest unpressed button; press it when adjacent."""
        nearest, nearest_i = None, -1
        for i, (gx, gy) in enumerate(self.buttons):
            if i in self.pressed:
                continue
            if nearest is None or self._dist(self.agent_pos, (gx, gy)) < self._dist(
                self.agent_pos, nearest
            ):
                nearest, nearest_i = (gx, gy), i
        if nearest is None:
            return
        if self._dist(self.agent_pos, nearest) <= 1:
            self.pressed.add(nearest_i)
        else:
            self._step_towards(nearest)

    def _random_walk(self) -> None:
        ax, ay = self.agent_pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        dx, dy = self._rng.choice(moves)
        ax = max(0, min(self.grid_w - 1, ax + dx))
        ay = max(0, min(self.grid_h - 1, ay + dy))
        self.agent_pos = (ax, ay)

    @staticmethod
    def _dist(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # -- status --
    def status(self) -> dict[str, Any]:
        return {
            "agent_pos": self.agent_pos,
            "step_count": self.step_count,
            "items_collected": len(self.collected),
            "items_total": len(self.items),
            "buttons_pressed": len(self.pressed),
            "buttons_total": len(self.buttons),
            "goals": self.goals,
            "done": len(self.collected) == len(self.items)
            and len(self.pressed) == len(self.buttons),
        }


# ---------------------------------------------------------------------------
# Standalone runner
# ---------------------------------------------------------------------------
def run_standalone(max_steps: int = 50, save_dir: str | None = None) -> DemoEnvironment:
    """Run the demo end-to-end and return the final environment state.

    If ``save_dir`` is given, each frame is written there as a PNG.
    """
    from ..config import load_config
    from ..main import AgentLoop

    config = load_config()
    env = DemoEnvironment(config)

    # Build an agent loop with demo templates.
    loop = AgentLoop(env, config, use_hil=False)

    # Search for assets in the new examples/ location first, then legacy.
    pkg_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    candidates = [
        os.path.join(os.getcwd(), "examples", "visual_grid_world", "assets"),
        os.path.join(pkg_dir, "examples", "visual_grid_world", "assets"),
        os.path.join(pkg_dir, "assets", "demo"),  # legacy
    ]
    loaded = 0
    for assets_dir in candidates:
        assets_dir = os.path.normpath(assets_dir)
        if os.path.isdir(assets_dir):
            loaded = loop.vision.load_directory(assets_dir)
            if loaded > 0:
                break
    if loaded == 0:
        # Generate assets on the fly so the demo always runs.
        print("[demo] No templates found, generating them now...")
        _generate_assets(assets_dir)
        loop.vision.load_directory(assets_dir)

    print(f"[demo] Loaded {len(loop.vision)} templates")
    print(
        f"[demo] World: {env.grid_w}x{env.grid_h}, goals={env.goals}, "
        f"items={len(env.items)}, buttons={len(env.buttons)}"
    )
    print(f"[demo] Running {max_steps} steps...\n")

    os.makedirs(save_dir, exist_ok=True) if save_dir else None

    for i in range(max_steps):
        loop.step()
        st = env.status()
        bar = _progress_bar(
            st["items_collected"], st["items_total"], st["buttons_pressed"], st["buttons_total"]
        )
        print(
            f"  step {st['step_count']:>3} | fsm={loop.fsm.current_state:<8} "
            f"pos={st['agent_pos']} | {bar}"
        )
        if save_dir:
            frame = env.get_frame()
            cv2.imwrite(os.path.join(save_dir, f"frame_{i:03d}.png"), frame)
        if st["done"]:
            print("\n[demo] All items collected and buttons pressed. Done!")
            break
    else:
        print("\n[demo] Reached step limit.")

    print(f"\n[demo] Final status: {env.status()}")
    if save_dir:
        print(f"[demo] Frames saved to {save_dir}/")
    return env


def _progress_bar(collected: int, total_items: int, pressed: int, total_buttons: int) -> str:
    items = "".join("I" if i < collected else "." for i in range(total_items))
    btns = "".join("B" if i < pressed else "." for i in range(total_buttons))
    return f"items[{items}] buttons[{btns}]"


def _generate_assets(assets_dir: str) -> None:
    """Generate the demo template PNGs into ``assets_dir``."""
    os.makedirs(assets_dir, exist_ok=True)
    cv2.imwrite(os.path.join(assets_dir, "target_goal.png"), make_goal_template())
    cv2.imwrite(os.path.join(assets_dir, "pickup_item.png"), make_item_template())
    cv2.imwrite(os.path.join(assets_dir, "interact_button.png"), make_button_template())


if __name__ == "__main__":
    # Parse simple CLI args.
    max_steps = 50
    save_dir = None
    args = sys.argv[1:]
    if "--save" in args:
        idx = args.index("--save")
        save_dir = args[idx + 1] if idx + 1 < len(args) else "demo_frames"
    if "--steps" in args:
        idx = args.index("--steps")
        try:
            max_steps = int(args[idx + 1])
        except (IndexError, ValueError):
            pass

    run_standalone(max_steps=max_steps, save_dir=save_dir)
