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


def test_slug_is_trimmed_to_255_characters():
    assert slugify("a" * 256) == "a" * 255


def test_slug_trimming_length_can_be_customized():
    assert slugify("a" * 100, 5) == "a" * 5


def test_slug_trimming_length_can_be_disabled():
    assert slugify("a" * 256, None) == "a" * 256


def test_slug_is_stripped_dangling_hashes():
    assert slugify("-test-") == "test"
