# PROGRESS

> Reverse-chronological order (newest first). Each entry is one work round.

---

## P001 — 2026-06-30 10:30

### Completed

- Created 7 maintenance ledger files in `docs/agent_ledger/`:
  `SESSION_START.md`, `NEXT.md`, `PROGRESS.md`, `DECISIONS.md`,
  `ERRORS.md`, `RELEASE_PLAN.md`, `CODEX_OSS_APPLICATION.md`.
- Rewrote `docs/agent_ledger/README.md` from incorrect "runtime audit
  log" placeholder to maintenance ledger directory guide.
- Enhanced `scripts/oss_readiness_check.py` with:
  - High-risk wording scan (Chinese zero-tolerance + English
    negative-context exemption)
  - `--run-tests` option to run pytest after readiness check
  - Enhanced output (file check, risky wording, tests, recommended
    actions)
  - 7 new ledger files added to required-files list
- Updated `.gitignore` to exclude `.coverage`.
- Updated `CHANGELOG.md` `[Unreleased]` with all changes.
- Recorded D001–D006 in `DECISIONS.md`.
- Recorded E001–E002 and R001–R002 in `ERRORS.md`.

### Files Changed

- `docs/agent_ledger/README.md` (rewritten)
- `docs/agent_ledger/SESSION_START.md` (new)
- `docs/agent_ledger/NEXT.md` (new)
- `docs/agent_ledger/PROGRESS.md` (new)
- `docs/agent_ledger/DECISIONS.md` (new)
- `docs/agent_ledger/ERRORS.md` (new)
- `docs/agent_ledger/RELEASE_PLAN.md` (new)
- `docs/agent_ledger/CODEX_OSS_APPLICATION.md` (new)
- `scripts/oss_readiness_check.py` (enhanced)
- `.gitignore` (added .coverage)
- `CHANGELOG.md` (updated [Unreleased])

### Validation

- pytest: **pass** (50 tests)
- oss_readiness_check: **pass**
- oss_readiness_check --run-tests: **pass**
- risky wording scan: **pass** (Chinese: 0 hits; English: all exempted)
- git status: **dirty** (all changes uncommitted, per "no push" constraint)

### Notes

- All changes are uncommitted. The user must explicitly approve commit
  and push.
- The oss_readiness_check English word scan uses negative-context
  exemption so that safety-boundary documentation (which legitimately
  mentions "cheating", "botting", etc. in a prohibitive context) does
  not trigger false positives.
- `src/fsm.py` line 188 uses "bypasses" in a technical sense
  ("bypasses on_exit callbacks"); the scan uses the precise phrase
  "bypass detection" instead of the bare word "bypass" to avoid this
  false positive.

### Next

Day 1: Improve README Quick Demo visibility and add `docs/demo.md`.
