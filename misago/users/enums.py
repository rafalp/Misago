from enum import IntEnum

from django.utils.translation import pgettext_lazy


CUSTOM_GROUP_ID_START = 100


class DefaultGroupId(IntEnum):
    ADMINS = 1
    MODERATORS = 2
    MEMBERS = 3
    GUESTS = 4


class UserNewPrivateThreadsPreference(IntEnum):
    EVERYBODY = 0
    FOLLOWED_USERS = 1
    NOBODY = 2

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.EVERYBODY.value,
                pgettext_lazy("new private threads preference", "Everybody"),
            ),
            (
                cls.FOLLOWED_USERS.value,
                pgettext_lazy("new private threads preference", "Users I follow"),
            ),
            (
                cls.NOBODY.value,
                pgettext_lazy("new private threads preference", "Nobody"),
            ),
        )
