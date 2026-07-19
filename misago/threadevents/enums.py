from enum import StrEnum


class ThreadEventActionName(StrEnum):
    TEST = "test"

    PINNED_EVERYWHERE = "pinned_everywhere"
    PINNED_CATEGORY = "pinned_category"
    UNPINNED = "unpinned"

    LOCKED = "locked"
    UNLOCKED = "unlocked"

    HIDDEN = "hidden"
    UNHIDDEN = "unhidden"

    APPROVED = "approved"

    MOVED = "moved"
    MERGED = "merged"

    CHANGED_TITLE = "changed_title"

    MOVED_POSTS_TO = "moved_posts_to"
    MOVED_POSTS_FROM = "moved_posts_from"

    SPLIT_POSTS_INTO = "split_posts_into"
    SPLIT_POSTS_FROM = "split_posts_from"

    DELETED_POSTS = "deleted_posts"

    REQUIRED_REPLY_APPROVAL = "required_reply_approval"
    REMOVED_REPLY_APPROVAL = "removed_reply_approval"

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
