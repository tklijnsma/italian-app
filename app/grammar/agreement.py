from app.grammar.pronouns import DirectPronoun


def agree_past_participle(participle: str, pronoun: DirectPronoun) -> str:
    if not participle.endswith("o"):
        return participle
    stem = participle[:-1]
    endings = {
        "lo": "o",
        "la": "a",
        "li": "i",
        "le": "e",
    }
    return stem + endings[pronoun]
