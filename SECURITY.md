# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
**responsibly**:

1. **Do not** open a public GitHub issue.
2. Use GitHub's private vulnerability reporting feature: go to the
   repository's **Security** tab and click **"Report a vulnerability"**.
   This keeps your report private and visible only to maintainers.
3. Include a clear description of the issue, steps to reproduce, and the
   potential impact.
4. You will receive an acknowledgement within 72 hours.

We appreciate responsible disclosure and will credit reporters in release
notes (unless you prefer to remain anonymous).

## Scope

This policy covers the code in this repository. It does **not** cover:

- Vulnerabilities in third-party dependencies (report to the upstream project).
- Issues arising from misuse of the live screen-capture mode against systems
  you do not own or are not authorised to control.

## Safety Boundaries (Important)

This project is designed for **local, controlled demo environments, research,
and education**. It is explicitly **not** intended for:

- Cheating in games or circumventing anti-cheat systems
- Botting or automating third-party services without authorisation
- Bypassing platform rules, terms of service, or access controls
- Any activity that violates applicable laws or regulations

The default demo runs entirely against a **local synthetic environment**
(`demo_app/visual_grid_world.py`) and performs no screen capture, no network
requests (except the optional local HIL server), and no input to external
software.

The optional `live` mode captures a screen region and performs mouse input.
**Use it only on systems you own or are authorised to control.** See
[`docs/safety-boundaries.md`](docs/safety-boundaries.md) for full details.

## Security Best Practices for Contributors

- Never commit secrets, API keys, or credentials.
- Never add features whose primary purpose is evasion, detection-avoidance,
  or circumvention of security controls.
- Keep `pyautogui.FAILSAFE` enabled (default `True`) in live mode so users
  can abort input by moving the mouse to a screen corner.
- Validate all external inputs (HIL correction payloads, config files).
