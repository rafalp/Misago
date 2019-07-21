from ..finalize import finalize_markup


def test_finalization_sets_translation_strings_in_quotes(snapshot):
    test_text = '<div class="quote-heading"></div>'
    finalized_text = finalize_markup(test_text)
    snapshot.assert_match(finalized_text)
