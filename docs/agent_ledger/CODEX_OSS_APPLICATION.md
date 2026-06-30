# Codex for Open Source Application Draft

> Working draft. Not yet submitted. Updated as evidence accumulates.

---

## Repository

**Vision FSM Agent**

A lightweight Python framework for building computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction.

## Maintainer Role

I am the primary maintainer of Vision FSM Agent. I define the project
direction, maintain the roadmap, review changes, manage releases, update
documentation, maintain tests, and enforce safety boundaries.

## Repository Qualification

Vision FSM Agent is a public Python framework for computer-vision-driven
automation agents with finite-state-machine control and human-in-the-loop
correction. It provides a reproducible synthetic demo, tests, CI, safety
boundaries, and documentation for researchers and developers exploring
visual agents in controlled local environments.

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
| Public repo | Pending | Repo to be renamed to `vision-fsm-agent` and confirmed public |
| License | ✅ | MIT (`LICENSE`) |
| CI | ✅ | `.github/workflows/test.yml` (Ubuntu + Windows, Python 3.9–3.13) |
| Tests | ✅ | 50 pytest tests, all passing |
| Release | Pending | v0.1.0 code complete, awaiting commit + tag |
| Issues | Pending | 5–8 issues to be created (drafts in NEXT.md) |
| PRs | Pending | 2–3 PR-ready commits planned |
| Docs | ✅ | README (12 sections), architecture, HIL workflow, safety boundaries |
| Safety boundaries | ✅ | `docs/safety-boundaries.md`, `SECURITY.md`, `AGENTS.md` |
| AGENTS.md | ✅ | Present with safety rules and contribution policy |
| Changelog | ✅ | `CHANGELOG.md` (Keep a Changelog format) |
| Maintenance evidence | In progress | `docs/agent_ledger/` with 7 tracking files |
| OSS readiness check | ✅ | `scripts/oss_readiness_check.py` with risky word scan |

## Application Short Statement (≤500 characters)

Vision FSM Agent is a public Python framework for CV-driven automation
with FSM control and human-in-the-loop correction. It features a
reproducible synthetic demo, 50 tests, CI, safety boundaries, and
complete OSS governance. I will use API credits for documentation, test
generation, issue triage, release notes, and human-reviewed LLM-assisted
development.

## Remaining Steps

1. Commit all changes (awaiting user approval)
2. Rename repo to `vision-fsm-agent` on GitHub
3. Push and tag `v0.1.0`
4. Create 5–8 GitHub issues
5. Complete Day 1–5 maintenance tasks
6. Create `v0.1.1` tag after Day 4
7. Finalize `docs/codex-for-oss-application.md`
8. Submit application after 3–5 days of visible maintenance
