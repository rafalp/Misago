from enum import StrEnum


class CacheName(StrEnum):
    BANS = "bans"
    CATEGORIES = "categories"
    GROUPS = "groups"
    MODERATORS = "moderators"
    PERMISSIONS = "permissions"
    SETTINGS = "settings"
