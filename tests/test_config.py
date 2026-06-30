"""Tests for config loading and the decision agent."""
import os
import pytest

from main import load_config
from agent import LocalDecisionAgent, ACTIONS


def test_load_config_finds_yaml():
    """load_config should find the project's config.yaml."""
    config = load_config()
    assert isinstance(config, dict)
    assert "environment" in config
    assert config["environment"] == "demo"
    assert "demo_max_steps" in config


def test_config_has_demo_defaults():
    config = load_config()
    assert config.get("demo_grid_w", 12) == 12
    assert config.get("confidence_default", 0.8) == 0.75
    assert "scale_range" in config


def test_local_agent_priority_interact():
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
    agent = LocalDecisionAgent(failure_threshold=3)
    state = {
        "match_results": {},
        "failed_attempts": 5,
    }
    d = agent.get_decision(state)
    assert d["action"] == "wait"


def test_local_agent_explore_default():
    agent = LocalDecisionAgent()
    state = {"match_results": {}, "failed_attempts": 0}
    d = agent.get_decision(state)
    assert d["action"] == "explore"


def test_actions_vocabulary():
    for a in ("move", "pickup", "interact", "explore", "wait", "continue"):
        assert a in ACTIONS


def test_cloud_agent_falls_back_without_key(monkeypatch):
    """CloudDecisionAgent should use local fallback when no API key is set."""
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    from agent import CloudDecisionAgent

    agent = CloudDecisionAgent()
    assert agent.api_key is None
    d = agent.get_decision({"match_results": {"target": {"found": True}}})
    assert d["action"] == "move"
