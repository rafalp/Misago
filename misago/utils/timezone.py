from datetime import datetime

import pytz


def now() -> datetime:
    return datetime.utcnow().replace(tzinfo=pytz.utc)
