from datetime import datetime

from ..ordering import get_ordering


def test_ordering_is_number_of_miliseconds_since_epoch():
    test_datetime = datetime.utcnow()
    assert get_ordering(test_datetime) == int(test_datetime.timestamp() * 1000)
