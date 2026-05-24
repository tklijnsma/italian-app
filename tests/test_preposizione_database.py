import random

from app.exercises.models import AnswerFormat
from app.exercises.preposizione.generators import Preposizione, load_preposition_items


def test_preposition_database_loads_from_jsonl():
    items = load_preposition_items()

    assert len(items) == 1200
    assert all(item["query"] for item in items)
    assert all(item["answers"] for item in items)


def test_preposition_generator_uses_database_items():
    items = load_preposition_items()
    rng = random.Random(7)
    expected_item = random.Random(7).choice(items)

    exercise = Preposizione().generate("preposition-example", rng)

    assert exercise.group_id == "preposizione"
    assert exercise.answer_format == AnswerFormat.ONLY_PREPOSITION
    assert exercise.query == expected_item["query"]
    assert exercise.expected_answers == expected_item["answers"]
    assert exercise.metadata["base_preposition"] == expected_item["base_preposition"]
    assert exercise.metadata["construction_type"] == expected_item["construction_type"]
