from ..strings import slugify


def test_string_is_lowercased_in_slug():
    assert slugify("LoremIpsum") == "loremipsum"


def test_string_spaces_are_replaced_with_dashes_in_slug():
    assert slugify("lorem ipsum") == "lorem-ipsum"


def test_repeated_string_spaces_are_replaced_with_single_dash_in_slug():
    assert slugify("lorem   ipsum") == "lorem-ipsum"


def test_string_diacritics_are_removed_from_slug():
    assert slugify("łóręm") == "lorem"


def test_special_signs_are_removed_from_slug():
    assert slugify("us!er") == "user"
