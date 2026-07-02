# NEXT

## Current Date

2026-07-02

## Current Stage

Day 3 complete. Awaiting user to create PR and merge.

## Current Task

User actions required (cannot be automated — no GitHub credentials in
sandbox):

1. **Create PR** on GitHub:
   https://github.com/evanzheng0107-dev/sword-legend-explorer/pull/new/refactor/vision-fsm-agent

   PR title: `refactor: rebrand to Vision FSM Agent with standard package layout`

   PR body: Copy from `docs/releases/v0.1.0.md` Highlights section +
   note "8 commits, 61 tests, oss_readiness_check passes".

2. **Merge PR** to `master`.

3. **Tag v0.1.0**:
   ```bash
   git checkout master
   git tag v0.1.0
   git push origin v0.1.0
   ```

4. **Create GitHub Release** using notes from `docs/releases/v0.1.0.md`.

## After User Actions

Day 4: v0.1.1 maintenance polish
- Improve custom FSM example with expected output
- Add/update smoke tests
- Update CHANGELOG and PROGRESS

## Day 4 Resume Command

```
开始 Day 4
```

## Forbidden Changes (always)

- Do not reintroduce game-specific wording
- Do not modify safety boundaries
- Do not push without explicit user approval
- Do not create GitHub Release without explicit user approval
