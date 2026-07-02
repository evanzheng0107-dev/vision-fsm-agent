#!/usr/bin/env python3
"""
Open-Source Readiness Checker for Vision FSM Agent.

Verifies:
  1. All expected governance, documentation, packaging, and CI files
     exist and are non-empty.
  2. No high-risk wording regression (game names, anti-detection terms).
  3. (Optional) pytest passes, when --run-tests is given.

Usage::

    python scripts/oss_readiness_check.py
    python scripts/oss_readiness_check.py --verbose
    python scripts/oss_readiness_check.py --run-tests

Exit code 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Required files: (relative_path, required, description)
# ------------------------------------------------------------------
REQUIRED_FILES = [
    # Governance
    ("README.md", True, "Project overview"),
    ("LICENSE", True, "MIT license text"),
    ("CONTRIBUTING.md", True, "Contribution guidelines"),
    ("CODE_OF_CONDUCT.md", True, "Contributor Covenant Code of Conduct"),
    ("SECURITY.md", True, "Security policy and vulnerability reporting"),
    ("CHANGELOG.md", True, "Keep a Changelog format version history"),
    ("AGENTS.md", True, "AI coding agent guidance"),
    ("CITATION.cff", True, "Citation File Format for academic use"),
    # Packaging
    ("pyproject.toml", True, "PEP 621 project metadata and tool config"),
    ("requirements.txt", True, "Pinned runtime dependencies"),
    (".gitignore", True, "Git ignore rules"),
    (".env.example", True, "Example environment variables"),
    (".editorconfig", True, "Editor configuration for consistent style"),
    ("config/default.yaml", True, "Default framework configuration"),
    ("Makefile", True, "Convenience commands for dev workflow"),
    (".pre-commit-config.yaml", True, "Pre-commit hooks configuration"),
    # Type marker
    ("src/vision_fsm_agent/py.typed", True, "PEP 561 typed-package marker", "allow_empty"),
    # Source package
    ("src/vision_fsm_agent/__init__.py", True, "Package init with __version__"),
    ("src/vision_fsm_agent/fsm.py", True, "FSM engine"),
    ("src/vision_fsm_agent/vision.py", True, "Vision engine"),
    ("src/vision_fsm_agent/agent.py", True, "Decision agents"),
    ("src/vision_fsm_agent/main.py", True, "Agent loop"),
    ("src/vision_fsm_agent/config.py", True, "Configuration loader"),
    ("src/vision_fsm_agent/cli.py", True, "CLI entry point"),
    ("src/vision_fsm_agent/hil/__init__.py", True, "HIL subpackage init"),
    ("src/vision_fsm_agent/hil/client.py", True, "HIL client"),
    ("src/vision_fsm_agent/hil/server.py", True, "HIL server"),
    ("src/vision_fsm_agent/envs/__init__.py", True, "Envs subpackage init"),
    ("src/vision_fsm_agent/envs/grid_world.py", True, "Demo grid world environment"),
    # Examples
    ("examples/visual_grid_world/run_demo.py", True, "Demo runner script"),
    ("examples/visual_grid_world/config.yaml", True, "Demo configuration"),
    ("examples/visual_grid_world/assets/target_goal.png", True, "Demo template"),
    ("examples/visual_grid_world/assets/pickup_item.png", True, "Demo template"),
    ("examples/visual_grid_world/assets/interact_button.png", True, "Demo template"),
    ("examples/custom_fsm/custom_fsm.py", True, "Custom FSM example"),
    # Documentation
    ("docs/architecture.md", True, "Architecture deep-dive"),
    ("docs/demo.md", True, "Demo walkthrough"),
    ("docs/hil-workflow.md", True, "HIL API reference"),
    ("docs/safety-boundaries.md", True, "Safety boundaries"),
    ("docs/troubleshooting.md", True, "Troubleshooting guide"),
    ("docs/api/README.md", True, "API reference index"),
    ("docs/api/fsm.md", True, "FSM API reference"),
    ("docs/api/vision.md", True, "Vision API reference"),
    ("docs/api/agent.md", True, "Agent API reference"),
    ("docs/api/hil.md", True, "HIL API reference"),
    ("docs/releases/v0.1.0.md", True, "v0.1.0 release notes"),
    # Doc site
    ("mkdocs.yml", False, "MkDocs documentation site config"),
    (".readthedocs.yaml", False, "ReadTheDocs configuration"),
    # Maintainer docs
    ("docs/maintainer/CODEX_OSS_APPLICATION.md", True, "Codex OSS application draft"),
    ("docs/maintainer/RELEASE_PLAN.md", True, "Release plan"),
    ("docs/maintainer/agent_ledger/README.md", True, "Maintenance ledger guide"),
    ("docs/maintainer/agent_ledger/SESSION_START.md", True, "Session start context"),
    ("docs/maintainer/agent_ledger/NEXT.md", True, "Current next task"),
    ("docs/maintainer/agent_ledger/PROGRESS.md", True, "Work round progress log"),
    ("docs/maintainer/agent_ledger/DECISIONS.md", True, "Key decisions record"),
    ("docs/maintainer/agent_ledger/ERRORS.md", True, "Errors and risks log"),
    # GitHub
    (".github/ISSUE_TEMPLATE/bug_report.yml", True, "Bug report issue template"),
    (".github/ISSUE_TEMPLATE/feature_request.yml", True, "Feature request issue template"),
    (".github/ISSUE_TEMPLATE/config.yml", False, "Issue template chooser config"),
    (".github/PULL_REQUEST_TEMPLATE.md", True, "Pull request template"),
    (".github/workflows/test.yml", True, "CI test workflow"),
    (".github/workflows/lint.yml", True, "CI lint workflow"),
    (".github/CODEOWNERS", True, "Code owners for PR review routing"),
    (".github/dependabot.yml", True, "Dependabot configuration"),
    (".github/FUNDING.yml", False, "Sponsorship configuration"),
    # Dev container
    (".devcontainer/devcontainer.json", False, "Dev container configuration"),
    # Tests
    ("tests/conftest.py", True, "Pytest configuration"),
    ("tests/unit/test_fsm.py", True, "FSM tests"),
    ("tests/unit/test_vision.py", True, "Vision tests"),
    ("tests/unit/test_agent.py", True, "Agent decision tests"),
    ("tests/unit/test_config.py", True, "Config tests"),
    ("tests/integration/test_hil.py", True, "HIL tests"),
    ("tests/integration/test_demo.py", True, "Demo end-to-end tests"),
    ("tests/smoke/test_demo_run.py", True, "Demo smoke test"),
    # Scripts
    ("scripts/generate_demo_assets.py", True, "Demo asset generator"),
    ("scripts/oss_readiness_check.py", False, "This script"),
]

# ------------------------------------------------------------------
# High-risk wording
# ------------------------------------------------------------------
# Chinese words: zero-tolerance. Any hit = FAIL.
RISKY_WORDS_CN = [
    "杖剑",
    "雷电",
    "防检测",
    "模拟人类",
    "7x24",
    "外挂",
    "自动刷",
    "商业游戏",
]

# English words/phrases: checked with negative-context exemption.
# Note: "bypass" is scanned as "bypass detection" (precise phrase) to
# avoid false positives on the technical usage "bypasses on_exit
# callbacks" in src/fsm.py.  See DECISIONS.md D006.
RISKY_WORDS_EN = [
    "anti-detection",
    "cheating",
    "botting",
    "bypass detection",
    "evade detection",
    "unattended farming",
]

# Negation markers: if the hit line or its ±1 line neighbours contain
# any of these (case-insensitive), the hit is exempted as a legitimate
# safety statement.
NEGATION_MARKERS = [
    "not ",
    "never ",
    "no ",
    "prohibit",
    "reject",
    "remove",
    "removed",
    "without ",
    "deliberately",
    "by design",
    "is not",
    "are not",
    "do not",
    "don't",
    "not for",
    "not intended",
    "will not",
    "will be rejected",
    "will be closed",
    "includes no",
    "shall not",
    "does not",
    "does **not**",
    "not add",
    "not include",
    # Meta-discussion markers: lines discussing the scan mechanism itself
    "is scanned",
    "scan uses",
    "scan strategy",
    "precise phrase",
    "instead of the bare",
]

# Files to exclude from scanning (self-referential word lists, etc.)
SCAN_EXCLUDE_FILES = {
    "oss_readiness_check.py",  # Contains the word list by definition
}

# File extensions to scan
SCAN_EXTENSIONS = {".py", ".md", ".yaml", ".yml", ".txt", ".example", ".toml", ".cfg"}

# Directories to exclude from scanning
SCAN_EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "venv",
    "env",
    ".venv",
    "demo_frames",
    ".coverage",
    "htmlcov",
    "node_modules",
    "build",
    "dist",
}


def _is_excluded(path: Path) -> bool:
    """Check if a path is within an excluded directory or is an excluded file."""
    for part in path.parts:
        if part in SCAN_EXCLUDE_DIRS:
            return True
    if path.name in SCAN_EXCLUDE_FILES:
        return True
    return False


def _strip_markdown(text: str) -> str:
    """Strip markdown bold/italic markers so negation detection works."""
    return text.replace("**", "").replace("__", "").replace("*", "")


def _has_negation_context(lines: list, idx: int) -> bool:
    """Check if the line at *idx* (and ±3 neighbours) has negation markers."""
    start = max(0, idx - 3)
    end = min(len(lines), idx + 4)
    window = _strip_markdown(" ".join(lines[start:end])).lower()
    return any(marker in window for marker in NEGATION_MARKERS)


def check_files(verbose: bool = False) -> tuple:
    """Check required files. Returns (missing, empty, ok_count)."""
    missing = []
    empty = []
    ok_count = 0

    for entry in REQUIRED_FILES:
        rel_path, required, desc = entry[0], entry[1], entry[2]
        allow_empty = len(entry) > 3 and entry[3] == "allow_empty"
        full = ROOT / rel_path
        if not full.exists():
            if required:
                missing.append((rel_path, desc))
                if verbose:
                    print(f"  MISSING (required): {rel_path}  -- {desc}")
            else:
                if verbose:
                    print(f"  missing (optional): {rel_path}  -- {desc}")
        elif full.stat().st_size == 0 and not allow_empty:
            empty.append((rel_path, desc))
            if verbose:
                print(f"  EMPTY: {rel_path}  -- {desc}")
        else:
            ok_count += 1
            if verbose:
                print(f"  OK: {rel_path}  ({full.stat().st_size} bytes)")

    return missing, empty, ok_count


def check_risky_words(verbose: bool = False) -> tuple:
    """Scan all text files for high-risk wording.

    Returns (cn_hits, en_hits_real, en_hits_exempt, files_scanned).
    Each hit is (rel_path, line_no, word, line_text).
    """
    cn_hits = []
    en_hits_real = []
    en_hits_exempt = []
    files_scanned = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip excluded dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SCAN_EXCLUDE_DIRS]

        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SCAN_EXTENSIONS:
                continue

            fpath = Path(dirpath) / fname
            rel = fpath.relative_to(ROOT)
            if _is_excluded(fpath):
                continue

            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            files_scanned += 1
            lines = text.splitlines()

            for i, line in enumerate(lines):
                line_lower = line.lower()

                # Chinese words: zero-tolerance
                for word in RISKY_WORDS_CN:
                    if word in line:
                        cn_hits.append((str(rel), i + 1, word, line.strip()))

                # English words: check with exemption
                for word in RISKY_WORDS_EN:
                    if word in line_lower:
                        if _has_negation_context(lines, i):
                            en_hits_exempt.append((str(rel), i + 1, word, line.strip()))
                            if verbose:
                                print(f"  EXEMPT: {rel}:{i + 1} -> {word}")
                        else:
                            en_hits_real.append((str(rel), i + 1, word, line.strip()))
                            if verbose:
                                print(f"  HIT:    {rel}:{i + 1} -> {word}")

    return cn_hits, en_hits_real, en_hits_exempt, files_scanned


def check_tests() -> tuple:
    """Run pytest. Returns (passed, returncode, output_summary)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        # Extract summary line
        output = result.stdout.strip().splitlines()
        summary = output[-1] if output else "(no output)"
        return (result.returncode == 0, result.returncode, summary)
    except subprocess.TimeoutExpired:
        return (False, -1, "pytest timed out (>120s)")
    except Exception as exc:
        return (False, -1, f"pytest error: {exc}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Open-Source Readiness Checker for Vision FSM Agent."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print status for every file and every word hit.",
    )
    parser.add_argument(
        "--run-tests", action="store_true", help="Also run pytest after the readiness check."
    )
    args = parser.parse_args()

    print("=== Open-Source Readiness Check ===\n")

    overall_pass = True
    actions = []

    # --- [1] File existence ---
    print("[1] File existence")
    missing, empty, ok_count = check_files(verbose=args.verbose)
    print(f"    Files OK:     {ok_count}")
    print(f"    Missing:      {len(missing)}" + (" (required)" if missing else ""))
    print(f"    Empty:        {len(empty)}")
    if missing:
        overall_pass = False
        for path, desc in missing:
            print(f"      - {path}  ({desc})")
        actions.append(f"Add missing required files: {', '.join(p for p, _ in missing)}")
    if empty:
        overall_pass = False
        for path, desc in empty:
            print(f"      - {path}  ({desc}) [EMPTY]")
        actions.append(f"Fill empty files: {', '.join(p for p, _ in empty)}")
    print()

    # --- [2] Risky wording scan ---
    print("[2] Risky wording scan")
    cn_hits, en_real, en_exempt, files_scanned = check_risky_words(verbose=args.verbose)
    print(f"    Files scanned:    {files_scanned}")
    print(f"    Chinese hits:     {len(cn_hits)}  (zero-tolerance)")
    print(f"    English hits:     {len(en_real)}  (real)")
    print(f"    English exempted: {len(en_exempt)}  (negative context)")

    if cn_hits:
        overall_pass = False
        print("\n    Chinese high-risk word hits:")
        for path, line, word, text in cn_hits:
            print(f"      {path}:{line}  ->  {word}")
            print(f"        {text[:120]}")
        actions.append("Remove Chinese high-risk words (game names, anti-detection terms)")

    if en_real:
        overall_pass = False
        print("\n    English high-risk word hits (no negation context):")
        for path, line, word, text in en_real:
            print(f"      {path}:{line}  ->  {word}")
            print(f"        {text[:120]}")
        actions.append("Remove or rephrase English high-risk words without negation context")

    if en_exempt and args.verbose:
        print("\n    English exempted hits (negative context — OK):")
        for path, line, word, _text in en_exempt:
            print(f"      {path}:{line}  ->  {word}  [EXEMPT]")
    print()

    # --- [3] Tests ---
    if args.run_tests:
        print("[3] Tests")
        if not overall_pass:
            print("    SKIPPED — fix readiness issues first.")
            actions.append("Re-run with --run-tests after fixing readiness issues")
        else:
            passed, rc, summary = check_tests()
            if passed:
                print("    pytest: PASS")
                print(f"    {summary}")
            else:
                print(f"    pytest: FAIL (exit code {rc})")
                print(f"    {summary}")
                overall_pass = False
                actions.append("Fix failing pytest tests")
        print()
    else:
        print("[3] Tests  (skipped — use --run-tests to enable)\n")

    # --- Result ---
    if overall_pass:
        print("=== Result: PASS ===")
    else:
        print("=== Result: FAIL ===")

    # --- Recommended next actions ---
    if actions:
        print("\nRecommended next actions:")
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action}")
    elif overall_pass:
        print("\nRecommended next actions:")
        print("  1. Commit changes (respect 'no push without approval' constraint)")
        print("  2. Consider integrating oss_readiness_check into CI")
        print("  3. Proceed to the next maintenance task in NEXT.md")

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
