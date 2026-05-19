from app.grammar import api as grammar
from app.exercises.models import CheckExerciseResponse, StoredExercise


def check_answer(exercise: StoredExercise, answer: str) -> CheckExerciseResponse:
    normalized = grammar.normalize_answer(answer)
    normalized_expected = [grammar.normalize_answer(expected) for expected in exercise.expected_answers]
    correct = normalized in normalized_expected
    return CheckExerciseResponse(
        correct=correct,
        expected_answers=exercise.expected_answers,
        normalized_answer=normalized,
        hint=None if correct else hint_for_answer(normalized, normalized_expected, exercise.metadata),
    )


def hint_for_answer(normalized: str, expected: list[str], metadata: dict) -> str | None:
    if any(answer.replace("'", "") == normalized.replace("'", "") for answer in expected):
        return "Check the apostrophe."
    if "participle" in metadata and metadata["participle"] not in normalized:
        return "Check the past participle agreement."
    if "reflexive_pronoun" in metadata and f" {metadata['reflexive_pronoun']} " not in f" {normalized} ":
        return "Check the reflexive pronoun."
    if "base_preposition" in metadata:
        return "Check whether the preposition needs to combine with the article."
    return None
