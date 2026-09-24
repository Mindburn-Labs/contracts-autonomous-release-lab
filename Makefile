SHELL := /usr/bin/env bash

# CI runs `make check` (platform-actions ci.yml v2, public copy in Mindburn-Labs/.github).
check: lint test

.PHONY: check setup lint test build

setup:
	@python3 --version

lint:
	@python3 -m compileall -q scripts tests
	@python3 scripts/validate_lab.py

test:
	@PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'

build: lint
