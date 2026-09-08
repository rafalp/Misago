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

    def get_detail_text(self, context: str):
        return f"<em>{escape(context)}</em>"

    def get_detail_link(self, context_url, context: str):
        return f'<a href="{escape(context_url)}">{escape(context)}</a>'

    def get_content_object_from_data(
        self, thread_event: ThreadEvent, data: dict
    ) -> Model | None:
        if not thread_event.object_id:
            return None
        return data.get(thread_event.object_id)


class TextDetailThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        replacements = {"detail": self.get_detail_text(thread_event.detail)}
        return escape(self.description) % replacements


class CategoryDetailThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        category = self.get_content_object_from_data(thread_event, data["categories"])

        if category:
            replacements = {
                "detail": self.get_detail_link(
                    category.get_absolute_url(), category.name
                )
            }
        else:
            replacements = {"detail": self.get_detail_text(thread_event.detail)}

        return escape(self.description) % replacements


class ThreadDetailThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_content_object_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        if thread and category:
            replacements = {
                "detail": self.get_detail_link(
                    get_thread_url(thread, category), thread.title
                )
            }
        else:
            replacements = {"detail": self.get_detail_text(thread_event.detail)}

        return escape(self.description) % replacements


class UserDetailThreadEventType(ThreadEventType):
    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        user = self.get_content_object_from_data(thread_event, data["users"])

        if user:
            replacements = {
                "detail": self.get_detail_link(user.get_absolute_url(), user.username)
            }
        else:
            replacements = {"detail": self.get_detail_text(thread_event.detail)}

        return escape(self.description) % replacements


@thread_events_renderer.register_thread_event_type
class TestThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.TEST
    icon = "tabler/bug.svg"

    def get_description(
        self, thread_event: ThreadEvent, data: dict | None = None
    ) -> str:
        if thread_event.detail:
            return f"EVENT [{thread_event.id}] - {escape(thread_event.detail)}"

        return f"EVENT [{thread_event.id}]"


@thread_events_renderer.register_thread_event_type
class PinnedEverywhereThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.PINNED_EVERYWHERE
    icon = "tabler/pin-filled.svg"
    description = pgettext_lazy("thread event type description", "Pinned everywhere")


@thread_events_renderer.register_thread_event_type
class PinnedCategoryThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.PINNED_CATEGORY
    icon = "tabler/pin.svg"
    description = pgettext_lazy("thread event type description", "Pinned in category")


@thread_events_renderer.register_thread_event_type
class UnpinnedCategoryThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNPINNED
    icon = "tabler/pinned-off.svg"
    description = pgettext_lazy("thread event type description", "Unpinned")


@thread_events_renderer.register_thread_event_type
class LockedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.LOCKED
    icon = "tabler/lock.svg"
    description = pgettext_lazy("thread event type description", "Locked")


@thread_events_renderer.register_thread_event_type
class UnlockedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNLOCKED
    icon = "tabler/lock-open.svg"
    description = pgettext_lazy("thread event type description", "Unlocked")


@thread_events_renderer.register_thread_event_type
class HiddenThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.HIDDEN
    icon = "tabler/eye-off.svg"
    description = pgettext_lazy("thread event type description", "Hidden")


@thread_events_renderer.register_thread_event_type
class UnhiddenThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.UNHIDDEN
    icon = "tabler/eye.svg"
    description = pgettext_lazy("thread event type description", "Unhidden")


@thread_events_renderer.register_thread_event_type
class ApprovedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.APPROVED
    icon = "tabler/checkbox.svg"
    description = pgettext_lazy("thread event type description", "Approved")


@thread_events_renderer.register_thread_event_type
class RequiredReplyApprovalThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.REQUIRED_REPLY_APPROVAL
    icon = "tabler/player-pause-filled.svg"
    description = pgettext_lazy(
        "thread event type description", "Required reply approval"
    )


@thread_events_renderer.register_thread_event_type
class RemovedReplyApprovalThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.REMOVED_REPLY_APPROVAL
    icon = "tabler/player-pause.svg"
    description = pgettext_lazy(
        "thread event type description", "Removed reply approval"
    )


@thread_events_renderer.register_thread_event_type
class MovedThreadEventType(CategoryDetailThreadEventType):
    event_type = ThreadEventTypeName.MOVED
    icon = "tabler/arrow-right.svg"
    description = pgettext_lazy(
        "thread event type description", "Moved from %(detail)s"
    )


@thread_events_renderer.register_thread_event_type
class MergedThreadEventType(ThreadDetailThreadEventType):
    event_type = ThreadEventTypeName.MERGED
    icon = "tabler/arrows-join-2.svg"
    description = pgettext_lazy(
        "thread event type description",
        "Merged %(detail)s with this thread",
    )


@thread_events_renderer.register_thread_event_type
class ChangedTitleThreadEventType(TextDetailThreadEventType):
    event_type = ThreadEventTypeName.CHANGED_TITLE
    icon = "tabler/pencil.svg"
    description = pgettext_lazy(
        "thread event type description", "Changed title from %(detail)s"
    )


