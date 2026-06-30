"""End-to-end tests for the demo environment and agent loop."""
import os
import sys
import pytest
import numpy as np

from visual_grid_world import DemoEnvironment, make_goal_template, make_item_template, make_button_template
from main import AgentLoop, load_config
from vision import TemplateManager


@pytest.fixture
def config():
    return load_config()


@pytest.fixture
def env(config):
    return DemoEnvironment(config)


def test_env_initial_state(env):
    assert env.agent_pos == (0, 0)
    assert len(env.goals) >= 1
    assert len(env.items) >= 1
    assert len(env.buttons) >= 1
    assert env.step_count == 0


def test_env_frame_is_valid_image(env):
    frame = env.get_frame()
    assert frame is not None
    assert frame.ndim == 3
    assert frame.shape[2] == 3  # BGR
    w, h = env.bounds
    assert frame.shape[0] == h
    assert frame.shape[1] == w


def test_env_actions_advance_state(env):
    initial_pos = env.agent_pos
    env.perform_action("explore")
    assert env.step_count == 1
    # explore may or may not move, but step_count must increment
    env.perform_action("wait")
    assert env.step_count == 2


def test_env_pickup_collects_adjacent_item():
    env = DemoEnvironment({"demo_seed": 42})
    # Force an item adjacent to the agent.
    env.items = [(1, 0)]
    env.collected = set()
    env.agent_pos = (0, 0)
    env.perform_action("pickup")
    assert 0 in env.collected


def test_env_interact_presses_adjacent_button():
    env = DemoEnvironment({"demo_seed": 42})
    env.buttons = [(0, 1)]
    env.pressed = set()
    env.agent_pos = (0, 0)
    env.perform_action("interact")
    assert 0 in env.pressed


def test_env_reproducible_with_seed():
    env1 = DemoEnvironment({"demo_seed": 99})
    env2 = DemoEnvironment({"demo_seed": 99})
    assert env1.goals == env2.goals
    assert env1.items == env2.items
    assert env1.buttons == env2.buttons


def test_agent_loop_runs_steps(config, env):
    """The full agent loop should run a few steps without error."""
    loop = AgentLoop(env, config, use_hil=False)
    # Load templates.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(root, "assets", "demo")
    loop.vision.load_directory(assets)
    assert len(loop.vision) > 0

    for _ in range(5):
        loop.step()

    assert loop.loop_count == 5
    assert env.step_count == 5


def test_agent_loop_completes_demo(config):
    """Given enough steps, the agent should collect all items and press buttons."""
    env = DemoEnvironment(config)
    loop = AgentLoop(env, config, use_hil=False)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loop.vision.load_directory(os.path.join(root, "assets", "demo"))

    for _ in range(60):
        loop.step()
        if env.status()["done"]:
            break

    st = env.status()
    assert st["items_collected"] == st["items_total"], "Not all items collected"
    assert st["buttons_pressed"] == st["buttons_total"], "Not all buttons pressed"


def test_fsm_transitions_during_run(config, env):
    """The FSM should record transitions during a run."""
    loop = AgentLoop(env, config, use_hil=False)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loop.vision.load_directory(os.path.join(root, "assets", "demo"))

    for _ in range(10):
        loop.step()

    # The FSM should have transitioned at least once.
    assert len(loop.fsm.history) > 0


def test_close_is_safe(env):
    """close() should not raise."""
    env.close()
