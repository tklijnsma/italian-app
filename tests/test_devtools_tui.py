import random
from pathlib import Path

import pytest

from app.exercises.registry import GENERATORS_BY_GROUP_ID


def test_textual_is_not_imported_by_normal_api_modules():
    normal_paths = [
        *Path("app/api").glob("*.py"),
        *Path("app/grammar").glob("*.py"),
        *Path("app/exercises").glob("*.py"),
        Path("app/main.py"),
    ]
    for path in normal_paths:
        assert "textual" not in path.read_text()


def test_dev_tool_module_imports_when_textual_is_installed():
    import app.devtools.exercise_tui as exercise_tui

    assert exercise_tui.ExerciseTui is not None


def test_tui_compose_is_compatible_with_installed_textual_version():
    from app.devtools.exercise_tui import ExerciseTui

    widgets = list(ExerciseTui(["preposizione"]).compose())
    assert len(widgets) == 6


def test_parse_group_ids_defaults_to_all_groups():
    from app.devtools.exercise_tui import parse_group_ids

    assert parse_group_ids(None) == list(GENERATORS_BY_GROUP_ID)
    assert parse_group_ids("") == list(GENERATORS_BY_GROUP_ID)


def test_parse_group_ids_accepts_valid_comma_separated_groups():
    from app.devtools.exercise_tui import parse_group_ids

    assert parse_group_ids("preposizione, congiuntivo_presente") == [
        "preposizione",
        "congiuntivo_presente",
    ]


def test_parse_group_ids_rejects_invalid_groups_with_clear_error():
    from app.devtools.exercise_tui import parse_group_ids

    with pytest.raises(ValueError, match="Unknown exercise group"):
        parse_group_ids("preposizione,missing_group")


def test_tui_helper_generates_exercise_from_each_selected_group():
    from app.devtools.exercise_tui import random_exercise

    for group_id in GENERATORS_BY_GROUP_ID:
        exercise = random_exercise([group_id], random.Random(1))
        assert exercise.group_id == group_id
        assert exercise.query
        assert exercise.expected_answers
