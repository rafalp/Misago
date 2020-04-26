from ..strings import parse_db_id


def test_valid_int_str_is_parsed_to_int():
    assert parse_db_id("1") == 1


def test_invalid_int_string_is_parsed_to_none():
    assert parse_db_id("abc") is None


def test_valid_int_zero_str_is_parsed_to_none():
    assert parse_db_id("0") is None


def test_valid_negative_int_str_is_parseed_to_none():
    assert parse_db_id("-1") is None
