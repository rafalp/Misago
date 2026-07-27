from html import escape

from django.db.models import Model
from django.utils.translation import npgettext, pgettext, pgettext_lazy

from ..threads.threadurl import get_thread_url
from .enums import ThreadEventTypeName
from .models import ThreadEvent
from .renderer import thread_events_renderer


class ThreadEventType:
    event_type: str
    icon: str
    description: str

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        return escape(self.description)

    def get_context_text(self, context: str):
        return f"<em>{escape(context)}</em>"

    def get_context_link(self, context_url, context: str):
        return f'<a href="{escape(context_url)}">{escape(context)}</a>'

    def get_context_obj_from_data(
        self, thread_event: ThreadEvent, data: dict
    ) -> Model | None:
        if not thread_event.context_id:
            return None
        return data.get(thread_event.context_id)


class TextContextThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        replacements = {"context": self.get_context_text(thread_event.context)}
        return escape(self.description) % replacements


class CategoryContextThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        category = self.get_context_obj_from_data(thread_event, data["categories"])

        if category:
            replacements = {
                "context": self.get_context_link(
                    category.get_absolute_url(), category.name
                )
            }
        else:
            replacements = {"context": self.get_context_text(thread_event.context)}

        return escape(self.description) % replacements


class ThreadContextThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_context_obj_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        if thread and category:
            replacements = {
                "context": self.get_context_link(
                    get_thread_url(thread, category), thread.title
                )
            }
        else:
            replacements = {"context": self.get_context_text(thread_event.context)}

        return escape(self.description) % replacements


class UserContextThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        user = self.get_context_obj_from_data(thread_event, data["users"])

        if user:
            replacements = {
                "context": self.get_context_link(user.get_absolute_url(), user.username)
            }
        else:
            replacements = {"context": self.get_context_text(thread_event.context)}

        return escape(self.description) % replacements


@thread_events_renderer.register_thread_event_type
class TestThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.TEST
    icon = "tabler/bug.svg"

    def get_description(
        self, thread_event: ThreadEvent, data: dict | None = None
    ) -> str:
        if thread_event.context:
            return f"UPDATE [{thread_event.id}] - {escape(thread_event.context)}"

        return f"UPDATE [{thread_event.id}]"


@thread_events_renderer.register_thread_event_type
class PinnedEverywhereThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.PINNED_EVERYWHERE
    icon = "tabler/pin-filled.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Pinned everywhere"
    )


@thread_events_renderer.register_thread_event_type
class PinnedCategoryThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.PINNED_CATEGORY
    icon = "tabler/pin.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Pinned in category"
    )


@thread_events_renderer.register_thread_event_type
class UnpinnedCategoryThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNPINNED
    icon = "tabler/pinned-off.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Unpinned"
    )


@thread_events_renderer.register_thread_event_type
class LockedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.LOCKED
    icon = "tabler/lock.svg"
    description = pgettext_lazy("thread thread_event event_type description", "Locked")


@thread_events_renderer.register_thread_event_type
class UnlockedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNLOCKED
    icon = "tabler/lock-open.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Unlocked"
    )


@thread_events_renderer.register_thread_event_type
class HiddenThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.HIDDEN
    icon = "tabler/eye-off.svg"
    description = pgettext_lazy("thread thread_event event_type description", "Hidden")


@thread_events_renderer.register_thread_event_type
class UnhiddenThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNHIDDEN
    icon = "tabler/eye.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Unhidden"
    )


@thread_events_renderer.register_thread_event_type
class ApprovedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.APPROVED
    icon = "tabler/checkbox.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Approved"
    )


@thread_events_renderer.register_thread_event_type
class RequiredReplyApprovalThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.REQUIRED_REPLY_APPROVAL
    icon = "tabler/player-pause-filled.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Required reply approval"
    )


@thread_events_renderer.register_thread_event_type
class RemovedReplyApprovalThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.REMOVED_REPLY_APPROVAL
    icon = "tabler/player-pause.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Removed reply approval"
    )


@thread_events_renderer.register_thread_event_type
class MovedThreadEventEventType(CategoryContextThreadEventType):
    event_type = ThreadEventTypeName.MOVED
    icon = "tabler/arrow-right.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Moved from %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class MergedThreadEventEventType(ThreadContextThreadEventType):
    event_type = ThreadEventTypeName.MERGED
    icon = "tabler/arrows-join-2.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description",
        "Merged %(context)s with this thread",
    )


