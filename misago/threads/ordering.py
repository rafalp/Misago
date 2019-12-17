from datetime import datetime


def get_ordering(last_posted_at: datetime) -> int:
    return int(last_posted_at.timestamp() * 1000)
