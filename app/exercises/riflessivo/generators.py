import random

from app.grammar import api as grammar
from app.exercises.conjugation import conjugate
from app.exercises.models import AnswerFormat, ExerciseGenerator, ExerciseGroup, StoredExercise


REFLEXIVE_VERBS = {
    "lavare": {"conjugation_lemma": "lavare", "object": "le mani"},
    "svegliarsi": {"conjugation_lemma": "svegliare", "object": ""},
    "alzarsi": {"conjugation_lemma": "alzare", "object": ""},
    "chiamarsi": {"conjugation_lemma": "chiamare", "object": ""},
}


class RiflessivoPresente(ExerciseGenerator):
    group = ExerciseGroup(
        id="riflessivo_presente",
        title="Reflessivo PRESENTE",
        description="Apply the riflessivo. Write the whole sentence.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        subject = rng.choice(["Io", "Tu", "Lui", "Lei", "Noi", "Voi", "Loro"])
        verb = rng.choice(list(REFLEXIVE_VERBS))
        verb_data = REFLEXIVE_VERBS[verb]
        object_phrase = verb_data["object"]
        reflexive = grammar.reflexive_pronoun(subject)
        conjugated = conjugate(verb_data["conjugation_lemma"], "presente", subject)
        expected = f"{subject} {reflexive} {conjugated}"
        if object_phrase:
            expected = f"{expected} {object_phrase}"
        query = f"{subject} ({verb_data['conjugation_lemma']} a {subject.lower()})"
        if object_phrase:
            query = f"{query} {object_phrase}"
        return StoredExercise(
            exercise_id=exercise_id,
            group_id=self.group.id,
            title=self.group.title,
            description=self.group.description,
            query=query,
            answer_format=AnswerFormat.WHOLE_SENTENCE,
            metadata={"verb": verb, "subject": subject, "reflexive_pronoun": reflexive},
            expected_answers=[expected],
        )
