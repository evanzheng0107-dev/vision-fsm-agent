"""
Generic agent main loop.

This module ties together the framework's pieces into a runnable loop:

    Environment  -->  Vision  -->  FSM  -->  Decision  -->  Action  -->  Environment
          ^                                                              |
          |______________________ HIL corrections _______________________|

The loop is *environment-agnostic*. An :class:`Environment` provides frames
and executes actions. Two implementations ship with the project:

  * :class:`~vision_fsm_agent.envs.grid_world.DemoEnvironment` - a fully
    synthetic, headless, reproducible grid world (the default).
  * :class:`LiveEnvironment` - captures a screen region with ``mss`` and
    clicks with ``pyautogui`` (opt-in, requires a window; **not** used by
    default).

Run the default demo::

    python run.py --start          # demo environment
    python run.py --start --live   # live screen capture (advanced)

Safety note
-----------
The default demo runs entirely against a local synthetic environment. The
live mode captures a screen region you explicitly configure; it must only
be used on systems and applications you own or are authorised to control.
See ``docs/safety-boundaries.md``.
"""

from __future__ import annotations

import logging
import os
import random
import time
from typing import Any, Protocol

import numpy as np

logger = logging.getLogger("AgentLoop")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# ----------------------------------------------------------------------
# Environment protocol
# ----------------------------------------------------------------------
class Environment(Protocol):
    """Interface that an agent loop drives."""

    def get_frame(self) -> np.ndarray | None:
        """Return the current frame as a BGR ``np.ndarray``, or ``None``."""
        ...

    def perform_action(self, action: str, params: dict[str, Any] | None = None) -> None:
        """Execute ``action`` (e.g. ``move``, ``pickup``, ``interact``)."""
        ...

    @property
    def bounds(self) -> tuple:
        """``(width, height)`` of the frame in pixels."""
        ...

    def close(self) -> None:
        """Release any resources."""
        ...


