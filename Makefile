.PHONY: install test run

install:
	uv sync

test:
	.venv/bin/pytest

run:
	.venv/bin/uvicorn app.main:app --reload
