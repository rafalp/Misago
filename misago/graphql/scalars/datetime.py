from datetime import datetime
from ariadne import ScalarType


datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime) -> str:
    serializer = value.isoformat()
    return serializer
