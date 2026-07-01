"""Smoke test: verify the demo runs end-to-end."""
import os
import sys
import subprocess


def test_demo_runs():
    """The demo should run 5 steps without error."""
    project_root = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    result = subprocess.run(
        [sys.executable, "examples/visual_grid_world/run_demo.py", "--steps", "5"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"Demo failed: {result.stderr}"
    assert "World:" in result.stdout or "demo" in result.stdout.lower()
