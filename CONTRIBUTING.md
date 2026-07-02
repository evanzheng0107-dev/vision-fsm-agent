# Contributing to Vision FSM Agent

Thank you for your interest in contributing! This project welcomes
contributions that align with its mission: a **safe, educational, and
reproducible** framework for computer-vision-driven automation with
finite-state-machine control.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report
unacceptable behavior to the maintainers via GitHub's private channels.

## Scope and Safety First

Before contributing, please read [`docs/safety-boundaries.md`](docs/safety-boundaries.md).
**Contributions that add capabilities for cheating, botting, bypassing
platform rules, or automating third-party services without permission will
be rejected.** This includes (but is not limited to):

- Anti-detection, evasion, or human-mimicry features
- Code that targets specific commercial games or services
- Automation intended to violate terms of service

If your contribution is in a grey area, open an issue and discuss it first.

---

## Development Setup

### Prerequisites

- Python 3.9 or later
- Git
- A fork of this repository

### Quick Setup (Makefile)

The fastest way to get a working development environment:

```bash
git clone https://github.com/<your-username>/sword-legend-explorer.git
cd sword-legend-explorer
make install   # installs the package + dev dependencies
make assets    # generates demo template images
make test      # verifies everything works
```

### Manual Setup

If you prefer not to use Make:

```bash
# 1. Clone your fork
git clone https://github.com/<your-username>/sword-legend-explorer.git
cd sword-legend-explorer

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install in development mode (includes dev tools)
pip install -e ".[dev]"

# 4. Generate demo assets
python scripts/generate_demo_assets.py

# 5. Verify setup
pytest tests/ -q
python demo_app/visual_grid_world.py --steps 10
```

### Dev Container (VS Code / Codespaces)

If you use VS Code or GitHub Codespaces, open the project in a dev
container for a pre-configured environment:

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. `Ctrl+Shift+P` → "Dev Containers: Open Folder in Container"
3. The container auto-installs dependencies and generates assets

See [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json).

---

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to enforce code
quality before each commit. After cloning:

```bash
pip install pre-commit
pre-commit install
```

This installs hooks for:
- **ruff** — linting and formatting
- **mypy** — type checking (on `src/` only)
- Standard checks — trailing whitespace, end-of-file, YAML/TOML validity

To run all hooks manually:

```bash
pre-commit run --all-files
```

---

## Development Workflow

### 1. Create a branch

```bash
git checkout -b feature/my-feature
```

Use descriptive branch names:
- `feature/add-edge-detection`
- `fix/template-match-threshold`
- `docs/update-architecture`

### 2. Make your changes

Keep commits focused. Write clear, conventional commit messages:

```
type: short description

Optional longer explanation.

- Bullet point of key change
```

Common types: `feat`, `fix`, `docs`, `test`, `chore`, `refactor`.

### 3. Test your changes

```bash
# Run the full test suite
make test

# Run with coverage
make test-cov

# Run the demo to verify end-to-end
make demo

# Run the OSS readiness check
make check

# Lint your code
make lint

# Type check
make type
```

### 4. Commit and push

```bash
git add -A
git commit -m "feat: add edge detection to vision engine"
git push origin feature/my-feature
```

### 5. Open a Pull Request

Use the [PR template](.github/PULL_REQUEST_TEMPLATE.md) and fill in all
sections. The safety checklist is mandatory.

---

## Makefile Commands Reference

| Command | Description |
|---------|-------------|
| `make install` | Install package + dev dependencies |
| `make test` | Run pytest (no coverage) |
| `make test-cov` | Run pytest with coverage report |
| `make demo` | Run the synthetic demo (20 steps) |
| `make assets` | Generate demo template images |
| `make check` | Run OSS readiness check |
| `make lint` | Run ruff linter |
| `make format` | Run ruff formatter |
| `make type` | Run mypy type checker |
| `make security` | Run bandit security scanner |
| `make clean` | Remove build artifacts and caches |

---

## Pull Request Guidelines

- **One feature per PR** — keep PRs small and reviewable.
- **Tests required** — new code must have tests that pass. Aim for ≥80%
  coverage on new lines.
- **Document changes** — update relevant docs and the `CHANGELOG.md`
  `[Unreleased]` section.
- **No secrets** — never commit API keys, credentials, or personal data.
- **No game-specific content** — keep the framework generic and safe.
- **Safety checklist** — the PR template includes a safety checklist that
  must be completed before merge.

---

## Coding Style

- **Python 3.9+** compatible.
- **PEP 8** with line length 100 (enforced by ruff).
- **Type hints** for all public functions and methods.
- **Docstrings** for modules, classes, and public functions (Google style).
- **Keep functions small** and focused; prefer composition over inheritance.
- **No `print()` in library code** — use the `logging` module.

Ruff configuration is in [`pyproject.toml`](pyproject.toml) under
`[tool.ruff]`. Run `make format` to auto-format.

---

## Project Structure

```
src/              Core framework (fsm, vision, agent, hil_client, hil_server, main)
demo_app/         Synthetic demo environment (default, no external dependencies)
tests/            Pytest test suite (61 tests)
docs/             Architecture, API reference, troubleshooting, safety
docs/api/         API reference for each module
docs/releases/    Release notes per version
docs/agent_ledger/  Maintenance tracking files (cross-session context)
assets/demo/      Programmatically generated demo templates
scripts/          Utility scripts (asset generation, OSS check)
examples/         Usage examples
.github/          CI workflows, issue/PR templates, CODEOWNERS
```

---

## Adding New Features

### New FSM states or transitions

1. Add the state/transitions in `src/main.py::build_demo_fsm()` (or your
   custom FSM).
2. Add tests in `tests/test_fsm.py`.
3. Update `docs/api/fsm.md` if the public API changes.
4. Update `CHANGELOG.md`.

### New vision templates

1. Add drawing primitives in `demo_app/visual_grid_world.py`.
2. Add a template generator in `scripts/generate_demo_assets.py`.
3. Run `make assets` to regenerate.
4. Add tests if the template introduces a new match category.

### New decision logic

1. Implement a new `DecisionAgent` subclass in `src/agent.py`.
2. Add tests in `tests/test_agent.py`.
3. Update `docs/api/agent.md`.

---

## Reporting Issues

- **Bug reports**: Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.yml).
- **Feature requests**: Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.yml).
- **Security vulnerabilities**: See [`SECURITY.md`](SECURITY.md) — do **not**
  open a public issue for security problems.

When reporting a bug, include:
- Python version and OS
- Output of `pytest tests/ -q`
- Output of `python demo_app/visual_grid_world.py --steps 5`
- Steps to reproduce

---

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
