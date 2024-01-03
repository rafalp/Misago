from enum import StrEnum


class CategoryPermission(StrEnum):
    SEE = "see"
    READ = "read"
    START = "start"
    REPLY = "reply"
    ATTACHMENTS = "attachments"
