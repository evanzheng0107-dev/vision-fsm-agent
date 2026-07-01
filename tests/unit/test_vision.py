"""Tests for the vision / template-matching engine."""
import os
import numpy as np
import pytest

from vision_fsm_agent.vision import TemplateManager, MatchResult, multi_scale_match
from vision_fsm_agent.envs.grid_world import (
    DemoEnvironment,
    make_goal_template,
    make_item_template,
    make_button_template,
)


@pytest.fixture
def env():
    return DemoEnvironment({"demo_seed": 42})


@pytest.fixture
def mgr():
    m = TemplateManager(confidence_threshold=0.7)
    m.add_from_array("target_goal", make_goal_template())
    m.add_from_array("pickup_item", make_item_template())
    m.add_from_array("interact_button", make_button_template())
    return m


def test_multi_scale_match_finds_template():
    """A template placed in a frame should be found with high confidence."""
    template = make_goal_template()
    # Place the template in a larger frame at a known location.
    frame = np.zeros((200, 200, 3), dtype=np.uint8)
    frame[20:60, 80:120] = template
    val, pos = multi_scale_match(template, frame, (0.9, 1.1), 3)
    assert val > 0.8
    assert pos[0] == 80  # x
    assert pos[1] == 20  # y


def test_multi_scale_match_returns_zero_for_none():
    assert multi_scale_match(None, np.zeros((10, 10), dtype=np.uint8)) == (0.0, (0, 0))
    assert multi_scale_match(np.zeros((10, 10), dtype=np.uint8), None) == (0.0, (0, 0))


def test_template_manager_load(env, mgr):
    assert len(mgr) == 3
    assert "target_goal" in mgr
    assert "pickup_item" in mgr
    assert "interact_button" in mgr


def test_match_all_finds_elements(env, mgr):
    """The demo frame should contain at least one of each element type."""
    frame = env.get_frame()
    results = mgr.match_all(frame)
    found_names = {r.template_name for r in results if r.found}
    assert "target_goal" in found_names
    assert "pickup_item" in found_names
    assert "interact_button" in found_names


def test_match_best_returns_highest(env, mgr):
    frame = env.get_frame()
    best = mgr.match_best(frame)
    assert best.confidence > 0
    # Results from match_all should be sorted descending.
    results = mgr.match_all(frame)
    confidences = [r.confidence for r in results]
    assert confidences == sorted(confidences, reverse=True)


def test_match_result_dataclass():
    r = MatchResult(found=True, confidence=0.9, position=(1, 2), center=(5, 6), template_name="x")
    assert r.found is True
    assert r.center == (5, 6)
    assert r.template_name == "x"


def test_load_directory(tmp_path):
    """Loading templates from a directory should work."""
    import cv2

    cv2.imwrite(str(tmp_path / "a.png"), make_goal_template())
    cv2.imwrite(str(tmp_path / "b.png"), make_item_template())
    mgr = TemplateManager()
    count = mgr.load_directory(str(tmp_path))
    assert count == 2
    assert "a" in mgr.names
    assert "b" in mgr.names


def test_match_one_unknown_template():
    mgr = TemplateManager()
    r = mgr.match_one("nonexistent", np.zeros((40, 40), dtype=np.uint8))
    assert r.found is False
    assert r.confidence == 0.0


def test_assets_demo_exists():
    """The generated demo assets should exist on disk."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assets = os.path.join(root, "examples", "visual_grid_world", "assets")
    assert os.path.isdir(assets)
    for name in ("target_goal.png", "pickup_item.png", "interact_button.png"):
        assert os.path.exists(os.path.join(assets, name)), f"Missing {name}"
