from fastapi.testclient import TestClient

from app.api.routes import EXERCISE_STORE
from app.exercises.models import AnswerFormat, StoredExercise
from app.exercises.registry import GENERATORS_BY_GROUP_ID
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_exercise_groups_returns_all_groups():
    response = client.get("/exercise-groups")
    assert response.status_code == 200
    groups = response.json()
    assert len(groups) == 7
    assert {group["id"] for group in groups} == set(GENERATORS_BY_GROUP_ID)


def test_cors_allows_github_pages_frontend():
    response = client.options(
        "/health",
        headers={
            "Origin": "https://italian-app.github.io",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://italian-app.github.io"


def test_generate_endpoint_works_for_all_groups():
    for group_id in GENERATORS_BY_GROUP_ID:
        response = client.post("/exercises/generate", json={"group_id": group_id, "seed": 1})
        assert response.status_code == 200
        payload = response.json()
        assert payload["exercise_id"]
        assert payload["group_id"] == group_id
        assert payload["query"]


def test_check_endpoint_marks_listed_examples_correct():
    examples = [
        ("pronome_diretto_presente", "Io (inviare PRESENTE) un messaggio a te", "Te lo invio"),
        ("pronome_diretto_passato_prossimo", "Io (inviare PASSATO PROSSIMO) una pizza a te", "Te l'ho inviata"),
        ("pronome_diretto_presente_modale", "Io (volere + inviare PRESENTE) un messaggio a te", "Voglio inviartelo"),
        ("pronome_diretto_presente_modale", "Io (potere + dare PRESENTE) una pizza a lui", "Posso dargliela"),
        ("congiuntivo_presente", "Credo che tu (prendere) una pizza", "prenda"),
        (
            "periodo_ipotetico_congiuntivo_imperfetto_condizionale",
            "Se mia nonna (avere) le ruote, (essere) una cariola",
            "avesse sarebbe",
        ),
        ("riflessivo_presente", "Io (lavare a me) le mani", "Io mi lavo le mani"),
        ("preposizione", "Metto il bicchiere ____ tavolo", "sul"),
    ]

    for index, (group_id, query, answer) in enumerate(examples):
        exercise_id = f"example-{index}"
        EXERCISE_STORE[exercise_id] = StoredExercise(
            exercise_id=exercise_id,
            group_id=group_id,
            title="Example",
            description="Example",
            query=query,
            answer_format=AnswerFormat.WHOLE_SENTENCE,
            metadata={},
            expected_answers=[answer],
        )
        response = client.post("/exercises/check", json={"exercise_id": exercise_id, "answer": answer})
        assert response.status_code == 200
        assert response.json()["correct"] is True


def test_check_endpoint_is_case_insensitive_and_space_tolerant():
    exercise_id = "normalization-example"
    EXERCISE_STORE[exercise_id] = StoredExercise(
        exercise_id=exercise_id,
        group_id="preposizione",
        title="Example",
        description="Example",
        query="Metto il bicchiere ____ tavolo",
        answer_format=AnswerFormat.ONLY_PREPOSITION,
        metadata={},
        expected_answers=["sul"],
    )

    response = client.post("/exercises/check", json={"exercise_id": exercise_id, "answer": "  SUL  ."})
    assert response.status_code == 200
    assert response.json()["correct"] is True
