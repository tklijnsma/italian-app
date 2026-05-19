# Continuation Notes

This project is a Python FastAPI backend for a hobby Italian grammar practice app. It generates Italian grammar exercises on demand, stores generated exercises in memory, and checks user answers. There is no database, auth, frontend, Docker setup, analytics, or progress tracking. The app is intentionally small and optimized for correctness, readability, and easy extension.

## Current State

The backend exposes four API endpoints:

- `GET /health`
- `GET /exercise-groups`
- `POST /exercises/generate`
- `POST /exercises/check`

The FastAPI app lives in `app/main.py`, and routes live in `app/api/routes.py`.

There is also a small internal Textual terminal tool for manually testing exercises:

```bash
python -m app.devtools.exercise_tui
python -m app.devtools.exercise_tui --groups pronome_diretto_presente,congiuntivo_presente,preposizione
```

This TUI is developer-only. It imports the exercise registry directly and does not call HTTP endpoints.

## Dependency Setup

The project uses `pyproject.toml` and `uv.lock`, not `requirements.txt`.

Install/sync dependencies:

```bash
uv sync
```

Run tests:

```bash
.venv/bin/pytest
```

Run API:

```bash
.venv/bin/uvicorn app.main:app --reload
```

Deploy branch:

- `prod`

Render deployment files:

- `render.yaml`
- `.python-version`

Render uses:

- build command: `pip install .`
- start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- health check path: `/health`

Important dependency notes:

- `mlconjug3` is a hard runtime dependency.
- `setuptools>=70,<81` is pinned because `mlconjug3` imports `pkg_resources`.
- `numpy<2` is pinned because the `mlconjug3` scikit-learn path is not compatible with NumPy 2.x in this environment.
- `textual==0.10.0` is a dev dependency only. Newer Textual versions conflict with `mlconjug3`'s `rich==13.2.0` dependency.

## Architecture

The code is split into reusable grammar functions and exercise modules.

### `app/grammar`

Reusable grammar rules live here. Public imports should generally use:

```python
from app.grammar import api as grammar
```

`app/grammar/api.py` re-exports:

- `normalize_answer`
- `direct_pronoun_for_noun`
- `combined_indirect_direct_pronoun`
- `elide_combined_pronoun_before_ho`
- `attach_pronouns_to_infinitive`
- `agree_past_participle`
- `reflexive_pronoun`
- `contract_preposition`

The grammar module exposes a functional API only. There are no grammar classes and no public mutable state.

### `app/exercises`

Exercise-specific modules live here. An exercise module may contain multiple generators/classes when they share logic.

Current modules:

- `app/exercises/pronome_diretto/generators.py`
  - `PronomeDirettoPresente`
  - `PronomeDirettoPassatoProssimo`
  - `PronomeDirettoPresenteModale`
- `app/exercises/congiuntivo/generators.py`
  - `CongiuntivoPresente`
  - `PeriodoIpoteticoCongiuntivoImperfettoCondizionale`
- `app/exercises/riflessivo/generators.py`
  - `RiflessivoPresente`
- `app/exercises/preposizione/generators.py`
  - `Preposizione`

`app/exercises/registry.py` is explicit. It does not auto-discover modules. It defines:

- `EXERCISE_GENERATORS`
- `GENERATORS_BY_GROUP_ID`
- `exercise_groups()`
- `generate_exercise(group_id, seed=None)`

`app/exercises/checking.py` contains shared answer checking logic used by both API routes and the TUI.

`app/exercises/conjugation.py` wraps repeated `mlconjug3` lookup details:

- `conjugate(verb, tense, subject)`
- `past_participle(verb)`

There are no hard-coded conjugation fallback tables. If `mlconjug3` is unavailable or broken, the app should fail rather than silently using fallback conjugation.

## Exercise Groups

The 7 registered group IDs are:

1. `pronome_diretto_presente`
2. `pronome_diretto_passato_prossimo`
3. `pronome_diretto_presente_modale`
4. `congiuntivo_presente`
5. `periodo_ipotetico_congiuntivo_imperfetto_condizionale`
6. `riflessivo_presente`
7. `preposizione`

Important examples that tests protect:

- `Io (inviare PRESENTE) un messaggio a te` -> `Te lo invio`
- `Io (inviare PASSATO PROSSIMO) una pizza a te` -> `Te l'ho inviata`
- `Io (volere + inviare PRESENTE) un messaggio a te` -> `Voglio inviartelo`
- `Io (potere + dare PRESENTE) una pizza a lui` -> `Posso dargliela`
- `Credo che tu (prendere) una pizza` -> `prenda`
- `Se mia nonna (avere) le ruote, (essere) una cariola` -> `avesse sarebbe`
- `Io (lavare a me) le mani` -> `Io mi lavo le mani`
- `Metto il bicchiere ____ tavolo` -> `sul`

## Data Approach

There is no global `app/data` folder anymore. Small curated word lists live near the exercise module that uses them, usually as plain Python constants. This is intentional. Duplicating small lists is acceptable if it keeps modules readable.

## In-Memory Storage

Generated exercises are stored in an in-memory dictionary in `app/api/routes.py`:

```python
EXERCISE_STORE = {}
```

The generated exercise response does not include expected answers. The expected answers are stored server-side in memory and used later by `/exercises/check`.

Restarting the API process clears stored exercises.

## CORS

`app/main.py` configures permissive CORS:

- `allow_origins=["*"]`
- all methods
- all headers

This is intended to make a future static React frontend easy to host separately, for example on GitHub Pages.

## Tests

Current test files:

- `tests/test_api.py`
- `tests/test_devtools_tui.py`
- `tests/test_exercise_architecture.py`
- `tests/test_grammar_api.py`

The suite verifies:

- API endpoint behavior
- grammar function behavior
- explicit registry architecture
- all 7 generators produce valid exercises
- pronome diretto module exposes all 3 generators
- old global `app/data/verbs.json` and `app/data/nouns.json` are gone
- Textual is not imported by normal API modules
- TUI group parsing and compose compatibility

Last verified command:

```bash
.venv/bin/pytest
```

Result:

```text
22 passed
```

Expected warnings come from `mlconjug3` internals using deprecated `pkg_resources` and `locale.getdefaultlocale`.

## Known Constraints

- This app is designed for 2-3 concurrent users and manual/hobby use.
- There is no persistence. Do not assume exercise IDs survive process restarts.
- Textual is dev-only. Do not import it from API modules.
- The API schema is currently stable and intended for a future React frontend.
- Keep future changes simple. Avoid auto-discovery, heavy abstractions, or a global data infrastructure unless there is a clear need.
