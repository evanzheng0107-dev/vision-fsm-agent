"""Smoke test: verify examples run independently from their own directories."""

import os
import subprocess
import sys


def _run_example(cwd: str, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_demo_runs_from_examples_dir():
    """The grid-world demo should run when invoked directly from its own directory."""
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    demo_dir = os.path.join(project_root, "examples", "visual_grid_world")
    result = _run_example(demo_dir, ["run_demo.py", "--steps", "5"])
    assert result.returncode == 0, f"Demo from examples dir failed: {result.stderr}"
    assert "[demo] World:" in result.stdout
    assert "[demo] Final status:" in result.stdout


def test_custom_fsm_runs_from_examples_dir():
    """The custom FSM example should run when invoked directly from its own directory."""
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    custom_fsm_dir = os.path.join(project_root, "examples", "custom_fsm")
    result = _run_example(custom_fsm_dir, ["custom_fsm.py"])
    assert result.returncode == 0, f"Custom FSM from examples dir failed: {result.stderr}"
    assert "Initial state: PATROL" in result.stdout
    assert "Transition history" in result.stdout


def test_demo_runs_via_arg_longer():
    """35 steps with default seed should complete all objectives."""
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = subprocess.run(
        [sys.executable, "examples/visual_grid_world/run_demo.py", "--steps", "35"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0
    assert "All items collected and buttons pressed. Done!" in result.stdout, (
        "35-step demo should reach completion"
    )
    assert "done=True" in result.stdout or "done': True" in result.stdout
