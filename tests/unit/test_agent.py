"""Tests for the decision agents (src/agent.py)."""
import pytest

from vision_fsm_agent.agent import (
    LocalDecisionAgent,
    CloudDecisionAgent,
    DecisionAgent,
    ACTIONS,
)


# ----------------------------------------------------------------------
# LocalDecisionAgent — priority rules
# ----------------------------------------------------------------------
def test_local_agent_priority_interact():
    """interact should take priority over pickup and target."""
    agent = LocalDecisionAgent()
    state = {
        "match_results": {
            "interact": {"found": True},
            "pickup": {"found": True},
            "target": {"found": True},
        }
    }
    d = agent.get_decision(state)
    assert d["action"] == "interact"


def test_local_agent_priority_pickup():
    """pickup should take priority over target when interact is absent."""
    agent = LocalDecisionAgent()
    state = {
        "match_results": {
            "interact": {"found": False},
            "pickup": {"found": True},
            "target": {"found": True},
        }
    }
    d = agent.get_decision(state)
    assert d["action"] == "pickup"


def test_local_agent_priority_move():
    """move should be chosen when only target is found."""
    agent = LocalDecisionAgent()
    state = {
        "match_results": {
            "interact": {"found": False},
            "pickup": {"found": False},
            "target": {"found": True},
        }
    }
    d = agent.get_decision(state)
    assert d["action"] == "move"


def test_local_agent_wait_on_failures():
    """wait should be chosen when failures exceed threshold."""
    agent = LocalDecisionAgent(failure_threshold=3)
    state = {
        "match_results": {},
        "failed_attempts": 5,
    }
    d = agent.get_decision(state)
    assert d["action"] == "wait"


def test_local_agent_explore_default():
    """explore should be chosen when nothing is found and no failures."""
    agent = LocalDecisionAgent()
    state = {"match_results": {}, "failed_attempts": 0}
    d = agent.get_decision(state)
    assert d["action"] == "explore"


# ----------------------------------------------------------------------
# LocalDecisionAgent — edge cases
# ----------------------------------------------------------------------
def test_local_agent_decision_count_increments():
    """Each call should increment the internal decision counter."""
    agent = LocalDecisionAgent()
    assert agent.decision_count == 0
    agent.get_decision({"match_results": {}})
    assert agent.decision_count == 1
    agent.get_decision({"match_results": {}})
    assert agent.decision_count == 2


def test_local_agent_empty_state():
    """An empty agent_state should default to explore."""
    agent = LocalDecisionAgent()
    d = agent.get_decision({})
    assert d["action"] == "explore"


def test_local_agent_interact_over_all():
    """interact wins even when pickup and target are also found."""
    agent = LocalDecisionAgent()
    state = {
        "match_results": {
            "interact": {"found": True, "confidence": 0.5},
            "pickup": {"found": True, "confidence": 0.99},
            "target": {"found": True, "confidence": 0.99},
        }
    }
    d = agent.get_decision(state)
    assert d["action"] == "interact"


def test_local_agent_failure_threshold_boundary():
    """At exactly the threshold, should NOT wait (only > threshold waits)."""
    agent = LocalDecisionAgent(failure_threshold=3)
    state = {"match_results": {}, "failed_attempts": 3}
    d = agent.get_decision(state)
    assert d["action"] == "explore"  # 3 is not > 3


# ----------------------------------------------------------------------
# ACTIONS vocabulary
# ----------------------------------------------------------------------
def test_actions_vocabulary():
    for a in ("move", "pickup", "interact", "explore", "wait", "continue"):
        assert a in ACTIONS


def test_actions_is_tuple():
    assert isinstance(ACTIONS, tuple)


# ----------------------------------------------------------------------
# CloudDecisionAgent — fallback behavior
# ----------------------------------------------------------------------
def test_cloud_agent_falls_back_without_key(monkeypatch):
    """CloudDecisionAgent should use local fallback when no API key is set."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    agent = CloudDecisionAgent()
    assert agent.api_key is None
    d = agent.get_decision({"match_results": {"target": {"found": True}}})
    assert d["action"] == "move"


def test_cloud_agent_has_fallback():
    """CloudDecisionAgent should always have a fallback agent."""
    agent = CloudDecisionAgent()
    assert agent.fallback is not None
    assert isinstance(agent.fallback, LocalDecisionAgent)


def test_cloud_agent_extract_json():
    """_extract_json should parse valid JSON from model output."""
    agent = CloudDecisionAgent()
    assert agent._extract_json('{"action": "move", "reason": "test"}') == {
        "action": "move",
        "reason": "test",
    }
    assert agent._extract_json('```json\n{"action": "wait"}\n```') == {
        "action": "wait"
    }
    assert agent._extract_json("not json at all") is None


# ----------------------------------------------------------------------
# DecisionAgent base class
# ----------------------------------------------------------------------
def test_decision_agent_base_raises():
    """The base DecisionAgent should raise NotImplementedError."""
    base = DecisionAgent()
    with pytest.raises(NotImplementedError):
        base.get_decision({})
