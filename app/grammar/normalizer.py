import re


_SPACE_RE = re.compile(r"\s+")


def normalize_answer(answer: str) -> str:
    normalized = answer.strip().replace("’", "'").replace("‘", "'").lower()
    normalized = _SPACE_RE.sub(" ", normalized)
    if normalized.endswith("."):
        normalized = normalized[:-1].rstrip()
    return normalized
