# RELEASE_PLAN

> Version plan for Vision FSM Agent. Updated when release scope changes.
> **No release without explicit user approval.**

---

## v0.1.0 — Initial public release

**Status**: Code complete, committed, and pushed to
`refactor/vision-fsm-agent` branch. Awaiting PR merge to `master` and
tag creation.

### Required (all met)

- [x] README complete (14 sections)
- [x] LICENSE present (MIT)
- [x] SECURITY present
- [x] CONTRIBUTING present (expanded with Development Setup)
- [x] CODE_OF_CONDUCT present
- [x] AGENTS present
- [x] CHANGELOG updated (with link definitions)
- [x] demo_app runs (`python demo_app/visual_grid_world.py --steps 20`)
- [x] pytest passes (61 tests)
- [x] GitHub Actions configured (test + lint workflows)
- [x] Safety boundaries documented
- [x] Issue templates (bug report + feature request)
- [x] PR template with safety checklist
- [x] CODEOWNERS
- [x] pyproject.toml (packaging metadata + scripts + tool config)
- [x] .editorconfig
- [x] CITATION.cff
- [x] py.typed (PEP 561)
- [x] Makefile
- [x] .pre-commit-config.yaml
- [x] .github/dependabot.yml
- [x] docs/releases/v0.1.0.md
- [x] docs/troubleshooting.md
- [x] docs/api/ (5 API reference files)
- [x] mkdocs.yml + .readthedocs.yaml
- [x] .devcontainer/
- [x] oss_readiness_check.py passes

### Release Notes

See [`docs/releases/v0.1.0.md`](../releases/v0.1.0.md).

### Remaining Steps

1. Merge `refactor/vision-fsm-agent` → `master` (via PR)
2. Tag `v0.1.0` on `master`
3. Create GitHub Release with release notes from `docs/releases/v0.1.0.md`
4. All steps require explicit user approval

---

## v0.1.1 — Maintenance polish

**Status**: In progress (Day 1–2 complete, Day 4 pending).

### Scope

- [x] Maintenance ledger (`docs/agent_ledger/` 7 files)
- [x] OSS readiness check with risky word scan
- [x] `.gitignore` updated (`.coverage`)
- [x] CHANGELOG updated
- [x] README Quick Demo improvement (Day 1)
- [x] `docs/demo.md` (Day 1)
- [x] Troubleshooting docs (Day 2)
- [x] CONTRIBUTING expansion (Day 2)
- [x] README Development Setup (Day 2)
- [x] 15 engineering gap fixes (py.typed, CITATION, pre-commit, Makefile,
      dependabot, lint CI, FUNDING, releases, CHANGELOG links, API docs,
      mkdocs, ReadTheDocs, devcontainer, test_agent.py, tool config)
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
- Relative imports (remove sys.path hack)
- Split `src/main.py` into environment.py + config.py + loop.py
- Coverage target 80%+

---

## Release Constraints

1. No push or release without explicit user approval.
2. All tests must pass before tagging.
3. `oss_readiness_check.py` must pass.
4. CHANGELOG must be updated.
5. Release notes must be prepared in `docs/releases/`.
