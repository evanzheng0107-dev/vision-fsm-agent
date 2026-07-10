"""Smoke test: verify the demo runs end-to-end with expected output."""

import os
import subprocess
import sys


def test_demo_runs_and_produces_expected_output():
    """The demo should run 10 steps without error and produce the
    expected progress markers and final status report."""
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    result = subprocess.run(
        [sys.executable, "examples/visual_grid_world/run_demo.py", "--steps", "10"],
        cwd=project_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"Demo failed with exit code {result.returncode}: {result.stderr}"
    )

    output = result.stdout

    # Header markers.
    assert "[demo] Loaded" in output, "Missing template loading message"
    assert "[demo] World:" in output, "Missing world configuration message"
    assert "12x12" in output, "Missing grid size"
    assert "[demo] Running" in output, "Missing 'Running' message"

    # Step output format: "step   N | fsm=STATE  pos=(x, y) | ..."
    assert "step   1 | fsm=" in output, "Missing step 1 output"
    assert "pos=(" in output, "Missing agent position in step output"
    assert "items[" in output, "Missing item progress indicator"
    assert "buttons[" in output, "Missing button progress indicator"

    # Completion markers.
    assert "[demo] Final status:" in output, "Missing final status report"
    assert "done" in output.lower(), "Missing done flag in final status"
    assert "items_collected" in output, "Missing items_collected in final status"
    assert "buttons_pressed" in output, "Missing buttons_pressed in final status"
