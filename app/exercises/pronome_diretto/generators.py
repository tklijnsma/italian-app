import random

from app.grammar import api as grammar
from app.exercises.conjugation import conjugate, past_participle
from app.exercises.models import AnswerFormat, ExerciseGenerator, ExerciseGroup, StoredExercise


NOUNS = [
    {"text": "un messaggio", "lemma": "messaggio", "gender": "masculine", "number": "singular"},
    {"text": "una pizza", "lemma": "pizza", "gender": "feminine", "number": "singular"},
    {"text": "i libri", "lemma": "libri", "gender": "masculine", "number": "plural"},
    {"text": "le chiavi", "lemma": "chiavi", "gender": "feminine", "number": "plural"},
]

INDIRECT_OBJECTS = ["a me", "a te", "a lui", "a lei", "a noi", "a voi", "a loro"]
TRANSITIVE_VERBS = ["inviare", "mandare", "comprare", "dare"]
MODAL_VERBS = ["volere", "potere", "dovere"]


class PronomeDirettoPresente(ExerciseGenerator):
    group = ExerciseGroup(
        id="pronome_diretto_presente",
        title="Pronome Diretto PRESENTE",
        description="Conjugate the verb, and use the pronome indiretto. Write the whole sentence.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        verb = rng.choice(TRANSITIVE_VERBS)
        noun = rng.choice(NOUNS)
        indirect = rng.choice(INDIRECT_OBJECTS)
        subject = "Io"
        direct = grammar.direct_pronoun_for_noun(noun)
        combined = grammar.combined_indirect_direct_pronoun(indirect, direct)
        expected = f"{combined.capitalize()} {conjugate(verb, 'presente', subject)}"
        query = f"{subject} ({verb} PRESENTE) {noun['text']} {indirect}"
        return _whole_sentence(
            self.group,
            exercise_id,
            query,
            [expected],
            {"verb": verb, "noun": noun, "indirect_object": indirect, "direct_pronoun": direct},
        )


class PronomeDirettoPassatoProssimo(ExerciseGenerator):
    group = ExerciseGroup(
        id="pronome_diretto_passato_prossimo",
        title="Pronome Diretto PASSATO PROSSIMO",
        description="Conjugate the verb, and use the pronome indiretto. Write the whole sentence.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        verb = rng.choice(TRANSITIVE_VERBS)
        noun = rng.choice(NOUNS)
        indirect = rng.choice(INDIRECT_OBJECTS)
        subject = "Io"
        direct = grammar.direct_pronoun_for_noun(noun)
        combined = grammar.elide_combined_pronoun_before_ho(indirect, direct)
        participle = grammar.agree_past_participle(past_participle(verb), direct)
        expected = _join_elided(combined.capitalize(), conjugate("avere", "presente", subject), participle)
        query = f"{subject} ({verb} PASSATO PROSSIMO) {noun['text']} {indirect}"
        return _whole_sentence(
            self.group,
            exercise_id,
            query,
            [expected],
            {
                "verb": verb,
                "noun": noun,
                "indirect_object": indirect,
                "direct_pronoun": direct,
                "participle": participle,
            },
        )


class PronomeDirettoPresenteModale(ExerciseGenerator):
    group = ExerciseGroup(
        id="pronome_diretto_presente_modale",
        title="Pronome Diretto PRESENTE con dovere/potere/volere",
        description="Conjugate the modal verb, and attach the pronouns to the infinitive. Write the whole sentence.",
    )

    def generate(self, exercise_id: str, rng: random.Random) -> StoredExercise:
        modal = rng.choice(MODAL_VERBS)
        verb = rng.choice(TRANSITIVE_VERBS)
        noun = rng.choice(NOUNS)
        indirect = rng.choice(INDIRECT_OBJECTS)
        subject = "Io"
        direct = grammar.direct_pronoun_for_noun(noun)
        combined = grammar.combined_indirect_direct_pronoun(indirect, direct)
        attached = grammar.attach_pronouns_to_infinitive(verb, combined)
        expected = f"{conjugate(modal, 'presente', subject).capitalize()} {attached}"
        query = f"{subject} ({modal} + {verb} PRESENTE) {noun['text']} {indirect}"
        return _whole_sentence(
            self.group,
            exercise_id,
            query,
            [expected],
            {"modal": modal, "verb": verb, "noun": noun, "indirect_object": indirect, "direct_pronoun": direct},
        )


def _join_elided(pronouns: str, auxiliary: str, participle: str) -> str:
    if pronouns.endswith("'"):
        return f"{pronouns}{auxiliary} {participle}"
    return f"{pronouns} {auxiliary} {participle}"


def _whole_sentence(
    group: ExerciseGroup,
    exercise_id: str,
    query: str,
    expected_answers: list[str],
    metadata: dict,
) -> StoredExercise:
    return StoredExercise(
        exercise_id=exercise_id,
        group_id=group.id,
        title=group.title,
        description=group.description,
        query=query,
        answer_format=AnswerFormat.WHOLE_SENTENCE,
        metadata=metadata,
        expected_answers=expected_answers,
    )
