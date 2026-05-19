import random

from app.exercises.conjugation import conjugate
from app.exercises.models import AnswerFormat, ExerciseGenerator, ExerciseGroup, StoredExercise


CONGIUNTIVO_PRESENTE_VERBS = ["prendere", "vedere", "mangiare"]


class CongiuntivoPresente(ExerciseGenerator):
    group = ExerciseGroup(
        id="congiuntivo_presente",
        title="Congiuntivo PRESENTE",
        description="Conjugate the verb to congiuntivo presente.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        verb = rng.choice(CONGIUNTIVO_PRESENTE_VERBS)
        subject = rng.choice(["tu", "lui", "lei"])
        query = f"Credo che {subject} ({verb}) una pizza"
        expected = conjugate(verb, "congiuntivo_presente", subject)
        return StoredExercise(
            exercise_id=exercise_id,
            group_id=self.group.id,
            title=self.group.title,
            description=self.group.description,
            query=query,
            answer_format=AnswerFormat.ONLY_WORDS,
            metadata={"verb": verb, "subject": subject},
            expected_answers=[expected],
        )


class PeriodoIpoteticoCongiuntivoImperfettoCondizionale(ExerciseGenerator):
    group = ExerciseGroup(
        id="periodo_ipotetico_congiuntivo_imperfetto_condizionale",
        title="Congiuntivo IMPERFETTO + CONDIZIONALE",
        description="Conjugate the verbs. Answer with only the verbs.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        query = "Se mia nonna (avere) le ruote, (essere) una cariola"
        expected = (
            f"{conjugate('avere', 'congiuntivo_imperfetto', 'lei')} "
            f"{conjugate('essere', 'condizionale_presente', 'lei')}"
        )
        return StoredExercise(
            exercise_id=exercise_id,
            group_id=self.group.id,
            title=self.group.title,
            description=self.group.description,
            query=query,
            answer_format=AnswerFormat.ONLY_WORDS,
            metadata={"first_verb": "avere", "second_verb": "essere", "subject": "lei"},
            expected_answers=[expected],
        )
