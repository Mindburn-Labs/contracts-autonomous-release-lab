SHELL := /usr/bin/env bash

.PHONY: setup lint test build

setup:
	@python3 --version

lint:
	@python3 -m compileall -q scripts tests
	@python3 scripts/validate_lab.py

test:
	@PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'

build: lint
