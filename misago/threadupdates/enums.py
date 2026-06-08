from enum import StrEnum


class ThreadUpdateActionName(StrEnum):
    TEST = "test"

    PINNED_EVERYWHERE = "pinned_everywhere"
    PINNED_CATEGORY = "pinned_category"
    UNPINNED = "unpinned"

    LOCKED = "locked"
    UNLOCKED = "unlocked"

    HIDDEN = "hidden"
    UNHIDDEN = "unhidden"

    APPROVED = "approved"
    REQUIRED_REPLY_APPROVAL = "required_reply_approval"
    REMOVED_REPLY_APPROVAL = "removed_reply_approval"

    MOVED = "moved"

    MERGED = "merged"
    SPLIT = "split"

    CHANGED_TITLE = "changed_title"

    STARTED_POLL = "started_poll"
    CLOSED_POLL = "closed_poll"
    OPENED_POLL = "opened_poll"
    DELETED_POLL = "deleted_poll"

    TOOK_OWNERSHIP = "took_ownership"
    CHANGED_OWNER = "changed_owner"

    JOINED = "joined"
    LEFT = "left"

    ADDED_MEMBER = "added_member"
    REMOVED_MEMBER = "removed_member"
