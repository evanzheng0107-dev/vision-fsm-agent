# DECISIONS

> Key product, technical, and safety decisions. Sequential numbering
> (D001, D002, …). Each entry: date, decision, rationale, status.

---

## D001 — Project positioning

**Date**: 2026-06-29
**Status**: Confirmed

Vision FSM Agent is a general-purpose CV + FSM + HIL framework for local
controlled demos, research, and education. It is not a game bot, cheating
tool, anti-detection tool, or third-party platform automation tool.

**Rationale**: The project was refactored from a game-specific prototype.
The new positioning ensures it is safe for public release and eligible
for open-source program applications.

---

## D002 — Safety boundary

**Date**: 2026-06-29
**Status**: Confirmed

The default environment must remain synthetic, local, and reproducible.
Third-party game assets, screenshots, platform bypass logic, and
anti-detection wording are not allowed.

**Rationale**: Safety boundaries are the core differentiator from the
original project. They protect users and maintainers from misuse
liability.

---

## D003 — Maintenance strategy

**Date**: 2026-06-29
**Status**: Confirmed

The repository should be maintained through small, reviewable increments:
issues, PR-ready commits, tests, documentation updates, changelog
updates, and releases.

**Rationale**: Small increments are easier to review, test, and roll
back. They also produce visible maintenance activity for open-source
program applications.

---

## D004 — Codex for Open Source application strategy

**Date**: 2026-06-29
**Status**: Confirmed

The application should emphasize active open-source maintenance,
maintainer responsibilities, safety boundaries, documentation, tests,
release workflows, and optional LLM-assisted development. It should not
claim broad adoption unless there is evidence.

**Rationale**: Honesty in the application builds trust. The project's
strength is its safety design and educational value, not market
adoption.

---

## D005 — Maintenance ledger structure

**Date**: 2026-06-30
**Status**: Confirmed

The maintenance ledger uses `docs/agent_ledger/` with 7 files
(SESSION_START, NEXT, PROGRESS, DECISIONS, ERRORS, RELEASE_PLAN,
CODEX_OSS_APPLICATION). This is separate from the planned runtime
agent-decision audit log (v0.2.0).

**Rationale**: AI-assisted development across multiple sessions needs
persistent context. The 7-file structure provides clear entry points
and update protocols.

---

## D006 — Risky wording scan strategy

**Date**: 2026-06-30
**Status**: Confirmed

The oss_readiness_check high-risk word scan uses:
- **Chinese words**: zero-tolerance (any hit = FAIL)
- **English words**: negative-context exemption (hits in lines with
  "not", "never", "prohibited", etc. are exempted as legitimate safety
  statements)
- **"bypass"**: scanned as the precise phrase "bypass detection" rather
  than the bare word, to avoid false positives on the technical usage
  "bypasses on_exit callbacks" in `src/fsm.py`

**Rationale**: Safety-boundary documentation legitimately mentions
prohibited concepts ("not intended for cheating"). A naive scan would
flag these as violations. The exemption strategy balances regression
detection with documentation needs.

---

## D007 — Codex application finalized

**Date**: 2026-07-02
**Status**: Confirmed

The Codex for Open Source application package is finalized. All evidence
checklist items are ✅. The project has:
- 2 releases (v0.1.0, v0.1.1) with GitHub Releases
- 4 merged PRs (refactor, 2 dependabot, v0.1.1 polish)
- 6 open issues (#5–#10) for roadmap and maintenance
- 63 tests, CI (test + lint), oss_readiness_check PASS
- Complete OSS governance and documentation

**Rationale**: The application requires visible maintenance activity
over multiple days. Days 1–5 provide a clear maintenance trajectory
from initial refactoring through release management to application
finalization.
