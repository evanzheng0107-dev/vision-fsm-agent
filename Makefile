# Makefile for Vision FSM Agent
# Usage: make <target>   (run `make` with no args to see all targets)

.PHONY: install test test-cov demo assets check lint type security clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install dev dependencies
	pip install -e ".[dev]"

test: ## Run tests (no coverage)
	pytest tests/ -q

test-cov: ## Run tests with coverage
	pytest tests/ -q --cov=src --cov-report=term-missing --cov-report=html

demo: ## Run the synthetic demo (20 steps)
	python demo_app/visual_grid_world.py --steps 20

assets: ## Generate demo template assets
	python scripts/generate_demo_assets.py

check: ## Run OSS readiness check
	python scripts/oss_readiness_check.py

lint: ## Run ruff linter
	ruff check src/ tests/ demo_app/ scripts/ examples/

format: ## Run ruff formatter
	ruff format src/ tests/ demo_app/ scripts/ examples/

type: ## Run mypy type checker
	mypy src/

security: ## Run bandit security scanner
	bandit -r src/ -q

clean: ## Clean build artifacts
	rm -rf __pycache__ .pytest_cache .coverage htmlcov *.egg-info dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
