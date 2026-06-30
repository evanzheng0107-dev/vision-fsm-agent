# NEXT

## Current Date

2026-06-30

## Current Stage

Day 2 — Contributor experience and troubleshooting.

## Current Task

Improve contributor onboarding and add troubleshooting documentation.

## Acceptance Criteria

- `CONTRIBUTING.md` covers local development setup
- `docs/troubleshooting.md` covers OpenCV, Windows, headless, pytest
  common issues
- PR template has safety checklist (verify, not add — should already exist)
- README has a Development Setup section
- `pytest tests/ -q` passes
- `python scripts/oss_readiness_check.py` passes
- `CHANGELOG.md` updated
- `PROGRESS.md` updated
- No risky wording regression

## Allowed Files

- `CONTRIBUTING.md`
- `docs/troubleshooting.md`
- `README.md` (Development Setup section only)
- `CHANGELOG.md`
- `docs/agent_ledger/PROGRESS.md`
- `docs/agent_ledger/NEXT.md`
- `.github/PULL_REQUEST_TEMPLATE.md` (verify safety checklist exists)

## Forbidden Changes

- Do not modify `docs/safety-boundaries.md` unless fixing clarity
- Do not reintroduce game-specific wording
- Do not remove tests
- Do not modify `src/` code
- Do not push or release

## Next Round Prompt (after Day 2 completion)

```
/goal prepare v0.1.0 release materials for Vision FSM Agent: verify README,
LICENSE, SECURITY, AGENTS, docs, examples, CI workflow, pytest, CHANGELOG,
and safety boundaries; generate docs/releases/v0.1.0.md; update RELEASE_PLAN
and PROGRESS; run oss_readiness_check; leave git status clean or clearly
report pending changes.
```
