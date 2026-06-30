# Troubleshooting

Common issues and solutions for Vision FSM Agent.

## Installation

### `cv2.error` or `ModuleNotFoundError: No module named 'cv2'`

OpenCV didn't install correctly. Try:

```bash
pip install opencv-python --force-reinstall
```

On some Linux systems you may also need system libraries:

```bash
# Ubuntu/Debian
sudo apt install libgl1-mesa-glx libglib2.0-0

# Fedora
sudo dnf install mesa-libGL glib2
```

### `ModuleNotFoundError: No module named 'numpy'`

Install dependencies in your virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Or use the dev extras:

```bash
pip install -e ".[dev]"
```

## Running the Demo

### "No templates found" or demo exits immediately

The demo needs template images in `assets/demo/`. Generate them:

```bash
python scripts/generate_demo_assets.py
```

Verify the files exist:

```bash
ls assets/demo/
# Should show: interact_button.png  pickup_item.png  target_goal.png
```

### Demo runs but agent doesn't move

Check `confidence_default` in `config.yaml`. If it's too high, template
matching may not find elements. Try lowering:

```yaml
confidence_default: 0.6
```

### Demo doesn't complete in 50 steps

Some random seeds produce harder layouts. Options:

1. Increase step count: `python demo_app/visual_grid_world.py --steps 60`
2. Change the seed in `config.yaml`: `demo_seed: 7`
3. Reduce grid size for faster completion: `demo_grid_w: 8`

### `TypeError: 'NoneType' object is not subscriptable` during demo

This usually means a template failed to load. Ensure `assets/demo/`
contains the 3 PNG files and they are valid images.

## Windows Issues

### Unicode characters show as `???` or garbled

Set console encoding to UTF-8:

```cmd
chcp 65001
set PYTHONIOENCODING=utf-8
```

Or run in PowerShell, which handles UTF-8 better.

### `pyautogui` fails with `ImageNotFoundException`

This only happens in **live mode** (not the default demo). Ensure:
- `pyautogui` is installed: `pip install pyautogui`
- The target window is visible and not minimized
- `capture_region` in `config.yaml` matches the window position

### Path issues with backslashes

Use forward slashes in config or pass absolute paths. The framework
uses `os.path` internally and handles both on Windows.

## pytest Issues

### `ImportError: No module named 'fsm'` in tests

The `tests/conftest.py` adds `src/` to `sys.path`. If you're running
pytest from a different directory, ensure you're in the project root:

```bash
cd /path/to/sword-legend-explorer
pytest tests/ -q
```

### Tests pass locally but fail in CI

Common causes:
- Missing demo assets: CI runs `generate_demo_assets.py` before tests.
  If you added new templates, update the generator script.
- Python version differences: CI tests 3.9/3.11/3.13. Check for
  version-specific syntax.
- OS differences: OpenCV behavior may differ on Windows vs Linux for
  edge cases. Use the demo's synthetic frames, not real screenshots.

### `CoverageWarning: Module src was never imported`

Run pytest with the correct coverage source:

```bash
pytest tests/ -q --cov=src
```

Not `--cov=src.main` or `--cov`.

## HIL Server Issues

### `requests.exceptions.ConnectionError` when polling HIL

The HIL server isn't running. Start it:

```bash
python run.py --hil
```

Or ignore the warnings — the agent continues autonomously when HIL is
unavailable.

### HIL server port 8001 already in use

Change the port in `src/hil_server.py` (the `run()` call) and update
`hil_server_url` in `config.yaml`.

## Performance

### Demo is slow

- Reduce `loop_delay` in `config.yaml`: `[0.1, 0.2]`
- Reduce `scale_steps`: `5` (from `10`)
- Narrow `scale_range`: `[0.8, 1.2]` (from `[0.6, 1.4]`)

### Template matching is inaccurate

- Increase `confidence_default` (e.g., `0.85`) to reduce false positives
- Increase `scale_steps` for better multi-scale coverage
- Ensure templates are crisp (regenerate with `generate_demo_assets.py`)

## Still Stuck?

1. Check [existing issues](https://github.com/evanzheng0107-dev/sword-legend-explorer/issues)
2. Run the OSS readiness check: `python scripts/oss_readiness_check.py --verbose`
3. Open a [bug report](https://github.com/evanzheng0107-dev/sword-legend-explorer/issues/new)
   with the output of:
   ```bash
   python --version
   pytest tests/ -q
   python demo_app/visual_grid_world.py --steps 5
   ```
