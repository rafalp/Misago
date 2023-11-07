from ..finalize import finalize_markup


def test_finalization_sets_translation_strings_in_empty_quotes_headings(snapshot):
    test_text = '<div class="quote-heading" data-noquote="1">Lorem ipsum</div>'
    finalized_text = finalize_markup(test_text)
    assert snapshot == finalized_text


def test_finalization_sets_translation_strings_in_empty_quotes_headings(snapshot):
    test_text = '<div class="quote-heading" data-noquote="1"></div>'
    finalized_text = finalize_markup(test_text)
    assert snapshot == finalized_text


def test_finalization_sets_translation_strings_in_spoilers_buttons(snapshot):
    test_text = '<button class="spoiler-reveal" type="button"></button>'
    finalized_text = finalize_markup(test_text)
    assert snapshot == finalized_text
