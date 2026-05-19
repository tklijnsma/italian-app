from app.grammar import api as grammar


def test_grammar_api_import_surface():
    expected_functions = [
        "normalize_answer",
        "direct_pronoun_for_noun",
        "combined_indirect_direct_pronoun",
        "attach_pronouns_to_infinitive",
        "agree_past_participle",
        "reflexive_pronoun",
        "contract_preposition",
    ]
    for function_name in expected_functions:
        assert callable(getattr(grammar, function_name))


def test_answer_normalization():
    assert grammar.normalize_answer("  Te   l’ho   INVIATA. ") == "te l'ho inviata"


def test_direct_pronoun_mapping():
    assert grammar.direct_pronoun_for_noun({"gender": "masculine", "number": "singular"}) == "lo"
    assert grammar.direct_pronoun_for_noun({"gender": "feminine", "number": "singular"}) == "la"
    assert grammar.direct_pronoun_for_noun({"gender": "masculine", "number": "plural"}) == "li"
    assert grammar.direct_pronoun_for_noun({"gender": "feminine", "number": "plural"}) == "le"


def test_combined_pronouns_and_infinitive_attachment():
    assert grammar.combined_indirect_direct_pronoun("a te", "lo") == "te lo"
    assert grammar.elide_combined_pronoun_before_ho("a te", "la") == "te l'"
    assert grammar.combined_indirect_direct_pronoun("a lui", "la") == "gliela"
    assert grammar.combined_indirect_direct_pronoun("a noi", "lo") == "ce lo"
    assert grammar.attach_pronouns_to_infinitive("inviare", "te lo") == "inviartelo"
    assert grammar.attach_pronouns_to_infinitive("dare", "gliela") == "dargliela"


def test_agreement_reflexive_pronouns_and_prepositions():
    assert grammar.agree_past_participle("inviato", "la") == "inviata"
    assert grammar.agree_past_participle("inviato", "li") == "inviati"
    assert grammar.agree_past_participle("inviato", "le") == "inviate"
    assert grammar.reflexive_pronoun("io") == "mi"
    assert grammar.reflexive_pronoun("tu") == "ti"
    assert grammar.reflexive_pronoun("loro") == "si"
    assert grammar.contract_preposition("su", "il") == "sul"
    assert grammar.contract_preposition("a", "la") == "alla"
    assert grammar.contract_preposition("in", "il") == "nel"
