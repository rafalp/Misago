from ..strings import get_random_string


def test_random_string_can_be_created():
    assert get_random_string()


def test_random_string_length_can_be_specified():
    string = get_random_string(8)
    assert len(string) == 8


def test_random_string_contents_can_be_specified():
    string = get_random_string(8, allowed_chars="ab")
    assert "a" in string or "b" in string
    assert string.count("a") + string.count("b") == 8
