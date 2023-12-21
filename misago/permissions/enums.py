from enum import StrEnum


class CategoryPermission(StrEnum):
    SEE = "SEE"
    READ = "READ"
    START = "START"
    REPLY = "REPLY"
    ATTACHMENTS = "ATTACHMENTS"
