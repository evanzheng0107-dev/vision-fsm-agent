"""
Finite-State-Machine (FSM) engine.

A small, dependency-free FSM that supports:
  * Named states and event-driven transitions
  * Optional guard conditions and side-effect actions on transitions
  * on_enter / on_exit callbacks per state
  * Transition history for debugging and testing

This module is intentionally generic. It knows nothing about computer
vision, games, or any concrete application domain. The demo application
(see ``demo_app/visual_grid_world.py``) wires vision results into FSM
events to drive an agent loop.

Safety note
-----------
The FSM itself is domain-agnostic. Any automation built on top of it
must respect the safety boundaries documented in ``docs/safety-boundaries.md``.
"""

from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger(__name__)

# A guard receives the FSM and the event payload, returns True to allow
# the transition or False to block it.
Guard = Callable[["FiniteStateMachine", dict], bool]

# An action receives the FSM and the event payload. Return value ignored.
Action = Callable[["FiniteStateMachine", dict], None]


@dataclass
class Transition:
    """A single FSM transition rule."""

    source: str
    event: str
    target: str
    guard: Guard | None = None
    action: Action | None = None
    description: str = ""

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return (
            f"Transition({self.source} --[{self.event}]--> {self.target}"
            f"{f' ({self.description})' if self.description else ''})"
        )


@dataclass
class TransitionRecord:
    """An entry in the FSM transition history."""

    source: str
    event: str
    target: str
    payload: dict = field(default_factory=dict)


class FiniteStateMachine:
    """A generic finite-state machine.

    Parameters
    ----------
    initial_state:
        The state the machine starts in.
    history_limit:
        How many past transitions to keep in memory (for debugging/tests).

    Example
    -------
    >>> fsm = FiniteStateMachine("IDLE")
    >>> fsm.add_transition("IDLE", "FOUND_TARGET", "MOVE")
    >>> fsm.add_transition("MOVE", "ARRIVED", "IDLE")
    >>> fsm.fire("FOUND_TARGET")
    >>> fsm.current_state
    'MOVE'
    """

    def __init__(self, initial_state: str, history_limit: int = 200) -> None:
        self._state: str = initial_state
        self._initial: str = initial_state
        self._transitions: list[Transition] = []
        self._on_enter: dict[str, list[Action]] = {}
        self._on_exit: dict[str, list[Action]] = {}
        self._history: deque[TransitionRecord] = deque(maxlen=history_limit)
        # Track how many times each (source, event) has been attempted but
        # blocked by a guard. Useful for failure-retry logic.
        self._blocked_count: dict[tuple[str, str], int] = {}

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    @property
    def current_state(self) -> str:
        return self._state

    @property
    def initial_state(self) -> str:
        return self._initial

    def add_transition(
        self,
        source: str,
        event: str,
        target: str,
        *,
        guard: Guard | None = None,
        action: Action | None = None,
        description: str = "",
    ) -> FiniteStateMachine:
        """Register a transition. Returns self for chaining."""
        self._transitions.append(Transition(source, event, target, guard, action, description))
        return self

    def on_enter(self, state: str, callback: Action) -> FiniteStateMachine:
        """Register a callback fired when entering ``state``."""
        self._on_enter.setdefault(state, []).append(callback)
        return self

    def on_exit(self, state: str, callback: Action) -> FiniteStateMachine:
        """Register a callback fired when leaving ``state``."""
        self._on_exit.setdefault(state, []).append(callback)
        return self

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------
    def available_events(self) -> list[str]:
        """Events that are valid *from the current state*."""
        return sorted({t.event for t in self._transitions if t.source == self._state})

    def can_fire(self, event: str) -> bool:
        """Whether ``event`` has at least one matching rule right now."""
        return any(t.source == self._state and t.event == event for t in self._transitions)

    @property
    def history(self) -> list[TransitionRecord]:
        return list(self._history)

    def blocked_count(self, source: str, event: str) -> int:
        return self._blocked_count.get((source, event), 0)

    # ------------------------------------------------------------------
    # Core engine
    # ------------------------------------------------------------------
    def fire(self, event: str, payload: dict | None = None) -> bool:
        """Attempt to transition on ``event``.

        Returns True if a transition occurred, False if no matching rule
        existed or a guard blocked it.
        """
        payload = payload or {}
        for t in self._transitions:
            if t.source != self._state or t.event != event:
                continue
            # Guard check
            if t.guard is not None and not t.guard(self, payload):
                self._blocked_count[(self._state, event)] = (
                    self._blocked_count.get((self._state, event), 0) + 1
                )
                logger.debug("Transition %s blocked by guard (event=%s)", t, event)
                return False
            # Execute the transition
            self._execute(t, payload)
            return True
        # No matching rule at all
        logger.debug("No transition for event=%r from state=%r", event, self._state)
        return False

    def force_state(self, state: str, payload: dict | None = None) -> None:
        """Directly jump to ``state`` without firing an event.

        This bypasses on_exit callbacks of the old state but still runs
        on_enter of the new state. Intended for HIL corrections and resets.
        """
        old = self._state
        self._state = state
        self._history.append(TransitionRecord(old, "__force__", state, payload or {}))
        for cb in self._on_enter.get(state, []):
            cb(self, payload or {})
        logger.info("Force-set state %r -> %r", old, state)

    def reset(self) -> None:
        """Return to the initial state and clear history."""
        self._state = self._initial
        self._history.clear()
        self._blocked_count.clear()
        logger.info("FSM reset to initial state %r", self._initial)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _execute(self, transition: Transition, payload: dict) -> None:
        old = self._state
        # on_exit of the source state
        for cb in self._on_exit.get(old, []):
            cb(self, payload)
        # update state
        self._state = transition.target
        # transition action
        if transition.action is not None:
            transition.action(self, payload)
        # on_enter of the target state
        for cb in self._on_enter.get(transition.target, []):
            cb(self, payload)
        # record
        self._history.append(TransitionRecord(old, transition.event, transition.target, payload))
        logger.info("FSM %s --[%s]--> %s", old, transition.event, transition.target)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<FiniteStateMachine state={self._state!r} rules={len(self._transitions)}>"
