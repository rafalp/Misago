from enum import StrEnum


class NotificationTarget(StrEnum):
    USER = "USER"
    THREAD = "THREAD"
    POST = "POST"


class NotificationVerb(StrEnum):
    REPLIED = "REPLIED"
