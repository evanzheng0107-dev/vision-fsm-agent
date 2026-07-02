# Agent Ledger — Maintenance Tracking

This directory is the **maintenance ledger** for the Vision FSM Agent
project. It provides cross-session context continuity for AI-assisted
development and human maintainers.

> **Not** a runtime agent decision log. The runtime audit-log feature is
> a separate v0.2.0 plan (see the project [Roadmap](../../README.md#11-roadmap)).

## Files

| File | When to read | When to write | Purpose |
|------|-------------|---------------|---------|
| `SESSION_START.md` | Every session start | When goals/constraints change | Project identity, current goal, safety rules, done criteria |
| `NEXT.md` | Every session start, after SESSION_START | At the end of each work round | The single next task to execute |
| `PROGRESS.md` | When reviewing history | At the end of each work round | What was completed, files changed, validation results |
| `DECISIONS.md` | When context is needed on *why* | When a significant decision is made | Key product/technical/safety decisions with rationale |
| `ERRORS.md` | When diagnosing a recurring issue | When an error/regression is found and fixed | Symptoms, detection, fix, regression test |
| `RELEASE_PLAN.md` | When planning a release | When release scope changes | Version plan, required items, release notes drafts |
| `CODEX_OSS_APPLICATION.md` | When preparing the application | Continuously, as evidence accumulates | Codex for Open Source application draft |

## Usage Convention

1. **Start of session**: Read `SESSION_START.md` → `NEXT.md` → `DECISIONS.md`.
2. **End of round**: Update `PROGRESS.md` (append new entry) → Update `NEXT.md` (set next task) → Run validation.
3. **Key decision made**: Add entry to `DECISIONS.md`.
4. **Error found/fixed**: Add entry to `ERRORS.md`.
5. **Release planning**: Update `RELEASE_PLAN.md`.

Entries are appended in reverse-chronological order (newest first) in
`PROGRESS.md` and `ERRORS.md`. `DECISIONS.md` uses sequential numbering
(D001, D002, …).
