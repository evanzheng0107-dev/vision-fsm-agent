# Project Summary

> **Last updated**: 2026-07-02

---

## Overview

Vision FSM Agent is a lightweight Python framework for building
computer-vision-driven automation agents with finite-state-machine
control and human-in-the-loop correction.

- **Repository**: https://github.com/evanzheng0107-dev/vision-fsm-agent
- **License**: MIT
- **Latest release**: v0.1.1
- **Tags**: v0.1.0, v0.1.1
- **Python**: 3.9+
- **Tests**: 66 (all passing, CI integrated)

## Architecture

The framework consists of four independent modules:

- **FSM Engine** (`vision_fsm_agent.fsm`) — generic finite-state-machine
  with guards, actions, on_enter/on_exit callbacks, and transition history.
- **Vision Engine** (`vision_fsm_agent.vision`) — multi-scale OpenCV
  template matching with TemplateManager for multi-template management.
- **Decision Agents** (`vision_fsm_agent.agent`) — local rule-based and
  optional LLM-backed decision agents with graceful fallback.
- **HIL System** (`vision_fsm_agent.hil`) — Human-in-the-Loop correction
  over HTTP (Flask server + client).

## Current State

- **Releases**: v0.1.0 and v0.1.1 tagged with GitHub Releases
- **PRs merged**: 5 (refactor, 2 dependabot, v0.1.1 polish, docs finalization)
- **Issues**: 6 open (#5–#10) for roadmap and maintenance
- **Tests**: 66 passing (unit + integration + smoke)
- **CI**: test (Python 3.9–3.13 matrix) + lint (ruff/mypy/bandit)
- **OSS readiness**: 77 files, 0 risky words

## Safety Design

- Default environment is a **local synthetic demo** — no screen capture,
  no network (except optional local HIL), no external input.
- **No anti-detection, evasion, or human-mimicry** features.
- Optional live mode is opt-in, requires explicit configuration, keeps
  PyAutoGUI failsafe enabled.
- High-risk wording scanned by `scripts/oss_readiness_check.py` before
  every release.

## OSS Governance

Complete open-source governance: LICENSE (MIT), CONTRIBUTING,
CODE_OF_CONDUCT, SECURITY, AGENTS.md, issue/PR templates, CODEOWNERS,
dependabot, FUNDING, CITATION.cff, py.typed (PEP 561).

## Documentation

README (14 sections), architecture overview, demo walkthrough, HIL
workflow, safety boundaries, troubleshooting, API reference (5 files),
mkdocs site config, ReadTheDocs config, dev container.

## Maintenance Timeline

| Round | Date | Summary |
|-------|------|---------|
| Round 1 | 2026-06-29 | Project refactoring, README Quick Demo, oss_readiness_check.py |
| Round 2 | 2026-06-30 | 15 engineering gaps fixed (py.typed, CITATION, pre-commit, Makefile, CI, etc.) |
| Round 3 | 2026-07-02 | Package reorganization, CI lint fix, v0.1.0 release |
| Round 4 | 2026-07-02 | v0.1.1 polish (custom FSM example + smoke test), v0.1.1 release |
| Round 5 | 2026-07-02 | Documentation finalized, 6 GitHub issues created, final docs sweep |
