
.PHONY: help install install-dev test lint format clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:
	pip install .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/utest/ -v

test-cov:
	pytest tests/utest/ --cov=Agent --cov-report=html --cov-report=term

lint:
	flake8 Agent/ tests/
	mypy Agent/ --ignore-missing-imports

format:
	black Agent/ tests/
	isort Agent/ tests/

format-check:
	black --check Agent/ tests/
	isort --check Agent/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .coverage htmlcov/
	rm -rf Agent/__pycache__/ Agent/**/__pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*

pre-commit:
	pre-commit run --all-files

