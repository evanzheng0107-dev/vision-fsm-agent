## Description

<!-- Briefly describe what this PR does and why. -->

## Type of change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Test improvement

## Safety checklist

- [ ] This PR does **not** add anti-detection, evasion, or human-mimicry features
- [ ] This PR does **not** target specific commercial games or services
- [ ] This PR does **not** add code intended to bypass platform rules or terms of service
- [ ] This PR does **not** introduce real screenshots or third-party imagery
- [ ] This PR keeps the default mode as the local synthetic demo

(See [`docs/safety-boundaries.md`](../docs/safety-boundaries.md) and [`SECURITY.md`](../SECURITY.md).)

## Testing

- [ ] `pytest tests/ -v` passes (all tests green)
- [ ] `python demo_app/visual_grid_world.py --steps 20` runs successfully
- [ ] New code has corresponding tests

## Changes to documentation

- [ ] Updated `README.md` if needed
- [ ] Updated `docs/` if needed
- [ ] Updated `CHANGELOG.md` under `[Unreleased]`

## Notes for reviewers

<!-- Anything else reviewers should know. -->
