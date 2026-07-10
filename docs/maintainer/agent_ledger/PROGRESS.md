# PROGRESS

> Reverse-chronological order (newest first). Each entry is one work round.

---

## P010 — 2026-07-10 12:00

### Completed

Day 7: Examples and test stability improvements.

- **Improved `tests/smoke/test_demo_run.py`**: Enhanced assertions to check
  for all expected output markers (header, step format, progress indicators,
  final status fields). Previously only checked return code and basic
  output presence.
- **Added `tests/smoke/test_examples_independent.py`** (3 new tests):
  - `test_demo_runs_from_examples_dir` — verifies grid world demo runs
    when invoked directly from `examples/visual_grid_world/`
  - `test_custom_fsm_runs_from_examples_dir` — verifies custom FSM runs
    from its own directory
  - `test_demo_runs_via_arg_longer` — verifies 35-step demo completes
    all objectives (`All items collected and buttons pressed. Done!`)
- **Rewrote `examples/README.md`**: Added quick-nav table, prerequisites,
  FSM topology diagram, "Verifying the examples" section with smoke test
  instructions, and links to roadmap/issues.
- **Updated README.md**: Test count 63 → 66.
- **Updated CHANGELOG.md**: Added Day 7 entries.

### Validation

- pytest: **pass** (66 tests, +3 new smoke tests)
- ruff check: **pass**
- oss_readiness_check: **pass** (78 files, 0 risky)
- git status: clean

### Next

Day 8: address open issues or continue with v0.2.0 feature planning.

### Completed

Repository rename and URL update.

- **Merged PR #13**: Audit fixes (`.ruff_cache` gitignore, stale path).
- **Repository URLs updated**: All references from `sword-legend-explorer`
  to `vision-fsm-agent` in README, CHANGELOG, pyproject.toml, CITATION.cff,
  mkdocs.yml, CONTRIBUTING, docs, and config files (32 references).
- **CHANGELOG.md** updated with rename entry in `[Unreleased]`.
- **PR #14** created and merged for URL updates.

### Validation

- pytest: **pass** (63 tests)
- ruff check: **pass**
- oss_readiness_check: **pass** (77 files, 0 risky)
- git status: clean

### Note

GitHub repo rename (`sword-legend-explorer` -> `vision-fsm-agent`) requires
manual action (PAT lacks admin scope). After rename, local remote URL
should be updated to the new repo URL.

### Next

Phase 5-9: Create issues, verify releases, finalize application materials.

---

## P008 — 2026-07-02 22:55

### Completed

Day 5: Documentation and roadmap finalization.

- **Updated project documentation**: Rewrote to final version with all
  current information (63 tests, 77 files, v0.1.0 + v0.1.1 released,
  5 PRs merged, issues created). Added maintenance timeline table.
