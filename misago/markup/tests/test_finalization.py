from ..finalize import finalize_markup


def test_finalization_sets_translation_strings_in_quotes(snapshot):
    test_text = '<div class="quote-heading"></div>'
    finalized_text = finalize_markup(test_text)
    snapshot.assert_match(finalized_text)


def test_finalization_sets_translation_strings_in_spoilers_buttons(snapshot):
    test_text = '<button class="spoiler-reveal" type="button"></button>'
    finalized_text = finalize_markup(test_text)
    snapshot.assert_match(finalized_text)
