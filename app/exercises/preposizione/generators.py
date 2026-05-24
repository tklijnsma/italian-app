import json
import random
from functools import lru_cache
from pathlib import Path

from app.exercises.models import AnswerFormat, ExerciseGenerator, ExerciseGroup, StoredExercise


DATA_PATH = Path(__file__).with_name("italian_prepositions.jsonl")


@lru_cache(maxsize=1)
def load_preposition_items() -> list[dict]:
    items = []
    with DATA_PATH.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            _validate_item(item, line_number)
            items.append(item)
    if not items:
        raise ValueError(f"No preposition exercises found in {DATA_PATH}")
    return items


class Preposizione(ExerciseGenerator):
    group = ExerciseGroup(
        id="preposizione",
        title="Preposizione",
        description="Fill in the right preposizione. Answer with only the preposizione.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        item = rng.choice(load_preposition_items())
        return StoredExercise(
            exercise_id=exercise_id,
            group_id=self.group.id,
            title=self.group.title,
            description=self.group.description,
            query=item["query"],
            answer_format=AnswerFormat.ONLY_PREPOSITION,
            metadata={
                "base_preposition": item["base_preposition"],
                "article": item.get("article"),
                "following_token": item.get("following_token"),
                "following_lemma": item.get("following_lemma"),
                "following_pos": item.get("following_pos"),
                "construction_type": item.get("construction_type"),
                "source": item.get("source"),
            },
            expected_answers=item["answers"],
        )


def _validate_item(item: dict, line_number: int) -> None:
    required = ["query", "answers", "base_preposition"]
    missing = [key for key in required if key not in item]
    if missing:
        raise ValueError(f"{DATA_PATH}:{line_number} missing required field(s): {', '.join(missing)}")
    if not isinstance(item["answers"], list) or not item["answers"]:
        raise ValueError(f"{DATA_PATH}:{line_number} answers must be a non-empty list")
