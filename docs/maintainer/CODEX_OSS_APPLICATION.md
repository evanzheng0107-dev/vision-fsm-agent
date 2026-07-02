# Codex for Open Source — Application

> **Status**: Ready for submission
> **Last updated**: 2026-07-02

---

## Repository

**Vision FSM Agent**

A lightweight Python framework for building computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction.

- **URL**: https://github.com/evanzheng0107-dev/sword-legend-explorer
- **License**: MIT
- **Latest release**: v0.1.1 (tagged, GitHub Release published)
- **Tags**: v0.1.0, v0.1.1
- **Python**: 3.9+
- **Tests**: 63 (all passing, CI integrated)

## Maintainer Role

I am the primary maintainer of Vision FSM Agent. I define the project
direction, maintain the roadmap, review changes, manage releases, update
documentation, maintain tests, and enforce safety boundaries.

Over 5 days of active maintenance I have:

- Refactored the project from a game-specific prototype into a
  general-purpose, safe, educational framework (Day 1–3)
- Reorganized the codebase into a standard Python package layout with
  `src/vision_fsm_agent/` and subpackages (Day 3)
- Fixed 15 engineering gaps (py.typed, CITATION.cff, pre-commit, Makefile,
  dependabot, lint CI, FUNDING, mkdocs, ReadTheDocs, devcontainer, etc.)
  (Day 2)
- Resolved 137 ruff lint errors and ensured CI passes (Day 3)
- Published v0.1.0 with formal release notes and GitHub Release (Day 3)
- Improved the custom FSM example with visible state transitions and a
  fallback-path demonstration; added smoke test (Day 4)
- Published v0.1.1 with GitHub Release (Day 4)
- Merged 4 PRs (1 feature + 2 dependabot + 1 polish) via GitHub PR workflow
- Created GitHub issues for roadmap items and maintenance tasks (Day 5)

All commits use conventional commit messages. The maintenance ledger
(`docs/maintainer/agent_ledger/`) documents every work session with
PROGRESS, DECISIONS, ERRORS, and NEXT files.

## Repository Qualification

Vision FSM Agent is a public Python framework for computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction. It provides:

- A reproducible **synthetic demo environment** (grid world rendered with
  OpenCV/numpy — zero external dependencies, no screen capture)
- **63 tests** across unit, integration, and smoke layers
- **CI** with two workflows: test matrix (Python 3.9–3.13) + lint
  (ruff + mypy + bandit)
- **Safety boundaries** documented and enforced
- **Complete OSS governance**: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT,
  SECURITY, issue/PR templates, CODEOWNERS, dependabot, FUNDING
- **Documentation**: README (14 sections), architecture, demo, HIL
  workflow, safety boundaries, troubleshooting, API reference (5 files),
  mkdocs site, ReadTheDocs config
- **Packaging**: pyproject.toml with PEP 621 metadata, scripts entry
  point, optional extras (live, cloud, dev), py.typed marker
- **Releases**: v0.1.0 and v0.1.1 tagged with GitHub Releases

The project was refactored from a game-specific prototype into a
public-safe, general-purpose framework. It now uses a synthetic demo
environment, avoids third-party assets, includes safety boundaries, and
is maintained through issues, pull requests, CI, changelog, and releases.

## API Credits Usage

I will use API credits for core OSS maintenance:

- **Documentation**: improving docstrings, generating API reference
  examples, writing troubleshooting guides
- **Test generation**: expanding test coverage, generating edge-case
  tests, property-based testing
- **Issue triage**: categorising issues, proposing labels, drafting
  responses
- **Release notes**: generating changelogs, release notes, upgrade guides
- **Code review**: reviewing pull requests, suggesting improvements,
  checking safety boundaries
- **LLM-assisted development**: experimenting with optional LLM-backed
  decision agents while keeping all outputs human-reviewed

## Safety Boundaries

- The default environment is a **local synthetic demo** — no screen
  capture, no network (except optional local HIL), no external input.
- The project includes **no anti-detection, evasion, or human-mimicry**
  features.
- The optional live mode is opt-in, requires explicit configuration, and
  keeps PyAutoGUI's failsafe enabled.
- High-risk wording (game names, anti-detection terms) is scanned by
  `scripts/oss_readiness_check.py` before every release.
- The scan enforces **zero-tolerance** for Chinese risky words and
  **negative-context exemption** for English terms used in safety
  documentation.

