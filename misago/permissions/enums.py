from enum import IntEnum, StrEnum

from django.utils.translation import pgettext_lazy


class CanSeePostEdits(IntEnum):
    HISTORY = 2
    COUNT = 1
    NEVER = 0

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
            (cls.NEVER, pgettext_lazy("see post edits permission", "Never")),
        )


class CanHideOwnPostEdits(IntEnum):
    NEVER = 0
    HIDE = 1
    DELETE = 2

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
        )


class CanSeePostLikes(IntEnum):
    USERS = 2
    COUNT = 1
    NEVER = 0

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
        )


class CanUploadAttachments(IntEnum):
    EVERYWHERE = 2
    THREADS = 1
    NEVER = 0

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
    ALL_PINNED_GLOBALLY = "all_pinned_globally"
    ALL_PINNED_IN_CATEGORY = "all_pinned_in_category"
    ALL_NOT_PINNED = "all_not_pinned"
    ALL_NOT_PINNED_GLOBALLY = "all_not_pinned_globally"

    ANON = "anon"
    ANON_PINNED = "anon_pinned"
    ANON_PINNED_GLOBALLY = "anon_pinned_globally"
    ANON_PINNED_IN_CATEGORY = "anon_pinned_in_category"
    ANON_NOT_PINNED = "anon_not_pinned"
    ANON_NOT_PINNED_GLOBALLY = "anon_not_pinned_globally"

    USER = "user"
    USER_PINNED = "user_pinned"
    USER_PINNED_GLOBALLY = "user_pinned_globally"
    USER_PINNED_IN_CATEGORY = "user_pinned_in_category"
    USER_NOT_PINNED = "user_not_pinned"
    USER_NOT_PINNED_GLOBALLY = "user_not_pinned_globally"

    USER_STARTED_PINNED = "user_started_pinned"
    USER_STARTED_PINNED_GLOBALLY = "user_started_pinned_globally"
    USER_STARTED_PINNED_IN_CATEGORY = "user_started_pinned_in_category"
    USER_STARTED_NOT_PINNED = "user_started_not_pinned"
