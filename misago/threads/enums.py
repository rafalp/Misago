from enum import IntEnum, StrEnum


class ThreadWeight(IntEnum):
    NOT_PINNED = 0
    PINNED_IN_CATEGORY = 1
    PINNED_GLOBALLY = 2


class ThreadUrl(StrEnum):
    THREAD = "misago:thread"
    POST = "misago:thread-post"
    NEW_POST = "misago:thread-new"
    LAST_POST = "misago:thread-last"
    UNAPPROVED_POST = "misago:thread-unapproved"
    BEST_ANSWER = "misago:thread-best-answer"


class PrivateThreadUrl(StrEnum):
    THREAD = "misago:private-thread"
    POST = "misago:private-thread-post"
    NEW_POST = "misago:private-thread-new"
    LAST_POST = "misago:private-thread-last"
    UNAPPROVED_POST = "misago:private-thread-unapproved"
    BEST_ANSWER = "misago:private-thread-best-answer"