## Human-Reviewed AI Usage

All AI-assisted development is human-reviewed. The maintainer:

1. Reviews every file change before commit
2. Runs the test suite (63 tests) before every commit
3. Runs the OSS readiness check before every release
4. Enforces safety boundaries documented in `docs/safety-boundaries.md`
5. Uses conventional commit messages for traceability
6. Maintains a detailed change log and maintenance ledger

## Evidence Checklist

| Item | Status | Evidence |
|------|--------|----------|
| Public repo | ✅ | https://github.com/evanzheng0107-dev/sword-legend-explorer |
| License | ✅ | MIT (`LICENSE`) |
| CI — tests | ✅ | `.github/workflows/test.yml` (Python 3.9–3.13 matrix) |
| CI — lint | ✅ | `.github/workflows/lint.yml` (ruff + mypy + bandit) |
| Tests | ✅ | 63 pytest tests, all passing |
| Release v0.1.0 | ✅ | Tag `v0.1.0`, GitHub Release published |
| Release v0.1.1 | ✅ | Tag `v0.1.1`, GitHub Release published |
| PRs merged | ✅ | 4 PRs merged (#1 refactor, #2–3 dependabot, #4 v0.1.1 polish) |
| Issues | ✅ | GitHub issues created for roadmap and maintenance |
| Docs | ✅ | README (14 sections), architecture, demo, HIL, safety, troubleshooting, API ref (5 files), mkdocs, ReadTheDocs |
| Safety boundaries | ✅ | `docs/safety-boundaries.md`, `SECURITY.md`, `AGENTS.md` |
| AGENTS.md | ✅ | Present with safety rules and contribution policy |
| Changelog | ✅ | `CHANGELOG.md` (Keep a Changelog format, v0.1.0 + v0.1.1 entries, link definitions) |
| Maintenance evidence | ✅ | `docs/maintainer/agent_ledger/` — 7 files (PROGRESS P001–P008, DECISIONS D001–D007, ERRORS, NEXT, SESSION_START) |
| OSS readiness check | ✅ | `scripts/oss_readiness_check.py` — 77 files OK, 0 missing, 0 risky words |
| Code quality | ✅ | pre-commit config, ruff/mypy/bandit config, py.typed (PEP 561) |
| Packaging | ✅ | `pyproject.toml` with scripts, extras, tool config |
| Contributing guide | ✅ | `CONTRIBUTING.md` with Development Setup, Makefile, pre-commit, Dev Container |
| Citation | ✅ | `CITATION.cff` |
| Dependabot | ✅ | `.github/dependabot.yml` (pip + github-actions) |
| Dev container | ✅ | `.devcontainer/devcontainer.json` |
| Issue templates | ✅ | bug_report.yml, feature_request.yml, config.yml |
| PR template | ✅ | `.github/PULL_REQUEST_TEMPLATE.md` with safety checklist |
| Code of Conduct | ✅ | `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1) |
| FUNDING | ✅ | `.github/FUNDING.yml` |

## Application Short Statement (≤500 characters)

Vision FSM Agent is a public Python framework for CV-driven automation
with FSM control and human-in-the-loop correction. It features a
reproducible synthetic demo, 63 tests, CI (test + lint), safety
boundaries, and complete OSS governance. I will use API credits for
documentation, test generation, issue triage, release notes, and
human-reviewed LLM-assisted development.

## Maintenance Timeline

| Day | Date | Summary |
|-----|------|---------|
| Day 1 | 2026-06-29 | Project refactoring, README Quick Demo, CODE_OF_CONDUCT, pyproject.toml, oss_readiness_check.py |
| Day 2 | 2026-06-30 | 15 engineering gaps fixed (py.typed, CITATION.cff, pre-commit, Makefile, dependabot, lint CI, FUNDING, mkdocs, ReadTheDocs, devcontainer, etc.) |
| Day 3 | 2026-07-02 | Package reorganization (src/vision_fsm_agent/), CI lint fix (137 ruff errors), v0.1.0 release (tag + GitHub Release) |
| Day 4 | 2026-07-02 | v0.1.1 polish (custom FSM example improvement, smoke test), v0.1.1 release (tag + GitHub Release), dependabot PRs merged |
| Day 5 | 2026-07-02 | Codex application finalized, GitHub issues created, final documentation sweep |
