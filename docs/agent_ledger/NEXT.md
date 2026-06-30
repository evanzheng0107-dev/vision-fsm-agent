# NEXT

## Current Date

2026-06-30

## Current Stage

Day 1 — README and demo clarity.

## Current Task

Improve README Quick Demo visibility and add reproducible demo
documentation.

## Acceptance Criteria

- README includes a Quick Demo section with copy-paste commands
- `docs/demo.md` exists with demo explanation and expected output
- Demo command is documented and reproducible
- `pytest tests/ -q` passes
- `python scripts/oss_readiness_check.py` passes
- `CHANGELOG.md` updated under `[Unreleased]`
- No risky wording regression
- `PROGRESS.md` updated

## Allowed Files

- `README.md`
- `docs/demo.md`
- `CHANGELOG.md`
- `docs/agent_ledger/PROGRESS.md`
- `docs/agent_ledger/NEXT.md`

## Forbidden Changes

- Do not modify `docs/safety-boundaries.md` unless fixing clarity
- Do not reintroduce game-specific wording
- Do not remove tests
- Do not modify `src/` code
- Do not push or release

## Next Round Prompt (after Day 1 completion)

```
/goal complete Day 2 contributor experience tasks for Vision FSM Agent:
improve CONTRIBUTING, add troubleshooting documentation, update PR template
safety checklist, update CHANGELOG and PROGRESS, run pytest and
oss_readiness_check, ensure no risky wording regression, and leave git
status clean or clearly report pending changes.
```
