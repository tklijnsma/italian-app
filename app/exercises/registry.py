import random
import uuid

from app.exercises.congiuntivo import (
    CongiuntivoPresente,
    PeriodoIpoteticoCongiuntivoImperfettoCondizionale,
)
from app.exercises.models import ExerciseGenerator, ExerciseGroup, StoredExercise
from app.exercises.preposizione import Preposizione
from app.exercises.pronome_diretto import (
    PronomeDirettoPassatoProssimo,
    PronomeDirettoPresente,
    PronomeDirettoPresenteModale,
)
from app.exercises.riflessivo import RiflessivoPresente


EXERCISE_GENERATORS: list[ExerciseGenerator] = [
    PronomeDirettoPresente(),
    PronomeDirettoPassatoProssimo(),
    PronomeDirettoPresenteModale(),
    CongiuntivoPresente(),
    PeriodoIpoteticoCongiuntivoImperfettoCondizionale(),
    RiflessivoPresente(),
    Preposizione(),
]

GENERATORS_BY_GROUP_ID: dict[str, ExerciseGenerator] = {
    generator.group.id: generator for generator in EXERCISE_GENERATORS
}


def exercise_groups() -> list[ExerciseGroup]:
    return [generator.group for generator in EXERCISE_GENERATORS]


def generate_exercise(group_id: str, seed: int | None = None) -> StoredExercise:
    generator = GENERATORS_BY_GROUP_ID[group_id]
    return generator.generate(str(uuid.uuid4()), random.Random(seed))
