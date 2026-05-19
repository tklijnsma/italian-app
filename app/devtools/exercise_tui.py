import argparse
import random
import sys

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Static

from app.exercises.checking import check_answer
from app.exercises.models import CheckExerciseResponse, StoredExercise
from app.exercises.registry import GENERATORS_BY_GROUP_ID, generate_exercise


def parse_group_ids(raw_groups: str | None) -> list[str]:
    if raw_groups is None or not raw_groups.strip():
        return list(GENERATORS_BY_GROUP_ID)

    group_ids = [group_id.strip() for group_id in raw_groups.split(",") if group_id.strip()]
    invalid = [group_id for group_id in group_ids if group_id not in GENERATORS_BY_GROUP_ID]
    if invalid:
        available = ", ".join(GENERATORS_BY_GROUP_ID)
        raise ValueError(f"Unknown exercise group(s): {', '.join(invalid)}. Available groups: {available}")
    return group_ids


def random_exercise(group_ids: list[str], rng: random.Random) -> StoredExercise:
    group_id = rng.choice(group_ids)
    return generate_exercise(group_id, seed=rng.randrange(1_000_000_000))


def check_exercise_answer(exercise: StoredExercise, answer: str) -> CheckExerciseResponse:
    return check_answer(exercise, answer)


class ExerciseTui(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #groups, #exercise, #feedback {
        border: solid $accent;
        padding: 1;
        margin: 1;
    }

    #answer {
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("n", "next_exercise", "Next"),
        ("a", "show_answer", "Show answer"),
    ]

    def __init__(self, group_ids: list[str]) -> None:
        super().__init__()
        self.group_ids = group_ids
        self.rng = random.Random()
        self.current_exercise: StoredExercise | None = None
        self.answer_checked = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("", id="groups")
        yield Static("", id="exercise")
        yield Input(placeholder="Type your answer and press Enter", id="answer")
        yield Static("", id="feedback")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#groups", Static).update("Active groups: " + ", ".join(self.group_ids))
        self.load_next_exercise()
        self.query_one("#answer", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.answer_checked:
            self.load_next_exercise()
            return
        self.submit_answer(event.value)

    def action_next_exercise(self) -> None:
        self.load_next_exercise()

    def action_show_answer(self) -> None:
        if self.current_exercise is None:
            return
        expected = "\n".join(f"- {answer}" for answer in self.current_exercise.expected_answers)
        self.query_one("#feedback", Static).update(f"Expected answers:\n{expected}")
        self.answer_checked = True

    def load_next_exercise(self) -> None:
        self.current_exercise = random_exercise(self.group_ids, self.rng)
        self.answer_checked = False
        self.query_one("#exercise", Static).update(_exercise_text(self.current_exercise))
        self.query_one("#feedback", Static).update("Feedback will appear here.")
        answer_input = self.query_one("#answer", Input)
        answer_input.value = ""
        answer_input.focus()

    def submit_answer(self, answer: str) -> None:
        if self.current_exercise is None:
            return
        result = check_exercise_answer(self.current_exercise, answer)
        status = "Correct" if result.correct else "Incorrect"
        expected = "\n".join(f"- {answer}" for answer in result.expected_answers)
        hint = f"\nHint: {result.hint}" if result.hint else ""
        self.query_one("#feedback", Static).update(
            f"{status}\n\nExpected answers:\n{expected}\n\nNormalized answer: {result.normalized_answer}{hint}\n\nPress Enter for next exercise."
        )
        self.answer_checked = True


def _exercise_text(exercise: StoredExercise) -> str:
    return (
        f"{exercise.title}\n\n"
        f"{exercise.description}\n\n"
        f"Query: {exercise.query}\n"
        f"Answer format: {exercise.answer_format.value}"
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Internal terminal UI for testing Italian grammar exercises.")
    parser.add_argument(
        "--groups",
        help="Comma-separated exercise group IDs to enable. Defaults to all registered groups.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        group_ids = parse_group_ids(args.groups)
    except ValueError as exc:
        parser.error(str(exc))
    ExerciseTui(group_ids).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
