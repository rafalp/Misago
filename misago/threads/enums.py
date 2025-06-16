from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2


class ThreadsListsPolling(IntEnum):
    DISABLED = 0
    ENABLED_FOR_USERS = 1
    ENABLED = 2

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.ENABLED,
                pgettext_lazy(
                    "threads lists polling choice",
                    "Enable for both signed-in users and guests",
                ),
            ),
            (
                cls.ENABLED_FOR_USERS,
                pgettext_lazy(
                    "category lists polling choice", "Enable for signed-in users"
                ),
            ),
            (
                cls.DISABLED,
                pgettext_lazy("category lists polling choice", "Disable"),
            ),
        )


class ThreadUpdateActionName(StrEnum):
    APPROVED = "approved"

    PINNED_GLOBALLY = "pinned_globally"
    PINNED_IN_CATEGORY = "pinned_in_category"
    UNPINNED = "unpinned"

    LOCKED = "locked"
    OPENED = "opened"

    MOVED = "moved"

    MERGED = "merged"
    SPLIT = "split"

    HID = "hid"
    UNHID = "unhid"

    CHANGED_TITLE = "changed_title"

    TOOK_OWNERSHIP = "took_ownership"
    CHANGED_OWNER = "changed_owner"

    JOINED = "joined"
    LEFT = "left"

    INVITED_PARTICIPANT = "invited_participant"
    REMOVED_PARTICIPANT = "removed_participant"
