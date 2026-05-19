import random

from app.exercises.models import AnswerFormat, ExerciseGenerator, ExerciseGroup, StoredExercise


PREPOSITION_ITEMS = [
    {
        "query": "Metto il bicchiere ____ tavolo",
        "base_preposition": "su",
        "article": "il",
        "noun": "tavolo",
        "answers": ["sul"],
    },
    {
        "query": "Vado ____ scuola",
        "base_preposition": "a",
        "article": "la",
        "noun": "scuola",
        "answers": ["alla"],
    },
    {
        "query": "Il gatto dorme ____ giardino",
        "base_preposition": "in",
        "article": "il",
        "noun": "giardino",
        "answers": ["nel"],
    },
    {
        "query": "Parlo ____ amici",
        "base_preposition": "con",
        "article": "",
        "noun": "amici",
        "answers": ["con gli", "con"],
    },
]


class Preposizione(ExerciseGenerator):
    group = ExerciseGroup(
        id="preposizione",
        title="Preposizione",
        description="Fill in the right preposizione. Answer with only the preposizione.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        item = rng.choice(PREPOSITION_ITEMS)
        return StoredExercise(
            exercise_id=exercise_id,
            group_id=self.group.id,
            title=self.group.title,
            description=self.group.description,
            query=item["query"],
            answer_format=AnswerFormat.ONLY_PREPOSITION,
            metadata={"base_preposition": item["base_preposition"], "article": item["article"], "noun": item["noun"]},
            expected_answers=item["answers"],
        )