@thread_events_renderer.register_thread_event_type
class ChangedTitleThreadEventEventType(TextContextThreadEventType):
    event_type = ThreadEventTypeName.CHANGED_TITLE
    icon = "tabler/pencil.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Changed title from %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class MovedPostsToThreadEventEventType(ThreadContextThreadEventType):
    event_type = ThreadEventTypeName.MOVED_POSTS_TO
    icon = "tabler/arrows-right.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_context_obj_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": thread_event.context_items}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(thread_event.context)

        replacements["posts"] = thread_event.context_items
        description = npgettext(
            "thread thread_event event_type description",
            "Moved %(posts)s post to %(context)s",
            "Moved %(posts)s posts to %(context)s",
            thread_event.context_items,
        )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class MovedPostsFromThreadEventEventType(ThreadContextThreadEventType):
    event_type = ThreadEventTypeName.MOVED_POSTS_FROM
    icon = "tabler/arrows-right.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_context_obj_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": thread_event.context_items}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(thread_event.context)

        description = npgettext(
            "thread thread_event event_type description",
            "Moved %(posts)s post from %(context)s",
            "Moved %(posts)s posts from %(context)s",
            thread_event.context_items,
        )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class SplitPostsIntoThreadEventEventType(ThreadContextThreadEventType):
    event_type = ThreadEventTypeName.SPLIT_POSTS_INTO
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_context_obj_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(thread_event.context)

        if thread_event.context_items:
            replacements["posts"] = thread_event.context_items
            description = npgettext(
                "thread thread_event event_type description",
                "Split %(posts)s post into %(context)s",
                "Split %(posts)s posts into %(context)s",
                thread_event.context_items,
            )
        else:
            description = pgettext(
                "thread thread_event event_type description", "Split into %(context)s"
            )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class SplitPostsFromThreadEventEventType(ThreadContextThreadEventType):
    event_type = ThreadEventTypeName.SPLIT_POSTS_FROM
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_context_obj_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(thread_event.context)

        if thread_event.context_items:
            replacements["posts"] = thread_event.context_items
            description = npgettext(
                "thread thread_event event_type description",
                "Split %(posts)s post from %(context)s",
                "Split %(posts)s posts from %(context)s",
                thread_event.context_items,
            )
        else:
            description = pgettext(
                "thread thread_event event_type description", "Split from %(context)s"
            )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class DeletedPostsThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.DELETED_POSTS
    icon = "tabler/x.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        description = npgettext(
            "thread thread_event event_type description",
            "Deleted %(posts)s post",
            "Deleted %(posts)s posts",
            thread_event.context_items,
        ) % {"posts": thread_event.context_items}

        return escape(description)


@thread_events_renderer.register_thread_event_type
class StartedPollThreadEventEventType(TextContextThreadEventType):
    event_type = ThreadEventTypeName.STARTED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Started poll: %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class ClosedPollThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.CLOSED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Closed poll"
    )


@thread_events_renderer.register_thread_event_type
class OpenedPollThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.OPENED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Opened poll"
    )


@thread_events_renderer.register_thread_event_type
class DeletedPollThreadEventEventType(TextContextThreadEventType):
    event_type = ThreadEventTypeName.DELETED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Deleted poll: %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class TookOwnershipThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.TOOK_OWNERSHIP
    icon = "tabler/user.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Took ownership"
    )


@thread_events_renderer.register_thread_event_type
class ChangedOwnerThreadEventEventType(UserContextThreadEventType):
    event_type = ThreadEventTypeName.CHANGED_OWNER
    icon = "tabler/user.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Changed owner to %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class JoinedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.JOINED
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread thread_event event_type description", "Joined")


@thread_events_renderer.register_thread_event_type
class LeftThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.LEFT
    icon = "tabler/user-off.svg"
    description = pgettext_lazy("thread thread_event event_type description", "Left")


@thread_events_renderer.register_thread_event_type
class AddedMemberThreadEventEventType(UserContextThreadEventType):
    event_type = ThreadEventTypeName.ADDED_MEMBER
    icon = "tabler/user.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Added %(context)s"
    )


@thread_events_renderer.register_thread_event_type
class RemovedMemberThreadEventEventType(UserContextThreadEventType):
    event_type = ThreadEventTypeName.REMOVED_MEMBER
    icon = "tabler/user-off.svg"
    description = pgettext_lazy(
        "thread thread_event event_type description", "Removed %(context)s"
    )
