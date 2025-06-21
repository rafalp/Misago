import pytest

from ..dicts import set_after_key, set_before_key


def test_set_after_key_sets_key_after_specified_one():
    src_dict = {"a": 1, "b": 2, "c": 3}

    new_dict = set_after_key(src_dict, "b", "z", 4)
    assert new_dict == {"a": 1, "b": 2, "z": 4, "c": 3}
    assert src_dict == {"a": 1, "b": 2, "c": 3}


def test_set_after_key_raises_key_error_for_invalid_after_argument():
    src_dict = {"a": 1, "b": 2, "c": 3}

    with pytest.raises(KeyError) as exc_info:
        set_after_key(src_dict, "d", "z", 4)

    assert str(exc_info.value) == "'d'"


def test_set_before_key_sets_key_before_specified_one():
    src_dict = {"a": 1, "b": 2, "c": 3}

    new_dict = set_before_key(src_dict, "b", "z", 4)
    assert new_dict == {"a": 1, "z": 4, "b": 2, "c": 3}
    assert src_dict == {"a": 1, "b": 2, "c": 3}


def test_set_before_key_raises_key_error_for_invalid_before_argument():
    src_dict = {"a": 1, "b": 2, "c": 3}

    with pytest.raises(KeyError) as exc_info:
        set_before_key(src_dict, "d", "z", 4)

    assert str(exc_info.value) == "'d'"
