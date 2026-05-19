from typing import Literal


DirectPronoun = Literal["lo", "la", "li", "le"]

_DIRECT_PRONOUNS: dict[tuple[str, str], DirectPronoun] = {
    ("masculine", "singular"): "lo",
    ("feminine", "singular"): "la",
    ("masculine", "plural"): "li",
    ("feminine", "plural"): "le",
}

_COMBINED_PRONOUNS: dict[str, dict[DirectPronoun, str]] = {
    "a me": {"lo": "me lo", "la": "me la", "li": "me li", "le": "me le"},
    "a te": {"lo": "te lo", "la": "te la", "li": "te li", "le": "te le"},
    "a lui": {"lo": "glielo", "la": "gliela", "li": "glieli", "le": "gliele"},
    "a lei": {"lo": "glielo", "la": "gliela", "li": "glieli", "le": "gliele"},
    "a noi": {"lo": "ce lo", "la": "ce la", "li": "ce li", "le": "ce le"},
    "a voi": {"lo": "ve lo", "la": "ve la", "li": "ve li", "le": "ve le"},
    "a loro": {"lo": "glielo", "la": "gliela", "li": "glieli", "le": "gliele"},
}

_REFLEXIVE_PRONOUNS = {
    "io": "mi",
    "tu": "ti",
    "lui": "si",
    "lei": "si",
    "noi": "ci",
    "voi": "vi",
    "loro": "si",
}


def direct_pronoun_for_noun(noun: dict[str, str]) -> DirectPronoun:
    return _DIRECT_PRONOUNS[(noun["gender"], noun["number"])]


def combined_indirect_direct_pronoun(indirect_phrase: str, direct_pronoun: DirectPronoun) -> str:
    return _COMBINED_PRONOUNS[indirect_phrase][direct_pronoun]


def elide_combined_pronoun_before_ho(indirect_phrase: str, direct_pronoun: DirectPronoun) -> str:
    combined = combined_indirect_direct_pronoun(indirect_phrase, direct_pronoun)
    if direct_pronoun in {"lo", "la"}:
        if combined.endswith(f" {direct_pronoun}"):
            return combined[: -len(direct_pronoun)] + "l'"
        if combined.endswith(direct_pronoun):
            return combined[: -len(direct_pronoun)] + "l'"
    return combined


def attach_pronouns_to_infinitive(infinitive: str, combined_pronoun: str) -> str:
    if not infinitive.endswith("e"):
        raise ValueError(f"Unsupported infinitive: {infinitive}")
    return infinitive[:-1] + combined_pronoun.replace(" ", "")


def reflexive_pronoun(subject: str) -> str:
    return _REFLEXIVE_PRONOUNS[subject.lower()]
