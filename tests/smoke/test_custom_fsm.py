"""Smoke test: verify the custom FSM example runs end-to-end."""

import os
import subprocess
import sys


def test_custom_fsm_runs():
    """The custom FSM example should run without error and produce
    the expected transition history."""
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = subprocess.run(
        [sys.executable, "examples/custom_fsm/custom_fsm.py"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"Custom FSM example failed: {result.stderr}"

    # Key markers that should appear in the output.
    assert "Initial state: PATROL" in result.stdout
    assert "Available events:" in result.stdout
    assert "Transition history" in result.stdout

    # The WAIT fallback path should have fired at least once.
    assert "STUCK" in result.stdout, "STUCK event never fired in custom FSM example"
    assert "WAIT" in result.stdout, "WAIT state never entered in custom FSM example"
    assert "READY" in result.stdout, "READY recovery event never fired"

    # Normal SCAN path should also be present.
    assert "SPOTTED" in result.stdout
    assert "SCAN" in result.stdout
    assert "DONE" in result.stdout
