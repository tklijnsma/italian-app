from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AnswerFormat(str, Enum):
    WHOLE_SENTENCE = "whole_sentence"
    ONLY_WORDS = "only_words"
    ONLY_PREPOSITION = "only_preposition"


class ExerciseGroup(BaseModel):
    id: str
    title: str
    description: str


class GenerateExerciseRequest(BaseModel):
    group_id: str
    seed: int | None = None


class CheckExerciseRequest(BaseModel):
    exercise_id: str
    answer: str


class GeneratedExercise(BaseModel):
    exercise_id: str
    group_id: str
    title: str
    description: str
    query: str
    answer_format: AnswerFormat
    metadata: dict[str, Any] = Field(default_factory=dict)


class StoredExercise(GeneratedExercise):
    expected_answers: list[str]
    hint_rules: dict[str, Any] = Field(default_factory=dict)


class CheckExerciseResponse(BaseModel):
    correct: bool
    expected_answers: list[str]
    normalized_answer: str
    hint: str | None = None


class ExerciseGenerator:
    group: ExerciseGroup

    def generate(self, exercise_id: str, rng) -> StoredExercise:
        raise NotImplementedError