- **Created 6 GitHub issues** (#5–#10) via GitHub API:
  - #5: Configurable FSM topologies via YAML (roadmap)
  - #6: Vision pipeline extensions (roadmap)
  - #7: Additional demo scenarios (roadmap)
  - #8: API reference examples with expected output (docs, good first issue)
  - #9: Property-based tests for FSM (testing)
  - #10: HIL correction persistence (research)
- **Updated README roadmap**: v0.1.0 → v0.1.x (current), added issue
  links to v0.2.0 planned items, added v0.1.1 achievements.
- **Final validation**: ruff PASS, pytest 63 passed, oss_readiness_check
  PASS (77 files, 0 risky words).

### Validation

- pytest: **pass** (63 tests)
- ruff check: **pass**
- oss_readiness_check: **pass** (77 files, 0 risky)
- git status: clean

### Next

Project documentation is complete. Next focus: v0.2.0 development.

---

## P007 — 2026-07-02 11:45

### Completed

Day 4: v0.1.1 maintenance polish.

- **Improved `examples/custom_fsm/custom_fsm.py`**: rewrote to show
  intermediate FSM states (PATROL→SCAN→PATROL per step, previously only
  the final state was printed). Added a simulated sensor-outage phase
  (steps 6–7) to demonstrate the STUCK→WAIT→READY fallback path, which
  previously never triggered. Added docstring with expected output.
- **Updated `examples/README.md`**: fixed stale path
  (`examples/custom_fsm.py` → `examples/custom_fsm/custom_fsm.py`),
  added expected-output block and key takeaways for the custom FSM
  example, added visual_grid_world cross-reference.
- **Added `tests/smoke/test_custom_fsm.py`**: smoke test verifying the
  custom FSM example runs end-to-end and exercises both the normal
  SPOTTED→SCAN→DONE path and the STUCK→WAIT→READY fallback path.
  Checks for key output markers (Initial state, Transition history,
  STUCK, WAIT, READY, SPOTTED, SCAN, DONE).
- **Updated `CHANGELOG.md`**: added `[0.1.1]` section.
- **Updated `docs/maintainer/agent_ledger/NEXT.md`**: Day 4 done,
  points to Day 5.

### Validation

- pytest: **pass** (63 tests, +1 new smoke test)
- smoke tests: **pass** (demo + custom_fsm)
- custom_fsm example: runs correctly, 16 transitions, WAIT path fires

### Next

Day 5: Documentation and roadmap finalization.

---

## P006 — 2026-07-02 09:50

### Completed

Day 3 (final): v0.1.0 release material verification and path sync.

- Verified all release materials reference correct paths after the
  project reorganization (commit 8c87554 + 009efb3).
- Fixed stale paths in `docs/releases/v0.1.0.md`,
  `docs/maintainer/RELEASE_PLAN.md`, and
  `docs/maintainer/PROJECT_SUMMARY.md`.
- All 8 commits are pushed to `origin/refactor/vision-fsm-agent`.
- PR-ready: branch is clean, tests pass, oss_readiness_check passes.

### Validation

- pytest: **pass** (61 tests)
- oss_readiness_check: **pass** (76 files OK, 0 missing, 0 risky)
- demo smoke: **pass**
- risky wording scan: **pass**
- git status: clean

### Next

User to create PR on GitHub, merge to master, tag v0.1.0, create release.
Then Day 4: v0.1.1 maintenance polish.

---

## P005 — 2026-07-01 11:06

### Completed

Day 3 (partial): v0.1.0 release material preparation.

- **docs/releases/v0.1.0.md** — Updated to reflect current state:
  61 tests (was 50), expanded governance list, updated file counts,
  added known limitations (import style, coverage target).
- **CHANGELOG.md** — Fixed `[0.1.0]` test count (50 → 61).
- **RELEASE_PLAN.md** — Updated v0.1.0 status to "committed and pushed",
  marked all 24 required items as met, added remaining steps (PR merge,
  tag, release). Updated v0.1.1 scope with completed Day 1–2 items +
  15 engineering gap fixes. Added v0.2.0 candidate items.
- **PROJECT_SUMMARY.md** — Updated with push evidence, expanded
  project status overview (17 items), updated statement.

### Files Changed

- `docs/releases/v0.1.0.md` (updated)
- `CHANGELOG.md` (fixed test count in [0.1.0])
- `docs/agent_ledger/RELEASE_PLAN.md` (rewritten)
- `docs/agent_ledger/PROJECT_SUMMARY.md` (rewritten)
- `docs/agent_ledger/PROGRESS.md` (this entry)
- `docs/agent_ledger/NEXT.md` (updated — paused, awaiting user)

### Validation

- pytest: not re-run (no code changes, docs only)
- oss_readiness_check: not re-run (no new files)
- git status: dirty (Day 3 changes, awaiting commit)

### Notes

- **Day 3 paused** per user instruction. Development will resume when the
  user manually issues the next day's command.
- All prior commits (5) have been successfully pushed to
  `origin/refactor/vision-fsm-agent` by the user.
- PR link available: https://github.com/evanzheng0107-dev/vision-fsm-agent/pull/new/refactor/vision-fsm-agent

### Next

**Paused.** Awaiting user instruction to start Day 3 completion or Day 4.

---

## P004 — 2026-07-01 10:30

### Completed

Day 2: Contributor experience and troubleshooting documentation.

- **CONTRIBUTING.md** — Expanded with:
  - Development Setup (Makefile quick setup + manual venv + dev container)
  - Pre-commit Hooks installation and usage
  - Makefile Commands Reference table (11 commands)
  - Development Workflow with conventional commit format
  - Adding New Features guide (FSM states, vision templates, decision logic)
  - Updated Project Structure with docs/api/ and docs/releases/
- **README** — Added Development Setup section (section 10) with:
  - `make install` / `make assets` / `make test` quick setup
  - Manual venv + `pip install -e ".[dev]"` setup
  - Pre-commit hooks installation
  - Dev Container reference
  - Useful commands table
  - Link to CONTRIBUTING.md
  - Renumbered sections 11–14 (was 10–13)
- **PR template** — Verified safety checklist (5 safety + 3 testing + 3 docs
  items). No changes needed.
- **docs/troubleshooting.md** — Already created in P003, verified content
  covers OpenCV, Windows, pytest, HIL, and performance issues.

### Files Changed

- `CONTRIBUTING.md` (expanded, ~107 → ~200 lines)
- `README.md` (added section 10, renumbered 11-14)
- `CHANGELOG.md` (updated [Unreleased])
- `docs/agent_ledger/PROGRESS.md` (this entry)
- `docs/agent_ledger/NEXT.md` (updated to Day 3)

### Validation

- pytest: **pass** (61 tests)
- oss_readiness_check: **pass**
- risky wording scan: **pass**
- git status: dirty (Day 2 changes, awaiting commit + push)

### Notes

- Attempted to push prior commits (a3dd112–b415c91) but encountered
  SSL/TLS handshake failure (`schannel: failed to receive handshake`).
  Will retry push after Day 2 commit.
- README now has 14 sections (was 13). Development Setup is section 10,
  before Testing (now 11).

### Next

Day 3: Prepare v0.1.0 release materials.

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
  `ERRORS.md`, `RELEASE_PLAN.md`, `PROJECT_SUMMARY.md`.
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
- `docs/agent_ledger/PROJECT_SUMMARY.md` (new)
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
