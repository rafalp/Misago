from enum import StrEnum


class ThreadUpdateActionName(StrEnum):
    TEST = "test"

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
