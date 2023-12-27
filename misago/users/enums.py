from enum import IntEnum

DEFAULT_GROUPS_IDS = 100


class DefaultGroupId(IntEnum):
    ADMINS = 1
    MODERATORS = 2
    MEMBERS = 3
    GUESTS = 4
