import re
from datetime import datetime

from ....utils import timezone
from ..datetime import serialize_datetime


def test_datetime_scalar_serializes_utc_datetime_to_js_iso8601_str():
    value = datetime.utcnow()
    parsed_value = serialize_datetime(value)
    assert parsed_value == value.isoformat()[:23] + "Z"
    assert re.match(
        r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$",
        parsed_value,
    )


def test_datetime_scalar_serializes_tz_aware_utc_datetime_to_js_iso8601_str():
    value = timezone.now()
    parsed_value = serialize_datetime(value)
    assert parsed_value == value.isoformat()[:23] + "Z"
    assert re.match(
        r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$",
        parsed_value,
    )
