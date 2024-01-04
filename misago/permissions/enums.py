from enum import StrEnum


class CategoryPermission(StrEnum):
    SEE = "see"
    BROWSE = "browse"
    START = "start"
    REPLY = "reply"
    ATTACHMENTS = "attachments"
