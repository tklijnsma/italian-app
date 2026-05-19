# Italian Grammar Practice API

Base URL for local development:

```text
http://127.0.0.1:8000
```

The API returns JSON. There is no authentication.

Generated exercises are stored in server memory. The frontend receives an `exercise_id` from `/exercises/generate` and must use that ID when calling `/exercises/check`. If the backend restarts, old `exercise_id` values stop working.

## CORS

The backend is configured with permissive CORS for a separately hosted static frontend:

- any origin
- any method
- any header

## Answer Formats

`answer_format` is one of:

```text
whole_sentence
only_words
only_preposition
```

## Exercise Group IDs

The current exercise group IDs are:

```text
pronome_diretto_presente
pronome_diretto_passato_prossimo
pronome_diretto_presente_modale
congiuntivo_presente
periodo_ipotetico_congiuntivo_imperfetto_condizionale
riflessivo_presente
preposizione
```

## GET /health

Returns a simple health check.

### Request

```http
GET /health
```

### Response 200

```json
{
  "status": "ok"
}
```

## GET /exercise-groups

Returns the available exercise groups.

### Request

```http
GET /exercise-groups
```

### Response 200

```json
[
  {
    "id": "pronome_diretto_presente",
    "title": "Pronome Diretto PRESENTE",
    "description": "Conjugate the verb, and use the pronome indiretto. Write the whole sentence."
  },
  {
    "id": "pronome_diretto_passato_prossimo",
    "title": "Pronome Diretto PASSATO PROSSIMO",
    "description": "Conjugate the verb, and use the pronome indiretto. Write the whole sentence."
  },
  {
    "id": "pronome_diretto_presente_modale",
    "title": "Pronome Diretto PRESENTE con dovere/potere/volere",
    "description": "Conjugate the modal verb, and attach the pronouns to the infinitive. Write the whole sentence."
  },
  {
    "id": "congiuntivo_presente",
    "title": "Congiuntivo PRESENTE",
    "description": "Conjugate the verb to congiuntivo presente."
  },
  {
    "id": "periodo_ipotetico_congiuntivo_imperfetto_condizionale",
    "title": "Congiuntivo IMPERFETTO + CONDIZIONALE",
    "description": "Conjugate the verbs. Answer with only the verbs."
  },
  {
    "id": "riflessivo_presente",
    "title": "Reflessivo PRESENTE",
    "description": "Apply the riflessivo. Write the whole sentence."
  },
  {
    "id": "preposizione",
    "title": "Preposizione",
    "description": "Fill in the right preposizione. Answer with only the preposizione."
  }
]
```

## POST /exercises/generate

Generates one exercise for a requested group.

The response intentionally does not include expected answers.

### Request

```http
POST /exercises/generate
Content-Type: application/json
```

Body:

```json
{
  "group_id": "pronome_diretto_presente",
  "seed": 123
}
```

Fields:

- `group_id`: required string. Must be one of the registered exercise group IDs.
- `seed`: optional integer. When provided, generation for that group is deterministic for the current generator implementation.

### Response 200

```json
{
  "exercise_id": "9a9a897d-f09c-48cc-97da-77152dd77d59",
  "group_id": "pronome_diretto_presente",
  "title": "Pronome Diretto PRESENTE",
  "description": "Conjugate the verb, and use the pronome indiretto. Write the whole sentence.",
  "query": "Io (inviare PRESENTE) un messaggio a te",
  "answer_format": "whole_sentence",
  "metadata": {
    "verb": "inviare",
    "noun": {
      "text": "un messaggio",
      "lemma": "messaggio",
      "gender": "masculine",
      "number": "singular"
    },
    "indirect_object": "a te",
    "direct_pronoun": "lo"
  }
}
```

Notes:

- `exercise_id` is opaque. Store it and send it back to `/exercises/check`.
- `metadata` is useful for debugging or optional frontend display, but frontend correctness should not depend on its exact contents.
- `answer_format` tells the frontend what kind of answer UI/help text to show.

### Response 404

Returned when `group_id` is unknown.

```json
{
  "detail": "Unknown exercise group"
}
```

### Example curl

```bash
curl -X POST http://127.0.0.1:8000/exercises/generate \
  -H 'Content-Type: application/json' \
  -d '{"group_id":"pronome_diretto_presente","seed":123}'
```

## POST /exercises/check

Checks an answer for a previously generated exercise.

### Request

```http
POST /exercises/check
Content-Type: application/json
```

Body:

```json
{
  "exercise_id": "9a9a897d-f09c-48cc-97da-77152dd77d59",
  "answer": "Te lo invio"
}
```

Fields:

- `exercise_id`: required string. Must come from a previous `/exercises/generate` response from the same backend process.
- `answer`: required string. User answer to check.

### Response 200

```json
{
  "correct": true,
  "expected_answers": [
    "Te lo invio"
  ],
  "normalized_answer": "te lo invio",
  "hint": null
}
```

When incorrect:

```json
{
  "correct": false,
  "expected_answers": [
    "Te l'ho inviata"
  ],
  "normalized_answer": "te lho inviata",
  "hint": "Check the apostrophe."
}
```

Notes:

- Checking is case-insensitive.
- Leading/trailing spaces are ignored.
- Repeated spaces are collapsed.
- Curly apostrophes are normalized to straight apostrophes.
- A final period is ignored.
- `expected_answers` is returned after checking. This makes it easy for the frontend to show the correct answer.
- `hint` may be `null`.

### Response 404

Returned when `exercise_id` is unknown, expired, or was generated before the API process restarted.

```json
{
  "detail": "Unknown exercise"
}
```

### Example curl

```bash
curl -X POST http://127.0.0.1:8000/exercises/check \
  -H 'Content-Type: application/json' \
  -d '{"exercise_id":"9a9a897d-f09c-48cc-97da-77152dd77d59","answer":"Te lo invio"}'
```

## Example Exercise Queries and Expected Answers

These examples represent behavior the backend tests currently protect.

```text
Io (inviare PRESENTE) un messaggio a te
Expected: Te lo invio
Answer format: whole_sentence
```

```text
Io (inviare PASSATO PROSSIMO) una pizza a te
Expected: Te l'ho inviata
Answer format: whole_sentence
```

```text
Io (volere + inviare PRESENTE) un messaggio a te
Expected: Voglio inviartelo
Answer format: whole_sentence
```

```text
Io (potere + dare PRESENTE) una pizza a lui
Expected: Posso dargliela
Answer format: whole_sentence
```

```text
Credo che tu (prendere) una pizza
Expected: prenda
Answer format: only_words
```

```text
Se mia nonna (avere) le ruote, (essere) una cariola
Expected: avesse sarebbe
Answer format: only_words
```

```text
Io (lavare a me) le mani
Expected: Io mi lavo le mani
Answer format: whole_sentence
```

```text
Metto il bicchiere ____ tavolo
Expected: sul
Answer format: only_preposition
```

## Suggested Frontend Flow

1. Call `GET /exercise-groups`.
2. Let the user choose a group.
3. Call `POST /exercises/generate` with the selected `group_id`.
4. Render `title`, `description`, `query`, and answer input based on `answer_format`.
5. Call `POST /exercises/check` with `exercise_id` and the user's answer.
6. Show `correct`, `expected_answers`, and `hint`.
7. Generate the next exercise when the user continues.

