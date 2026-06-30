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

## Getting Started

1. **Fork** the repository and clone your fork.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Run the demo** to verify your setup:
   ```bash
   python demo_app/visual_grid_world.py --steps 10
   ```
4. **Run the tests**:
   ```bash
   pytest tests/ -v
   ```
5. **Generate demo assets** (if needed):
   ```bash
   python scripts/generate_demo_assets.py
   ```

## Development Workflow

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```
2. **Make your changes**. Keep commits focused and write clear messages.
3. **Add or update tests** for any new functionality. Aim to maintain or
   improve test coverage.
4. **Run the full test suite**:
   ```bash
   pytest tests/ -v
   ```
5. **Verify the demo still runs**:
   ```bash
   python demo_app/visual_grid_world.py --steps 10
   ```
6. **Commit and push** to your fork.
7. **Open a Pull Request** using the PR template.

## Pull Request Guidelines

- **One feature per PR** — keep PRs reviewable.
- **Tests required** — new code must have tests that pass.
- **Document changes** — update relevant docs and the CHANGELOG.
- **No secrets** — never commit API keys, credentials, or personal data.
- **No game-specific content** — keep the framework generic.

## Coding Style

- Python 3.9+ compatible.
- Follow [PEP 8](https://peps.python.org/pep-0008/) (line length 100).
- Use type hints for public functions.
- Write docstrings for modules, classes, and public functions.
- Keep functions small and focused; prefer composition over inheritance.

## Project Structure

```
src/          Core framework (fsm, vision, agent, hil_client, hil_server, main)
demo_app/     Synthetic demo environment (no external dependencies)
tests/        Pytest test suite
docs/         Architecture and safety documentation
assets/demo/  Programmatically generated demo templates
scripts/      Utility scripts (asset generation, etc.)
examples/     Usage examples
```

## Reporting Issues

Use the GitHub issue templates. For security vulnerabilities, see
[`SECURITY.md`](SECURITY.md) — do **not** open a public issue for security
problems.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
