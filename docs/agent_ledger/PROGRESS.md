# PROGRESS

> Reverse-chronological order (newest first). Each entry is one work round.

---

## P003 — 2026-06-30 12:30

### Completed

Fixed all 15 engineering gaps identified in the project assessment:

**New files (21)**:
- `src/py.typed` (PEP 561 marker)
- `CITATION.cff` (academic citation)
- `.pre-commit-config.yaml` (ruff + mypy + standard hooks)
- `Makefile` (install/test/demo/lint/check/clean targets)
- `.github/dependabot.yml` (pip + github-actions updates)
- `.github/workflows/lint.yml` (ruff + mypy + bandit CI)
- `.github/FUNDING.yml` (sponsorship placeholder)
- `docs/releases/v0.1.0.md` (formal release notes)
- `docs/troubleshooting.md` (OpenCV/Windows/pytest/HIL troubleshooting)
- `docs/api/README.md` + `fsm.md` + `vision.md` + `agent.md` + `hil.md`
- `mkdocs.yml` (MkDocs Material site config)
- `.readthedocs.yaml` (ReadTheDocs config)
- `.devcontainer/devcontainer.json` (VS Code / Codespaces)
- `tests/test_agent.py` (15 dedicated agent tests)

**Modified files (4)**:
- `pyproject.toml` — added [project.scripts], [tool.ruff], [tool.mypy],
  [tool.bandit], expanded dev extras
- `CHANGELOG.md` — added link definitions + [Unreleased] entries
- `tests/test_config.py` — moved agent tests out, added config tests
- `scripts/oss_readiness_check.py` — added 19 new files to required list,
  added allow_empty flag for py.typed

### Validation

- pytest: **pass** (61 tests — up from 50, thanks to test_agent.py)
- oss_readiness_check: **pass** (66 files OK, 0 missing, 0 empty)
- risky wording scan: **pass** (0 Chinese, 0 English real, 59 exempted)
- git status: dirty (all changes uncommitted)

### Notes

- py.typed is an empty file by design (PEP 561 marker); oss_readiness_check
  now supports an `allow_empty` flag for such cases.
- ruff/mypy/bandit configs are created but tools not installed locally;
  they will run in CI (lint.yml) and via pre-commit.
- mkdocs.yml and .readthedocs.yaml configure the doc site but it is not
  yet built/deployed.

### Next

Day 2: Contributor experience (CONTRIBUTING polish + PR template verify).

---

## P002 — 2026-06-30 11:00

### Completed

- Added **Quick Demo** section to README (section 4), with 30-second
  copy-paste commands and expected output. Renumbered subsequent sections
  (5–13).
- Created **docs/demo.md** — detailed demo walkthrough covering overview,
  prerequisites, running options, expected output, step-by-step
  explanation, configuration, saving frames, and troubleshooting.
- Updated CHANGELOG `[Unreleased]` with Quick Demo and docs/demo.md.
- Committed all prior work in 2 commits on branch
  `refactor/vision-fsm-agent`:
  - `a3dd112` refactor: rebrand to Vision FSM Agent
  - `7648a13` docs: add maintenance ledger and enhance oss readiness check

### Files Changed

- `README.md` (added Quick Demo section, renumbered sections 5–13)
- `docs/demo.md` (new)
- `CHANGELOG.md` (updated [Unreleased])
- `docs/agent_ledger/PROGRESS.md` (this entry)
- `docs/agent_ledger/NEXT.md` (updated to Day 2)

### Validation

- pytest: **pass** (50 tests)
- oss_readiness_check: **pass**
- demo smoke test: **pass** (agent completes objectives)
- risky wording scan: **pass**
- git status: dirty (Day 1 changes uncommitted)

### Notes

- README now has 13 sections (was 12). Quick Demo is section 4, before
  Quick Start (now section 5). This gives first-time visitors an
  immediate "30 seconds to see it work" experience.
- docs/demo.md includes a troubleshooting section that links forward to
  the planned `docs/troubleshooting.md` (Day 2).

### Next

Day 2: Contributor experience and troubleshooting documentation.

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
