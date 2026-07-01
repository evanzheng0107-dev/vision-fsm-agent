"""Tests for the finite-state-machine engine."""
import pytest
from vision_fsm_agent.fsm import FiniteStateMachine


def test_initial_state():
    fsm = FiniteStateMachine("IDLE")
    assert fsm.current_state == "IDLE"


def test_basic_transition():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN")
    assert fsm.fire("GO") is True
    assert fsm.current_state == "RUN"


def test_no_matching_event_returns_false():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN")
    assert fsm.fire("UNKNOWN") is False
    assert fsm.current_state == "IDLE"


def test_guard_blocks_transition():
    fsm = FiniteStateMachine("IDLE")
    # guard returns False -> blocked
    fsm.add_transition("IDLE", "GO", "RUN", guard=lambda f, p: False)
    assert fsm.fire("GO") is False
    assert fsm.current_state == "IDLE"
    assert fsm.blocked_count("IDLE", "GO") == 1


def test_guard_allows_transition():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN", guard=lambda f, p: True)
    assert fsm.fire("GO") is True
    assert fsm.current_state == "RUN"


def test_action_callback():
    calls = []
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN", action=lambda f, p: calls.append(p))
    fsm.fire("GO", payload={"x": 1})
    assert calls == [{"x": 1}]


def test_on_enter_on_exit():
    entered, exited = [], []
    fsm = FiniteStateMachine("A")
    fsm.on_enter("B", lambda f, p: entered.append("B"))
    fsm.on_exit("A", lambda f, p: exited.append("A"))
    fsm.add_transition("A", "SWITCH", "B")
    fsm.fire("SWITCH")
    assert exited == ["A"]
    assert entered == ["B"]
    assert fsm.current_state == "B"


def test_history():
    fsm = FiniteStateMachine("A")
    fsm.add_transition("A", "GO", "B")
    fsm.add_transition("B", "BACK", "A")
    fsm.fire("GO")
    fsm.fire("BACK")
    assert len(fsm.history) == 2
    assert fsm.history[0].source == "A"
    assert fsm.history[0].target == "B"
    assert fsm.history[1].source == "B"
    assert fsm.history[1].target == "A"


def test_force_state():
    fsm = FiniteStateMachine("A")
    fsm.force_state("C")
    assert fsm.current_state == "C"
    assert fsm.history[-1].event == "__force__"


def test_reset():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN")
    fsm.fire("GO")
    fsm.reset()
    assert fsm.current_state == "IDLE"
    assert len(fsm.history) == 0


def test_available_events():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "A", "X")
    fsm.add_transition("IDLE", "B", "Y")
    fsm.add_transition("X", "C", "Z")
    assert set(fsm.available_events()) == {"A", "B"}
    fsm.fire("A")
    assert set(fsm.available_events()) == {"C"}


def test_can_fire():
    fsm = FiniteStateMachine("IDLE")
    fsm.add_transition("IDLE", "GO", "RUN")
    assert fsm.can_fire("GO") is True
    assert fsm.can_fire("NOPE") is False


def test_demo_fsm_builds():
    """The standard demo FSM should build without error and have transitions."""
    from vision_fsm_agent.main import build_demo_fsm

    fsm = build_demo_fsm()
    assert fsm.current_state == "IDLE"
    assert fsm.can_fire("FOUND_TARGET")
    assert fsm.can_fire("FOUND_PICKUP")
    assert fsm.can_fire("FOUND_INTERACT")
    assert fsm.can_fire("NO_TARGET")
