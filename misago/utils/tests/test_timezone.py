from ..timezone import now


def test_now_returns_tz_aware_datetime_with_utc_timezone():
    value = now()
    assert value.utcoffset() is not None
    assert value.utcoffset().seconds == 0
