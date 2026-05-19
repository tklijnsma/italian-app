# Italian Grammar Practice API

FastAPI backend for a small Italian grammar practice app. It generates exercises on demand, stores generated answers in memory, and checks normalized user answers.

## Setup

Python 3.11+ is recommended.

```bash
make install
```

Dependencies are managed with `pyproject.toml` and `uv sync`. `mlconjug3` is a hard dependency for Italian conjugation.

## Run the API

```bash
make run
```

The API starts at `http://127.0.0.1:8000`.

CORS is permissive (`*`) so a separately hosted React/static frontend, including GitHub Pages or local dev servers, can call it.

## Run Tests

```bash
make test
```

## Developer TUI

There is a small internal Textual terminal app for manually inspecting generated exercises. It imports the exercise registry directly; it does not call the FastAPI endpoints and does not require uvicorn to be running.

Install dev dependencies:

```bash
uv sync
```

Run with all exercise groups:

```bash
.venv/bin/python -m app.devtools.exercise_tui
```

Run with selected groups:

```bash
.venv/bin/python -m app.devtools.exercise_tui --groups pronome_diretto_presente,congiuntivo_presente,preposizione
```

## Example Requests

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl http://127.0.0.1:8000/exercise-groups
```

```bash
curl -X POST http://127.0.0.1:8000/exercises/generate \
  -H 'Content-Type: application/json' \
  -d '{"group_id":"pronome_diretto_presente","seed":123}'
```

```bash
curl -X POST http://127.0.0.1:8000/exercises/check \
  -H 'Content-Type: application/json' \
  -d '{"exercise_id":"<exercise_id from generate>","answer":"Te lo invio"}'
```

## Structure

- `app/api`: FastAPI route handlers.
- `app/grammar`: reusable functional grammar helpers exposed through `app.grammar.api`.
- `app/exercises`: explicit exercise registry and grouped exercise modules.
- `tests`: pytest coverage for helpers, generators, and API behavior.

Generated exercises are stored in memory only. Restarting the process clears them.
