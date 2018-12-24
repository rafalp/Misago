from .. import algebra


def test_greatest_value_is_returned():
    assert algebra.greater(1, 3) == 3
    assert algebra.greater(4, 2) == 4
    assert algebra.greater(2, 2) == 2
    assert algebra.greater(True, False) is True


def test_greatest_or_zero_value_is_returned():
    assert algebra.greater_or_zero(1, 3) == 3
    assert algebra.greater_or_zero(4, 2) == 4
    assert algebra.greater_or_zero(2, 2) == 2
    assert algebra.greater_or_zero(True, False) is False
    assert algebra.greater_or_zero(2, 0) == 0
    assert algebra.greater_or_zero(0, 0) == 0
    assert algebra.greater_or_zero(0, 120) == 0


def test_lower_value_is_returned():
    assert algebra.lower(1, 3) == 1
    assert algebra.lower(4, 2) == 2
    assert algebra.lower(2, 2) == 2
    assert algebra.lower(True, False) is False


def test_lowest_non_zero_value_is_returned():
    assert algebra.lower_non_zero(1, 3) == 1
    assert algebra.lower_non_zero(0, 2) == 2
    assert algebra.lower_non_zero(1, 2) == 1
    assert algebra.lower_non_zero(0, 0) == 0


def test_acls_are_be_added_together():
    test_acls = [
        {
            "can_see": 0,
            "can_hear": 0,
            "max_speed": 10,
            "min_age": 16,
            "speed_limit": 50,
        },
        {"can_see": 1, "can_hear": 0, "max_speed": 40, "min_age": 20, "speed_limit": 0},
        {
            "can_see": 0,
            "can_hear": 1,
            "max_speed": 80,
            "min_age": 18,
            "speed_limit": 40,
        },
    ]

    defaults = {
        "can_see": 0,
        "can_hear": 0,
        "max_speed": 30,
        "min_age": 18,
        "speed_limit": 60,
    }

    acl = algebra.sum_acls(
        defaults,
        acls=test_acls,
        can_see=algebra.greater,
        can_hear=algebra.greater,
        max_speed=algebra.greater,
        min_age=algebra.lower,
        speed_limit=algebra.greater_or_zero,
    )

    assert acl["can_see"] == 1
    assert acl["can_hear"] == 1
    assert acl["max_speed"] == 80
    assert acl["min_age"] == 16
    assert acl["speed_limit"] == 0