@thread_events_renderer.register_thread_event_type
class MovedPostsToThreadEventType(ThreadDetailThreadEventType):
    event_type = ThreadEventTypeName.MOVED_POSTS_TO
    icon = "tabler/arrows-right.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_content_object_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": thread_event.items}

        if thread and category:
            replacements["detail"] = self.get_detail_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["detail"] = self.get_detail_text(thread_event.detail)

        replacements["posts"] = thread_event.items
        description = npgettext(
            "thread event type description",
            "Moved %(posts)s post to %(detail)s",
            "Moved %(posts)s posts to %(detail)s",
            thread_event.items,
        )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class MovedPostsFromThreadEventType(ThreadDetailThreadEventType):
    event_type = ThreadEventTypeName.MOVED_POSTS_FROM
    icon = "tabler/arrows-right.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_content_object_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": thread_event.items}

        if thread and category:
            replacements["detail"] = self.get_detail_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["detail"] = self.get_detail_text(thread_event.detail)

        description = npgettext(
            "thread event type description",
            "Moved %(posts)s post from %(detail)s",
            "Moved %(posts)s posts from %(detail)s",
            thread_event.items,
        )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class SplitPostsIntoThreadEventType(ThreadDetailThreadEventType):
    event_type = ThreadEventTypeName.SPLIT_POSTS_INTO
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_content_object_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["detail"] = self.get_detail_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["detail"] = self.get_detail_text(thread_event.detail)

        if thread_event.items:
            replacements["posts"] = thread_event.items
            description = npgettext(
                "thread event type description",
                "Split %(posts)s post into %(detail)s",
                "Split %(posts)s posts into %(detail)s",
                thread_event.items,
            )
        else:
            description = pgettext(
                "thread event type description", "Split into %(detail)s"
            )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class SplitPostsFromThreadEventType(ThreadDetailThreadEventType):
    event_type = ThreadEventTypeName.SPLIT_POSTS_FROM
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        thread = self.get_content_object_from_data(thread_event, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["detail"] = self.get_detail_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["detail"] = self.get_detail_text(thread_event.detail)

        if thread_event.items:
            replacements["posts"] = thread_event.items
            description = npgettext(
                "thread event type description",
                "Split %(posts)s post from %(detail)s",
                "Split %(posts)s posts from %(detail)s",
                thread_event.items,
            )
        else:
            description = pgettext(
                "thread event type description", "Split from %(detail)s"
            )

        return escape(description) % replacements


@thread_events_renderer.register_thread_event_type
class DeletedPostsThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.DELETED_POSTS
    icon = "tabler/x.svg"

    def get_description(self, thread_event: ThreadEvent, data: dict) -> str:
        description = npgettext(
            "thread event type description",
            "Deleted %(posts)s post",
            "Deleted %(posts)s posts",
            thread_event.items,
        ) % {"posts": thread_event.items}

        return escape(description)


@thread_events_renderer.register_thread_event_type
class StartedPollThreadEventType(TextDetailThreadEventType):
    event_type = ThreadEventTypeName.STARTED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread event type description", "Started poll: %(detail)s"
    )


@thread_events_renderer.register_thread_event_type
class ClosedPollThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.CLOSED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy("thread event type description", "Closed poll")


@thread_events_renderer.register_thread_event_type
class OpenedPollThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.OPENED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy("thread event type description", "Opened poll")


@thread_events_renderer.register_thread_event_type
class DeletedPollThreadEventType(TextDetailThreadEventType):
    event_type = ThreadEventTypeName.DELETED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread event type description", "Deleted poll: %(detail)s"
    )


@thread_events_renderer.register_thread_event_type
class TookOwnershipThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.TOOK_OWNERSHIP
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread event type description", "Took ownership")


@thread_events_renderer.register_thread_event_type
class ChangedOwnerThreadEventType(UserDetailThreadEventType):
    event_type = ThreadEventTypeName.CHANGED_OWNER
    icon = "tabler/user.svg"
    description = pgettext_lazy(
        "thread event type description", "Changed owner to %(detail)s"
    )


@thread_events_renderer.register_thread_event_type
class MemberJoinedThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.MEMBER_JOINED
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread event type description", "Joined")


@thread_events_renderer.register_thread_event_type
class MemberLeftThreadEventType(ThreadEventType):
    event_type = ThreadEventTypeName.MEMBER_LEFT
    icon = "tabler/user-off.svg"
    description = pgettext_lazy("thread event type description", "Left")


@thread_events_renderer.register_thread_event_type
class AddedMemberThreadEventType(UserDetailThreadEventType):
    event_type = ThreadEventTypeName.ADDED_MEMBER
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread event type description", "Added %(detail)s")


@thread_events_renderer.register_thread_event_type
class RemovedMemberThreadEventType(UserDetailThreadEventType):
    event_type = ThreadEventTypeName.REMOVED_MEMBER
    icon = "tabler/user-off.svg"
    description = pgettext_lazy("thread event type description", "Removed %(detail)s")
