"""Tests for config loading."""
import pytest

from main import load_config


def test_load_config_finds_yaml():
    """load_config should find the project's config.yaml."""
    config = load_config()
    assert isinstance(config, dict)
    assert "environment" in config
    assert config["environment"] == "demo"
    assert "demo_max_steps" in config


def test_config_has_demo_defaults():
    config = load_config()
    assert config.get("demo_grid_w", 12) == 12
    assert config.get("confidence_default", 0.8) == 0.75
    assert "scale_range" in config


def test_config_has_vision_params():
    """Config should contain vision matching parameters."""
    config = load_config()
    assert "scale_range" in config
    assert "scale_steps" in config
    assert isinstance(config["scale_range"], list)
    assert len(config["scale_range"]) == 2


def test_config_has_timing_params():
    """Config should contain loop timing parameters."""
    config = load_config()
    for key in ("loop_delay", "wait_delay", "max_failed_attempts"):
        assert key in config, f"Missing config key: {key}"


def test_config_environment_is_demo_by_default():
    """The default environment should be demo (safe)."""
    config = load_config()
    assert config.get("environment") == "demo"
