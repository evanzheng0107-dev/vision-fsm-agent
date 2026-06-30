# RELEASE_PLAN

> Version plan for Vision FSM Agent. Updated when release scope changes.
> **No release without explicit user approval.**

---

## v0.1.0 — Initial public release

**Status**: Code complete, uncommitted. Awaiting user approval to commit
and tag.

### Required (all met)

- [x] README complete (12 sections)
- [x] LICENSE present (MIT)
- [x] SECURITY present
- [x] CONTRIBUTING present
- [x] CODE_OF_CONDUCT present
- [x] AGENTS present
- [x] CHANGELOG updated
- [x] demo_app runs (`python demo_app/visual_grid_world.py --steps 20`)
- [x] pytest passes (50 tests)
- [x] GitHub Actions configured
- [x] Safety boundaries documented
- [x] Issue templates (bug report + feature request)
- [x] PR template with safety checklist
- [x] CODEOWNERS
- [x] pyproject.toml (packaging metadata)
- [x] .editorconfig

### Release Notes Draft

#### Highlights

- Rebranded as Vision FSM Agent
- Added reproducible synthetic visual grid world demo
- Added FSM, Vision, Decision, HIL, Action architecture
- Added safety boundaries
- Added MIT License, CI, tests, issue templates, and PR template

#### Safety

- Intended for local, controlled demo environments, research, and
  education
- Not intended for cheating, botting, bypassing platform rules, or
  automating third-party systems without permission

#### Verification

- Demo completes synthetic objectives (collects items, presses buttons)
- pytest passes (50 tests)
- Risky wording scan passes

---

## v0.1.1 — Maintenance ledger and OSS readiness

**Status**: In progress.

### Scope

- [x] Maintenance ledger (`docs/agent_ledger/` 7 files)
- [x] OSS readiness check with risky word scan
- [x] `.gitignore` updated (`.coverage`)
- [x] CHANGELOG updated
- [ ] README Quick Demo improvement (Day 1)
- [ ] `docs/demo.md` (Day 1)
- [ ] Troubleshooting docs (Day 2)
- [ ] Example improvements (Day 4)

### Not in scope

- New features
- CI integration of oss_readiness_check (defer to v0.2.0)
- Runtime agent-decision audit log (v0.2.0)

---

## v0.2.0 — Planned

### Candidate items

- Configurable FSM topologies via YAML
- Vision pipeline extensions (edge detection, feature matching)
- Runtime agent-decision audit log (JSON-lines, separate from
  maintenance ledger)
- HIL web dashboard
- Performance benchmarking harness
- Educational lab exercises
- CI integration of `oss_readiness_check.py`

---

## Release Constraints

1. No push or release without explicit user approval.
2. All tests must pass before tagging.
3. `oss_readiness_check.py` must pass.
4. CHANGELOG must be updated.
5. Release notes must be prepared in `docs/releases/`.
