import pytest

from ..dicts import set_key_after, set_key_before


def test_set_key_after_sets_key_after_specified_one():
    src_dict = {"a": 1, "b": 2, "c": 3}

    new_dict = set_key_after(src_dict, "b", "z", 4)
    assert new_dict == {"a": 1, "b": 2, "z": 4, "c": 3}
    assert src_dict == {"a": 1, "b": 2, "c": 3}


def test_set_key_after_raises_key_error_for_invalid_after_argument():
    src_dict = {"a": 1, "b": 2, "c": 3}

    with pytest.raises(KeyError) as exc_info:
        set_key_after(src_dict, "d", "z", 4)

    assert str(exc_info.value) == "'d'"


def test_set_key_before_sets_key_before_specified_one():
    src_dict = {"a": 1, "b": 2, "c": 3}

    new_dict = set_key_before(src_dict, "b", "z", 4)
    assert new_dict == {"a": 1, "z": 4, "b": 2, "c": 3}
    assert src_dict == {"a": 1, "b": 2, "c": 3}


def test_set_key_before_raises_key_error_for_invalid_before_argument():
    src_dict = {"a": 1, "b": 2, "c": 3}

    with pytest.raises(KeyError) as exc_info:
        set_key_before(src_dict, "d", "z", 4)

    assert str(exc_info.value) == "'d'"
