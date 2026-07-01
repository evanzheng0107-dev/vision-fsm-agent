# Codex for Open Source Application Draft

> Working draft. Updated as evidence accumulates.

---

## Repository

**Vision FSM Agent**

A lightweight Python framework for building computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction.

**URL**: https://github.com/evanzheng0107-dev/sword-legend-explorer
**Branch**: `refactor/vision-fsm-agent` (pushed, PR pending merge to `master`)
**License**: MIT
**Version**: 0.1.0 (pending tag)

## Maintainer Role

I am the primary maintainer of Vision FSM Agent. I define the project
direction, maintain the roadmap, review changes, manage releases, update
documentation, maintain tests, and enforce safety boundaries.

Over the past 3 days I have:
- Refactored the project from a game-specific prototype into a
  general-purpose, safe, educational framework
- Committed 5 incremental, well-documented changes with conventional
  commit messages
- Pushed all changes to a public feature branch
- Maintained a detailed change log and maintenance ledger

## Repository Qualification

Vision FSM Agent is a public Python framework for computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction. It provides a reproducible synthetic demo, 61 tests, CI (test
+ lint), safety boundaries, complete OSS governance, and documentation
for researchers and developers exploring visual agents in controlled local
environments.

The project was refactored from a game-specific prototype into a
public-safe, general-purpose framework. It now uses a synthetic demo
environment, avoids third-party assets, includes safety boundaries, and
is maintained through issues, pull requests, CI, changelog, and releases.

## API Credits Usage

I will use API credits for core OSS maintenance: improving documentation,
generating and reviewing tests, triaging issues, preparing release notes,
reviewing pull requests, and experimenting with optional LLM-assisted
decision modules while keeping all outputs human-reviewed.

## Safety Boundaries

- The default environment is a **local synthetic demo** — no screen
  capture, no network (except optional local HIL), no external input.
- The project includes **no anti-detection, evasion, or human-mimicry**
  features.
- The optional live mode is opt-in, requires explicit configuration, and
  keeps PyAutoGUI's failsafe enabled.
- High-risk wording (game names, anti-detection terms) is scanned by
  `scripts/oss_readiness_check.py` before every release.

## Human-Reviewed AI Usage

All AI-assisted development is human-reviewed. The maintainer
(1) reviews every file change, (2) runs the test suite before commits,
(3) runs the OSS readiness check, and (4) enforces safety boundaries
documented in `docs/safety-boundaries.md`.

## Evidence Checklist

| Item | Status | Evidence |
|------|--------|----------|
| Public repo | ✅ | https://github.com/evanzheng0107-dev/sword-legend-explorer |
| Branch pushed | ✅ | `refactor/vision-fsm-agent` (5 commits) |
| License | ✅ | MIT (`LICENSE`) |
| CI | ✅ | test.yml (matrix) + lint.yml (ruff/mypy/bandit) |
| Tests | ✅ | 61 pytest tests, all passing |
| Release | Pending | v0.1.0 code complete, docs/releases/v0.1.0.md ready, awaiting tag |
| Issues | Pending | To be created on GitHub |
| PRs | Pending | PR for branch merge pending |
| Docs | ✅ | README (14 sections), architecture, demo, HIL workflow, safety boundaries, troubleshooting, API reference (5 files), releases |
| Safety boundaries | ✅ | `docs/safety-boundaries.md`, `SECURITY.md`, `AGENTS.md` |
| AGENTS.md | ✅ | Present with safety rules and contribution policy |
| Changelog | ✅ | `CHANGELOG.md` (Keep a Changelog format, with link definitions) |
| Maintenance evidence | ✅ | `docs/agent_ledger/` with 7 tracking files (PROGRESS P001–P004) |
| OSS readiness check | ✅ | `scripts/oss_readiness_check.py` — 66 files OK, 0 missing, 0 risky |
| Code quality | ✅ | pre-commit config, ruff/mypy/bandit config, py.typed |
| Packaging | ✅ | pyproject.toml with scripts, extras, tool config |
| Contributing guide | ✅ | CONTRIBUTING.md with Development Setup, Makefile, pre-commit |
| Citation | ✅ | CITATION.cff |

## Application Short Statement (≤500 characters)

Vision FSM Agent is a public Python framework for CV-driven automation
with FSM control and human-in-the-loop correction. It features a
reproducible synthetic demo, 61 tests, CI (test + lint), safety
boundaries, and complete OSS governance. I will use API credits for
documentation, test generation, issue triage, release notes, and
human-reviewed LLM-assisted development.

## Remaining Steps

1. Merge `refactor/vision-fsm-agent` → `master` (via PR)
2. Tag `v0.1.0` on `master`
3. Create GitHub Release with release notes
4. Create 5–8 GitHub issues
5. Complete Day 4–5 maintenance tasks
6. Finalize `docs/codex-for-oss-application.md`
7. Submit application after visible maintenance activity
