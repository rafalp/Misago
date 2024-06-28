from enum import StrEnum


class CategoryPermission(StrEnum):
    SEE = "see"
    BROWSE = "browse"
    START = "start"
    REPLY = "reply"
    ATTACHMENTS = "attachments"


class CategoryAccess(StrEnum):
    MODERATOR = "moderator"
    STARTED_ONLY = "started_only"
    DEFAULT = "default"
