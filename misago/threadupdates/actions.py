from html import escape

from django.db.models import Model
from django.utils.translation import npgettext, pgettext, pgettext_lazy

from ..threads.threadurl import get_thread_url
from .enums import ThreadUpdateActionName
from .models import ThreadUpdate
from .renderer import thread_updates_renderer


class ThreadUpdateAction:
    action: str
    icon: str
    description: str

    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        return escape(self.description)

    def get_context_text(self, context: str):
        return f"<em>{escape(context)}</em>"

    def get_context_link(self, context_url, context: str):
        return f'<a href="{escape(context_url)}">{escape(context)}</a>'

    def get_context_obj_from_data(
        self, update: ThreadUpdate, data: dict
    ) -> Model | None:
        if not update.context_id:
            return None
        return data.get(update.context_id)


class TextContextThreadUpdateAction(ThreadUpdateAction):
    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        replacements = {"context": self.get_context_text(update.context)}
        return escape(self.description) % replacements


class CategoryContextThreadUpdateAction(ThreadUpdateAction):
    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        category = self.get_context_obj_from_data(update, data["categories"])

        if category:
            replacements = {
                "context": self.get_context_link(
                    category.get_absolute_url(), category.name
                )
            }
        else:
            replacements = {"context": self.get_context_text(update.context)}

        return escape(self.description) % replacements


class ThreadContextThreadUpdateAction(ThreadUpdateAction):
    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        thread = self.get_context_obj_from_data(update, data["threads"])
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
            replacements = {"context": self.get_context_text(update.context)}

        return escape(self.description) % replacements


class UserContextThreadUpdateAction(ThreadUpdateAction):
    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        user = self.get_context_obj_from_data(update, data["users"])

        if user:
            replacements = {
                "context": self.get_context_link(user.get_absolute_url(), user.username)
            }
        else:
            replacements = {"context": self.get_context_text(update.context)}

        return escape(self.description) % replacements


@thread_updates_renderer.register_action
class TestThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.TEST
    icon = "tabler/bug.svg"

    def get_description(self, update: ThreadUpdate, data: dict | None = None) -> str:
        if update.context:
            return f"UPDATE [{update.id}] - {escape(update.context)}"

        return f"UPDATE [{update.id}]"


@thread_updates_renderer.register_action
class PinnedEverywhereThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.PINNED_EVERYWHERE
    icon = "tabler/pin-filled.svg"
    description = pgettext_lazy("thread update action description", "Pinned everywhere")


@thread_updates_renderer.register_action
class PinnedCategoryThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.PINNED_CATEGORY
    icon = "tabler/pin.svg"
    description = pgettext_lazy(
        "thread update action description", "Pinned in category"
    )


@thread_updates_renderer.register_action
class UnpinnedCategoryThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.UNPINNED
    icon = "tabler/pinned-off.svg"
    description = pgettext_lazy("thread update action description", "Unpinned")


@thread_updates_renderer.register_action
class LockedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.LOCKED
    icon = "tabler/lock.svg"
    description = pgettext_lazy("thread update action description", "Locked")


@thread_updates_renderer.register_action
class UnlockedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.UNLOCKED
    icon = "tabler/lock-open.svg"
    description = pgettext_lazy("thread update action description", "Unlocked")


@thread_updates_renderer.register_action
class HiddenThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.HIDDEN
    icon = "tabler/eye-off.svg"
    description = pgettext_lazy("thread update action description", "Hidden")


@thread_updates_renderer.register_action
class UnhiddenThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.UNHIDDEN
    icon = "tabler/eye.svg"
    description = pgettext_lazy("thread update action description", "Unhidden")


@thread_updates_renderer.register_action
class ApprovedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.APPROVED
    icon = "tabler/checkbox.svg"
    description = pgettext_lazy("thread update action description", "Approved")


@thread_updates_renderer.register_action
class RequiredReplyApprovalThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.REQUIRED_REPLY_APPROVAL
    icon = "tabler/player-pause-filled.svg"
    description = pgettext_lazy(
        "thread update action description", "Required reply approval"
    )


@thread_updates_renderer.register_action
class RemovedReplyApprovalThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.REMOVED_REPLY_APPROVAL
    icon = "tabler/player-pause.svg"
    description = pgettext_lazy(
        "thread update action description", "Removed reply approval"
    )


@thread_updates_renderer.register_action
class MovedThreadUpdateAction(CategoryContextThreadUpdateAction):
    action = ThreadUpdateActionName.MOVED
    icon = "tabler/arrow-right.svg"
    description = pgettext_lazy(
        "thread update action description", "Moved from %(context)s"
    )


