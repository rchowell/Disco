.DEFAULT_GOAL := help

SHELL=/bin/bash
VENV = .venv
PYTHON_VERSION ?= python3.11

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

.PHONY: venv
venv:
	uv venv .venv -p python3.11; . .venv/bin/activate; uv pip install -r pyproject.toml

.PHONY: check
check:
	.git/hooks/pre-commit

.PHONY: hooks
hooks: .venv
	source $(VENV_BIN)/activate && pre-commit install --install-hooks

.PHONY: test
test:
	$(VENV_BIN)/pytest

.PHONY: clean
clean:
	rm -rf $(VENV)
