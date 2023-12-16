from ..client import get_value_from_json


def test_json_str_value_is_returned():
    assert get_value_from_json("val", {"val": "ok", "val2": "nope"}) == "ok"


def test_json_str_value_has_stripped_whitespace():
    assert get_value_from_json("val", {"val": "  ok  ", "val2": "nope"}) == "ok"


def test_json_int_value_is_cast_to_str():
    assert get_value_from_json("val", {"val": 21, "val2": "nope"}) == "21"


def test_none_is_returned_if_val_is_not_found():
    assert get_value_from_json("val", {"val3": 21, "val2": "nope"}) is None


def test_none_is_returned_if_val_is_null():
    assert get_value_from_json("val", {"val": None, "val2": "nope"}) is None


def test_json_value_is_returned_from_nested_object():
    assert (
        get_value_from_json(
            "val.child.val",
            {
                "val2": "nope",
                "val": {
                    "child": {
                        "val2": "nope",
                        "val": "ok",
                    },
                },
            },
        )
        == "ok"
    )


def test_none_is_returned_from_nested_object_missing_value():
    assert (
        get_value_from_json(
            "val.child.val3",
            {
                "val2": "nope",
                "val": {
                    "child": {
                        "val2": "nope",
                        "val": "ok",
                    },
                },
            },
        )
        is None
    )


def test_json_value_returned_from_nested_object_is_str():
    assert (
        get_value_from_json(
            "val.child.val",
            {
                "val2": "nope",
                "val": {
                    "child": {
                        "val2": "nope",
                        "val": 21,
                    },
                },
            },
        )
        == "21"
    )


def test_none_is_returned_from_nested_object_missing_path_item():
    assert (
        get_value_from_json(
            "val.missing.val",
            {
                "val2": "nope",
                "val": {
                    "child": {
                        "val2": "nope",
                        "val": 21,
                    },
                },
            },
        )
        is None
    )


def test_none_is_returned_from_nested_path_item_not_being_dict():
    assert (
        get_value_from_json(
            "val.child.val",
            {
                "val2": "nope",
                "val": {
                    "child": "nope",
                },
            },
        )
        is None
    )