@thread_updates_renderer.register_action
class MergedThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.MERGED
    icon = "tabler/arrows-join-2.svg"
    description = pgettext_lazy(
        "thread update action description", "Merged %(context)s with this thread"
    )


@thread_updates_renderer.register_action
class MovedPostsToThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.MOVED_POSTS_TO
    icon = "tabler/arrows-right.svg"

    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        thread = self.get_context_obj_from_data(update, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": update.context_items}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(update.context)

        replacements["posts"] = update.context_items
        description = npgettext(
            "thread update action description",
            "Moved %(posts)s post to %(context)s",
            "Moved %(posts)s posts to %(context)s",
            update.context_items,
        )

        return escape(description) % replacements


@thread_updates_renderer.register_action
class MovedPostsFromThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.MOVED_POSTS_FROM
    icon = "tabler/arrows-right.svg"

    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        thread = self.get_context_obj_from_data(update, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {"posts": update.context_items}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(update.context)

        description = npgettext(
            "thread update action description",
            "Moved %(posts)s post from %(context)s",
            "Moved %(posts)s posts from %(context)s",
            update.context_items,
        )

        return escape(description) % replacements


@thread_updates_renderer.register_action
class SplitPostsIntoThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.SPLIT_POSTS_INTO
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        thread = self.get_context_obj_from_data(update, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(update.context)

        if update.context_items:
            replacements["posts"] = update.context_items
            description = npgettext(
                "thread update action description",
                "Split %(posts)s post into %(context)s",
                "Split %(posts)s posts into %(context)s",
                update.context_items,
            )
        else:
            description = pgettext(
                "thread update action description", "Split into %(context)s"
            )

        return escape(description) % replacements


@thread_updates_renderer.register_action
class SplitPostsFromThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.SPLIT_POSTS_FROM
    icon = "tabler/arrows-split-2.svg"

    def get_description(self, update: ThreadUpdate, data: dict) -> str:
        thread = self.get_context_obj_from_data(update, data["threads"])
        category = None

        if thread:
            category = data["categories"].get(thread.category_id)

        replacements = {}

        if thread and category:
            replacements["context"] = self.get_context_link(
                get_thread_url(thread, category), thread.title
            )
        else:
            replacements["context"] = self.get_context_text(update.context)

        if update.context_items:
            replacements["posts"] = update.context_items
            description = npgettext(
                "thread update action description",
                "Split %(posts)s post from %(context)s",
                "Split %(posts)s posts from %(context)s",
                update.context_items,
            )
        else:
            description = pgettext(
                "thread update action description", "Split from %(context)s"
            )

        return escape(description) % replacements


@thread_updates_renderer.register_action
class ChangedTitleThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.CHANGED_TITLE
    icon = "tabler/pencil.svg"
    description = pgettext_lazy(
        "thread update action description", "Changed title from %(context)s"
    )


@thread_updates_renderer.register_action
class StartedPollThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.STARTED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread update action description", "Started poll: %(context)s"
    )


@thread_updates_renderer.register_action
class ClosedPollThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.CLOSED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy("thread update action description", "Closed poll")


@thread_updates_renderer.register_action
class OpenedPollThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.OPENED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy("thread update action description", "Opened poll")


@thread_updates_renderer.register_action
class DeletedPollThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.DELETED_POLL
    icon = "tabler/chart-bar.svg"
    description = pgettext_lazy(
        "thread update action description", "Deleted poll: %(context)s"
    )


@thread_updates_renderer.register_action
class TookOwnershipThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.TOOK_OWNERSHIP
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread update action description", "Took ownership")


@thread_updates_renderer.register_action
class ChangedOwnerThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.CHANGED_OWNER
    icon = "tabler/user.svg"
    description = pgettext_lazy(
        "thread update action description", "Changed owner to %(context)s"
    )


@thread_updates_renderer.register_action
class JoinedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.JOINED
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread update action description", "Joined")


@thread_updates_renderer.register_action
class LeftThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.LEFT
    icon = "tabler/user-off.svg"
    description = pgettext_lazy("thread update action description", "Left")


@thread_updates_renderer.register_action
class AddedMemberThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.ADDED_MEMBER
    icon = "tabler/user.svg"
    description = pgettext_lazy("thread update action description", "Added %(context)s")


@thread_updates_renderer.register_action
class RemovedMemberThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.REMOVED_MEMBER
    icon = "tabler/user-off.svg"
    description = pgettext_lazy(
        "thread update action description", "Removed %(context)s"
    )