# ----------------------------------------------------------------------
# Optional live environment (screen capture + input)
# ----------------------------------------------------------------------
class LiveEnvironment:
    """Captures a screen region and performs mouse input.

    This is the *only* component that touches the real OS. It is **not**
    used by default. To enable it pass ``--live`` and configure
    ``capture_region`` in config to a region you are authorised
    to control.

    Safety: ``pyautogui.FAILSAFE`` is left at its default ``True`` so that
    moving the mouse to a screen corner aborts input instantly.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        import pyautogui  # noqa: F401  (import to configure)
        from mss import mss

        self._mss = mss()
        region = config.get("capture_region")
        if not region or len(region) != 4:
            raise ValueError("LiveEnvironment requires 'capture_region' [x, y, w, h] in config")
        self.region = {
            "left": int(region[0]),
            "top": int(region[1]),
            "width": int(region[2]),
            "height": int(region[3]),
        }
        pyautogui.PAUSE = 0.1
        self._pyautogui = pyautogui
        logger.warning(
            "LiveEnvironment active. Ensure you are authorised to control "
            "the target region. Move mouse to a screen corner to abort."
        )

    @property
    def bounds(self) -> tuple:
        return (self.region["width"], self.region["height"])

    def get_frame(self) -> np.ndarray | None:
        import cv2

        try:
            img = np.array(self._mss.grab(self.region))
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        except Exception as exc:
            logger.error("Capture failed: %s", exc)
            return None

    def perform_action(self, action: str, params: dict[str, Any] | None = None) -> None:
        params = params or {}
        if action in ("move", "pickup", "interact", "click"):
            x = params.get("x")
            y = params.get("y")
            if x is not None and y is not None:
                self._pyautogui.click(int(x), int(y))
                logger.info("Live click at (%d, %d)", int(x), int(y))

    def close(self) -> None:
        try:
            self._mss.close()
        except Exception:
            pass


# ----------------------------------------------------------------------
# FSM wiring for the demo agent
# ----------------------------------------------------------------------
def build_demo_fsm():
    """Build the standard FSM used by the demo agent.

    States: IDLE -> MOVE -> IDLE,  IDLE -> PICKUP -> IDLE,
            IDLE -> INTERACT -> WAIT -> IDLE,  IDLE -> EXPLORE -> IDLE
    """
    from .fsm import FiniteStateMachine

    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "FOUND_TARGET", "MOVE", description="target detected")
    fsm.add_transition("MOVE", "ARRIVED", "IDLE", description="reached target")
    fsm.add_transition("MOVE", "LOST_TARGET", "EXPLORE", description="target lost mid-move")

    fsm.add_transition("IDLE", "FOUND_PICKUP", "PICKUP", description="collectible detected")
    fsm.add_transition("PICKUP", "COLLECTED", "IDLE", description="item collected")

    fsm.add_transition("IDLE", "FOUND_INTERACT", "INTERACT", description="button detected")
    fsm.add_transition("INTERACT", "INTERACT_DONE", "WAIT", description="action performed")
    fsm.add_transition("WAIT", "READY", "IDLE", description="scene settled")

    fsm.add_transition("IDLE", "NO_TARGET", "EXPLORE", description="nothing detected")
    fsm.add_transition("EXPLORE", "EXPLORED", "IDLE", description="explored a step")
    fsm.add_transition(
        "EXPLORE", "FOUND_TARGET", "MOVE", description="found target while exploring"
    )

    fsm.add_transition("IDLE", "TOO_MANY_FAILURES", "WAIT", description="retry budget exhausted")
    return fsm


# ----------------------------------------------------------------------
# Agent loop
# ----------------------------------------------------------------------
class AgentLoop:
    """The main agent loop.

    Parameters
    ----------
    environment:
        An :class:`Environment` providing frames and executing actions.
    config:
        Application config dict.
    use_hil:
        Whether to poll the HIL server each iteration.
    decision_agent:
        A :class:`~vision_fsm_agent.agent.DecisionAgent`. Defaults to local rules.
    """

    def __init__(
        self,
        environment: Environment,
        config: dict[str, Any],
        *,
        use_hil: bool = False,
        decision_agent=None,
    ) -> None:
        self.env = environment
        self.config = config
        self.use_hil = use_hil
        self.fsm = build_demo_fsm()
        self.failed_attempts = 0
        self.start_time = time.time()
        self.loop_count = 0
        self.running = True

        # Vision
        from .vision import TemplateManager

        scale_range = tuple(config.get("scale_range", [0.6, 1.4]))
        scale_steps = int(config.get("scale_steps", 10))
        self.vision = TemplateManager(
            confidence_threshold=float(config.get("confidence_default", 0.8)),
            scale_range=scale_range,
            scale_steps=scale_steps,
        )

        # Decision
        if decision_agent is None:
            from .agent import LocalDecisionAgent

            decision_agent = LocalDecisionAgent(
                failure_threshold=int(config.get("max_failed_attempts", 3))
            )
        self.agent = decision_agent

        # HIL
        self.hil = None
        if use_hil:
            from .hil.client import HilClient

            self.hil = HilClient(config)

        # Loop timing
        self.loop_delay = tuple(config.get("loop_delay", [0.5, 1.0]))
        self.wait_delay = tuple(config.get("wait_delay", [0.5, 1.0]))
        self.max_failed_attempts = int(config.get("max_failed_attempts", 3))

    # ------------------------------------------------------------------
    def _build_agent_state(self, match_results: dict[str, Any]) -> dict[str, Any]:
        return {
            "current_state": self.fsm.current_state,
            "match_results": match_results,
            "failed_attempts": self.failed_attempts,
            "time_elapsed": time.time() - self.start_time,
            "loop_count": self.loop_count,
        }

    def _classify_matches(self, results) -> dict[str, dict[str, Any]]:
        """Turn a list of MatchResults into the match_results dict."""
        out: dict[str, dict[str, Any]] = {}
        for r in results:
            name = r.template_name.lower()
            if name.startswith("interact") or name.startswith("button"):
                key = "interact"
            elif name.startswith("pickup") or name.startswith("item"):
                key = "pickup"
            elif name.startswith("target") or name.startswith("locator") or name.startswith("goal"):
                key = "target"
            else:
                key = "other"
            if key not in out or r.confidence > out[key].get("confidence", 0):
                out[key] = {
                    "found": r.found,
                    "confidence": r.confidence,
                    "center": r.center,
                    "template_name": r.template_name,
                }
        return out

    def _apply_decision(self, decision: dict[str, Any]) -> None:
        action = decision.get("action", "continue")
        reason = decision.get("reason", "")
        logger.info("Decision: %s - %s", action, reason)

        if action == "move":
            self.fsm.fire("FOUND_TARGET")
        elif action == "pickup":
            self.fsm.fire("FOUND_PICKUP")
        elif action == "interact":
            self.fsm.fire("FOUND_INTERACT")
        elif action == "explore":
            self.fsm.fire("NO_TARGET")
        elif action == "wait":
            self.fsm.fire("TOO_MANY_FAILURES")

        self.env.perform_action(action)

        if action == "move":
            self.fsm.fire("ARRIVED")
        elif action == "pickup":
            self.fsm.fire("COLLECTED")
        elif action == "interact":
            self.fsm.fire("INTERACT_DONE")
            self.fsm.fire("READY")
        elif action == "explore":
            self.fsm.fire("EXPLORED")
        elif action == "wait":
            self.fsm.fire("READY")

    # ------------------------------------------------------------------
    def step(self) -> dict[str, Any]:
        """Run a single iteration of the loop. Returns the agent state."""
        self.loop_count += 1

        # 1. HIL correction check
        if self.hil:
            correction = self.hil.get_manual_correction()
            if correction and correction.get("type") == "correct":
                logger.info("Applying HIL correction: %s", correction)
                action = correction.get("action")
                if action == "stop":
                    self.running = False
                    return {}
                if action == "reset":
                    self.fsm.reset()
                    self.failed_attempts = 0
                    return {}
                if action == "click":
                    self.env.perform_action("click", correction.get("correct_params"))
                self.hil.send_correction_to_agent(correction)
                return self._build_agent_state({})

        # 2. Capture frame
        frame = self.env.get_frame()
        if frame is None:
            self.failed_attempts += 1
            if self.failed_attempts >= self.max_failed_attempts:
                logger.warning("Too many capture failures; entering WAIT")
                self.fsm.fire("TOO_MANY_FAILURES")
                self.fsm.fire("READY")
                self.failed_attempts = 0
            time.sleep(random.uniform(*self.wait_delay))
            return self._build_agent_state({})

        self.failed_attempts = 0

        # 3. Vision: match all templates
        if len(self.vision) == 0:
            logger.debug("No templates loaded; skipping vision")
            match_results = {}
        else:
            results = self.vision.match_all(frame)
            match_results = self._classify_matches(results)

        # 4. Build agent state and decide
        agent_state = self._build_agent_state(match_results)
        if self.hil:
            self.hil.send_status(agent_state)

        decision = self.agent.get_decision(agent_state)
        self._apply_decision(decision)

        return agent_state

    # ------------------------------------------------------------------
    def run(self, max_steps: int | None = None) -> None:
        """Run the loop until ``running`` is False or ``max_steps`` reached."""
        logger.info(
            "Agent loop starting (env=%s, fsm=%s, hil=%s, steps=%s)",
            type(self.env).__name__,
            self.fsm.current_state,
            bool(self.hil),
            max_steps or "unlimited",
        )
        try:
            while self.running:
                if max_steps is not None and self.loop_count >= max_steps:
                    logger.info("Reached max_steps=%d, stopping", max_steps)
                    break
                self.step()
                delay = random.uniform(*self.loop_delay)
                time.sleep(delay)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.env.close()
            logger.info(
                "Agent loop finished after %d steps (state=%s)",
                self.loop_count,
                self.fsm.current_state,
            )


# ----------------------------------------------------------------------
# Entry points
# ----------------------------------------------------------------------
def run_demo(config: dict[str, Any], *, max_steps: int = 50, use_hil: bool = False) -> None:
    """Run the agent against the synthetic demo environment."""
    from .envs.grid_world import DemoEnvironment

    env = DemoEnvironment(config)
    loop = AgentLoop(env, config, use_hil=use_hil)

    # Load demo templates.
    pkg_dir = os.path.dirname(__file__)
    candidates = [
        os.path.join(os.getcwd(), "examples", "visual_grid_world", "assets"),
        os.path.join(pkg_dir, "..", "..", "examples", "visual_grid_world", "assets"),
        os.path.join(pkg_dir, "..", "..", "assets", "demo"),  # legacy
    ]
    loaded = 0
    for assets_dir in candidates:
        assets_dir = os.path.normpath(assets_dir)
        if os.path.isdir(assets_dir):
            loaded = loop.vision.load_directory(assets_dir)
            if loaded > 0:
                break
    if loaded == 0:
        logger.warning("No demo templates found. Run scripts/generate_demo_assets.py first.")
    else:
        logger.info("Loaded %d demo templates", loaded)

    loop.run(max_steps=max_steps)


def run_live(config: dict[str, Any], *, use_hil: bool = False) -> None:
    """Run the agent against a live screen region (advanced)."""
    env = LiveEnvironment(config)
    loop = AgentLoop(env, config, use_hil=use_hil)
    loop.run()
