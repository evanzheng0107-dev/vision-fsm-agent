# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`[project.scripts]` entry point** in pyproject.toml (`vision-fsm-agent`).
- **`src/py.typed`** - PEP 561 typed-package marker.
- **CITATION.cff** - Citation File Format for academic use.
- **.pre-commit-config.yaml** - Pre-commit hooks (ruff, mypy, standard hooks).
- **Makefile** - Convenience commands (install, test, demo, lint, check, clean).
- **.github/dependabot.yml** - Dependency update automation (pip + github-actions).
- **.github/workflows/lint.yml** - CI lint workflow (ruff + mypy + bandit).
- **.github/FUNDING.yml** - Sponsorship configuration (placeholder).
- **docs/releases/v0.1.0.md** - Formal v0.1.0 release notes.
- **docs/troubleshooting.md** - Troubleshooting guide (OpenCV, Windows, pytest, HIL).
- **docs/api/** - API reference (README + fsm + vision + agent + hil).
- **mkdocs.yml** - MkDocs Material documentation site configuration.
- **.readthedocs.yaml** - ReadTheDocs configuration.
- **.devcontainer/devcontainer.json** - Dev container for VS Code / Codespaces.
- **tests/test_agent.py** - Dedicated agent tests (15 tests, split from test_config.py
  plus new edge-case coverage).
- **Code quality tool config** in pyproject.toml: `[tool.ruff]`, `[tool.mypy]`,
  `[tool.bandit]` with dev extras (ruff, mypy, bandit, pre-commit).

### Changed
- **pyproject.toml** - Added `[project.scripts]`, ruff/mypy/bandit config, expanded
  dev extras.
- **CHANGELOG.md** - Added link definitions at file end (`[Unreleased]:`, `[0.1.0]:`).
- **tests/test_config.py** - Moved agent tests to test_agent.py; added config tests.
- **scripts/oss_readiness_check.py** - Added 19 new files to required list; added
  `allow_empty` flag for py.typed.

### Added (continued — Day 1)
- **README Quick Demo section** - A 30-second "see it in action" section
  with copy-paste commands and expected output, placed before Quick Start.
- **docs/demo.md** - Detailed demo walkthrough: overview, prerequisites,
  running options, expected output, step-by-step explanation, configuration,
  saving frames, and troubleshooting tips.
- **CODE_OF_CONDUCT.md** - Contributor Covenant 2.1 Code of Conduct.
- **pyproject.toml** - PEP 621 project metadata, packaging config, pytest and
  coverage tool configuration. Enables pip install and PyPI publishing.
- **.editorconfig** - Editor configuration for consistent cross-IDE style.
- **.github/CODEOWNERS** - Code ownership rules for automatic PR review routing.
- **.github/ISSUE_TEMPLATE/feature_request.yml** - Feature request issue template.
- **.github/ISSUE_TEMPLATE/config.yml** - Issue template chooser (disables blank issues).
- **Maintenance ledger** (`docs/agent_ledger/`) - 7 tracking files for
  cross-session context continuity: SESSION_START, NEXT, PROGRESS,
  DECISIONS (D001–D006), ERRORS (E001–E002, R001–R002), RELEASE_PLAN,
  CODEX_OSS_APPLICATION. README rewritten as directory guide.
- **scripts/oss_readiness_check.py** - Enhanced with high-risk wording
  scan (Chinese zero-tolerance + English negative-context exemption),
  `--run-tests` option, and structured output (file check, risky words,
  tests, recommended actions).
- **pytest-cov** dependency and --cov step in CI for coverage reporting.

### Changed
- **SECURITY.md** - Replaced placeholder email with GitHub private vulnerability
  reporting guidance.
- **CONTRIBUTING.md** - Updated Code of Conduct section to link to the new
  standalone CODE_OF_CONDUCT.md.
- **src/agent.py** - Removed vendor-specific DASHSCOPE_API_KEY fallback and
  DashScope/qwen default values; now uses neutral OpenAI-compatible defaults.
- **src/main.py** - Fixed stale pygame reference in a comment (now opencv/numpy).
- **.env.example** - Updated LLM example to use neutral OpenAI-compatible defaults.
- **.github/workflows/test.yml** - Added pytest-cov and --cov coverage reporting.
- **requirements.txt** - Added pytest-cov>=4.0.
- **.gitignore** - Added `.coverage` and `htmlcov/` to prevent committing
  coverage artifacts.
- **docs/agent_ledger/README.md** - Rewritten from incorrect "runtime audit
  log" placeholder to maintenance ledger directory guide.

### Planned
- Additional demo scenarios (multi-agent, dynamic obstacles)
- Configurable FSM topologies via YAML
- Vision pipeline extensions (edge detection, feature matching)

## [0.1.0] - 2026-06-29

### Added
- **Core framework** with four independent modules:
  - `src/fsm.py` — generic finite-state-machine engine with guards,
    actions, on_enter/on_exit callbacks, and transition history.
  - `src/vision.py` — multi-scale OpenCV template-matching engine with
    a `TemplateManager` for multi-template management.
  - `src/agent.py` — decision agents: local rule-based
    (`LocalDecisionAgent`) and optional LLM-backed
    (`CloudDecisionAgent`) with graceful fallback.
  - `src/hil_client.py` / `src/hil_server.py` — Human-in-the-Loop
    correction system over HTTP (Flask).
- **Synthetic demo environment** (`demo_app/visual_grid_world.py`) — a
  reproducible grid world rendered with OpenCV/numpy. Runs the full
  agent loop (vision → FSM → decision → action) with zero external
  dependencies and no screen capture.
- **Generic agent main loop** (`src/main.py`) — environment-agnostic
  loop with optional HIL integration and failure-retry logic.
- **Programmatically generated demo assets** — all template images are
  drawn in code (`scripts/generate_demo_assets.py`); no third-party
  imagery.
- **Pytest test suite** (50 tests) covering FSM, vision, HIL, config,
  agent decisions, and end-to-end demo execution.
- **GitHub Actions CI** (`.github/workflows/test.yml`) running the test
  suite on push and pull request.
- **Documentation**: architecture overview, HIL workflow, and safety
  boundaries.
- **Open-source governance**: MIT license, contributing guide, security
  policy, issue/PR templates, and AGENTS.md.

### Safety
- The default environment is a **local synthetic demo**. No screen
  capture, no network calls (except optional local HIL), no input to
  external software.
- The optional `live` mode is clearly marked as advanced and requires
  explicit configuration; `pyautogui.FAILSAFE` stays enabled.
- All documentation explicitly states the project is **not** for
  cheating, botting, or bypassing platform rules.

### Changed
- Project renamed and repositioned from a game-specific automation
  script to a **generic, educational CV+FSM+HIL framework**.
- Removed all references to specific commercial games, emulators, and
  anti-detection features.
- Removed all real game screenshots and templates; replaced with
  programmatically generated synthetic assets.

### Removed
- Game-specific window management code (kept as optional `LiveEnvironment`).
- Anti-detection / human-mimicry features (random jitter, timing
  randomisation designed to evade detection).
- Cloud API keys and provider-specific configuration from the codebase.
- References to specific games and emulators throughout.

---

[Unreleased]: https://github.com/evanzheng0107-dev/sword-legend-explorer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/evanzheng0107-dev/sword-legend-explorer/releases/tag/v0.1.0
