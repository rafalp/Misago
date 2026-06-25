from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class CanSeePostEdits(IntEnum):
    HISTORY = 3
    COUNT = 2
    NO = 0
    NEVER = 1

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.HISTORY,
                pgettext_lazy(
                    "see post edits permission", "Counts and history of changes"
                ),
            ),
            (
                cls.COUNT,
                pgettext_lazy("see post edits permission", "Count only"),
            ),
            (cls.NO, pgettext_lazy("see post edits permission", "No")),
            (cls.NEVER, pgettext_lazy("see post edits permission", "Never")),
        )


class CanHideOwnPostEdits(IntEnum):
    NEVER = 1
    NO = 0
    HIDE = 2
    DELETE = 3

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.DELETE,
                pgettext_lazy("hide own post edits permission", "Hide and delete"),
            ),
            (
                cls.HIDE,
                pgettext_lazy("hide own post edits permission", "Hide only"),
            ),
            (cls.NEVER, pgettext_lazy("hide own post edits permission", "Never")),
            (cls.NO, pgettext_lazy("hide own post edits permission", "No")),
        )


class CanSeePostLikes(IntEnum):
    USERS = 3
    COUNT = 2
    NO = 0
    NEVER = 1

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.USERS,
                pgettext_lazy(
                    "see post likes permission", "Count and users who liked the post"
                ),
            ),
            (
                cls.COUNT,
                pgettext_lazy("see post likes permission", "Count only"),
            ),
            (cls.NEVER, pgettext_lazy("see post likes permission", "Never")),
            (cls.NO, pgettext_lazy("see post likes permission", "No")),
        )


class CanUploadAttachments(IntEnum):
    EVERYWHERE = 3
    THREADS = 2
    NO = 0
    NEVER = 1

    @classmethod
    def get_choices(cls):
        return (
            (
                cls.EVERYWHERE,
                pgettext_lazy(
                    "upload attachments permission", "In threads and private threads"
                ),
            ),
            (
                cls.THREADS,
                pgettext_lazy("upload attachments permission", "In threads only"),
            ),
            (cls.NEVER, pgettext_lazy("upload attachments permission", "Never")),
            (cls.NO, pgettext_lazy("upload attachments permission", "No")),
        )


class PermissionValue(IntEnum):
    YES = 1
    NO = 0
    NEVER = 2

    @classmethod
    def get_choices(cls):
        return (
            (cls.YES, pgettext_lazy("permission value", "Yes")),
            (cls.NO, pgettext_lazy("permission value", "No")),
            (cls.NEVER, pgettext_lazy("permission value", "Never")),
        )


class CategoryPermission(StrEnum):
    SEE = "see"
    BROWSE = "browse"
    START = "start"
    REPLY = "reply"
    ATTACHMENTS = "attachments"


class CategoryQueryContext(StrEnum):
    CURRENT = "current"
    CHILD = "child"
    OTHER = "other"


class CategoryThreadsQuery(StrEnum):
    ALL = "all"
    ALL_PINNED = "all_pinned"
    ALL_PINNED_EVERYWHERE = "all_pinned_everywhere"
    ALL_PINNED_CATEGORY = "all_pinned_in_category"
    ALL_NOT_PINNED = "all_not_pinned"
    ALL_NOT_PINNED_EVERYWHERE = "all_not_pinned_everywhere"

    ANON = "anon"
    ANON_PINNED = "anon_pinned"
    ANON_PINNED_EVERYWHERE = "anon_pinned_everywhere"
    ANON_PINNED_CATEGORY = "anon_pinned_in_category"
    ANON_NOT_PINNED = "anon_not_pinned"
    ANON_NOT_PINNED_EVERYWHERE = "anon_not_pinned_everywhere"

    USER = "user"
    USER_PINNED = "user_pinned"
    USER_PINNED_EVERYWHERE = "user_pinned_everywhere"
    USER_PINNED_CATEGORY = "user_pinned_in_category"
    USER_NOT_PINNED = "user_not_pinned"
    USER_NOT_PINNED_EVERYWHERE = "user_not_pinned_everywhere"

    USER_STARTED_PINNED = "user_started_pinned"
    USER_STARTED_PINNED_EVERYWHERE = "user_started_pinned_everywhere"
    USER_STARTED_PINNED_CATEGORY = "user_started_pinned_in_category"
    USER_STARTED_NOT_PINNED = "user_started_not_pinned"
