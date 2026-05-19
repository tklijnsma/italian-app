from functools import lru_cache

import mlconjug3


_PERSON_KEYS = {
    "io": "io",
    "tu": "tu",
    "lui": "egli/ella",
    "lei": "egli/ella",
    "noi": "noi",
    "voi": "voi",
    "loro": "essi/esse",
}

_TENSE_PATHS = {
    "presente": ("Indicativo", "Indicativo presente"),
    "congiuntivo_presente": ("Congiuntivo", "Congiuntivo presente"),
    "congiuntivo_imperfetto": ("Congiuntivo", "Congiuntivo imperfetto"),
    "condizionale_presente": ("Condizionale", "Condizionale presente"),
}


@lru_cache(maxsize=1)
def _conjugator():
    return mlconjug3.Conjugator(language="it")


@lru_cache(maxsize=256)
def _conjugated(verb: str):
    return _conjugator().conjugate(verb)


def conjugate(verb: str, tense: str, subject: str) -> str:
    mood, tense_name = _TENSE_PATHS[tense]
    person = _PERSON_KEYS[subject.lower()]
    value = _conjugated(verb).conjug_info[mood][tense_name][person]
    return _first_variant(value)


def past_participle(verb: str) -> str:
    value = _conjugated(verb).conjug_info["Participio"]["Participio Participio"][1]
    return _first_variant(value)


def _first_variant(value: str) -> str:
    return value.replace("’", "'").replace("‘", "'").split("/")[0]
