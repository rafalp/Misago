from enum import IntEnum

CUSTOM_GROUP_ID_START = 100


class DefaultGroupId(IntEnum):
    ADMINS = 1
    MODERATORS = 2
    MEMBERS = 3
    GUESTS = 4
