from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.exercises.checking import check_answer
from app.exercises.models import CheckExerciseRequest, CheckExerciseResponse, GenerateExerciseRequest, GeneratedExercise
from app.exercises.registry import GENERATORS_BY_GROUP_ID, exercise_groups, generate_exercise


router = APIRouter()
EXERCISE_STORE = {}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/exercise-groups")
def get_exercise_groups():
    return exercise_groups()


@router.post("/exercises/generate", response_model=GeneratedExercise)
def post_generate_exercise(request: GenerateExerciseRequest):
    if request.group_id not in GENERATORS_BY_GROUP_ID:
        raise HTTPException(status_code=404, detail="Unknown exercise group")
    exercise = generate_exercise(request.group_id, request.seed)
    EXERCISE_STORE[exercise.exercise_id] = exercise
    return exercise


@router.post("/exercises/check", response_model=CheckExerciseResponse)
def post_check_exercise(request: CheckExerciseRequest):
    exercise = EXERCISE_STORE.get(request.exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Unknown exercise")

    return check_answer(exercise, request.answer)
