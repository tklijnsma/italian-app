from pathlib import Path

from app.exercises.pronome_diretto import (
    PronomeDirettoPassatoProssimo,
    PronomeDirettoPresente,
    PronomeDirettoPresenteModale,
)
from app.exercises.registry import EXERCISE_GENERATORS, GENERATORS_BY_GROUP_ID, generate_exercise


EXPECTED_GROUP_IDS = {
    "pronome_diretto_presente",
    "pronome_diretto_passato_prossimo",
    "pronome_diretto_presente_modale",
    "congiuntivo_presente",
    "periodo_ipotetico_congiuntivo_imperfetto_condizionale",
    "riflessivo_presente",
    "preposizione",
}


def test_every_exercise_group_is_registered():
    assert {generator.group.id for generator in EXERCISE_GENERATORS} == EXPECTED_GROUP_IDS
    assert set(GENERATORS_BY_GROUP_ID) == EXPECTED_GROUP_IDS


def test_pronome_diretto_module_exposes_all_three_generators():
    assert PronomeDirettoPresente.group.id == "pronome_diretto_presente"
    assert PronomeDirettoPassatoProssimo.group.id == "pronome_diretto_passato_prossimo"
    assert PronomeDirettoPresenteModale.group.id == "pronome_diretto_presente_modale"


def test_registry_is_explicit_not_auto_discovered():
    registry_source = Path("app/exercises/registry.py").read_text()
    assert "EXERCISE_GENERATORS" in registry_source
    assert "pkgutil" not in registry_source
    assert "importlib" not in registry_source


def test_no_global_verbs_or_nouns_json_remains():
    assert not Path("app/data/verbs.json").exists()
    assert not Path("app/data/nouns.json").exists()


def test_each_generator_produces_valid_exercise_with_real_mlconjug3():
    for group_id in EXPECTED_GROUP_IDS:
        exercise = generate_exercise(group_id, seed=1)
        assert exercise.query
        assert exercise.expected_answers
        assert exercise.metadata
        assert exercise.group_id == group_id
