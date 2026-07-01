# NEXT

## Current Date

2026-07-01

## Current Stage

Day 3 — v0.1.0 release preparation.

## Current Task

Prepare v0.1.0 release materials and finalize release workflow evidence.

## Acceptance Criteria

- `docs/releases/v0.1.0.md` is complete and consistent with CHANGELOG
- `CHANGELOG.md` `[0.1.0]` section matches release notes
- README / LICENSE / SECURITY / AGENTS / docs are complete
- `pytest tests/ -q` passes
- `python scripts/oss_readiness_check.py` passes
- `RELEASE_PLAN.md` updated
- `CODEX_OSS_APPLICATION.md` updated
- `PROGRESS.md` updated
- No risky wording regression
- All changes committed and pushed

## Allowed Files

- `docs/releases/v0.1.0.md`
- `CHANGELOG.md`
- `docs/agent_ledger/RELEASE_PLAN.md`
- `docs/agent_ledger/CODEX_OSS_APPLICATION.md`
- `docs/agent_ledger/PROGRESS.md`
- `docs/agent_ledger/NEXT.md`
- `README.md` (if release-specific updates needed)

## Forbidden Changes

- Do not modify `docs/safety-boundaries.md` unless fixing clarity
- Do not reintroduce game-specific wording
- Do not remove tests
- Do not modify `src/` code
- Do not create the GitHub Release (tag only after explicit user approval)

## Next Round Prompt (after Day 3 completion)

```
/goal complete v0.1.1 maintenance polish for Vision FSM Agent: improve
custom FSM examples, add expected output docs, add or update smoke tests,
update CHANGELOG and PROGRESS, run pytest and oss_readiness_check, ensure
no risky wording regression, commit and push.
```
