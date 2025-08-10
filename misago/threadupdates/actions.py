from html import escape

from django.db.models import Model
from django.utils.translation import pgettext_lazy

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
    icon = "bug_report"

    def get_description(self, update: ThreadUpdate, data: dict | None = None) -> str:
        if update.context:
            return f"UPDATE [{update.id}] - {escape(update.context)}"

        return f"UPDATE [{update.id}]"


@thread_updates_renderer.register_action
class ApprovedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.APPROVED
    icon = "verified_user"
    description = pgettext_lazy("thread update action description", "Approved thread")


@thread_updates_renderer.register_action
class PinnedGloballyThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.PINNED_GLOBALLY
    icon = "bookmark"
    description = pgettext_lazy(
        "thread update action description", "Pinned thread globally"
    )


@thread_updates_renderer.register_action
class PinnedInCategoryThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.PINNED_IN_CATEGORY
    icon = "bookmark_outline"
    description = pgettext_lazy(
        "thread update action description", "Pinned thread in category"
    )


@thread_updates_renderer.register_action
class UnpinnedCategoryThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.UNPINNED
    icon = "radio_button_unchecked"
    description = pgettext_lazy("thread update action description", "Unpinned thread")


@thread_updates_renderer.register_action
class LockedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.LOCKED
    icon = "lock_outline"
    description = pgettext_lazy("thread update action description", "Locked thread")


@thread_updates_renderer.register_action
class OpenedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.OPENED
    icon = "lock_open"
    description = pgettext_lazy("thread update action description", "Opened thread")


@thread_updates_renderer.register_action
class MovedThreadUpdateAction(CategoryContextThreadUpdateAction):
    action = ThreadUpdateActionName.MOVED
    icon = "arrow_forward"
    description = pgettext_lazy(
        "thread update action description", "Moved thread from %(context)s"
    )


@thread_updates_renderer.register_action
class MergedThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.MERGED
    icon = "call_merge"
    description = pgettext_lazy(
        "thread update action description", "Merged %(context)s with this thread"
    )


@thread_updates_renderer.register_action
class SplitThreadUpdateAction(ThreadContextThreadUpdateAction):
    action = ThreadUpdateActionName.SPLIT
    icon = "call_split"
    description = pgettext_lazy(
        "thread update action description", "Split this thread from %(context)s"
    )


@thread_updates_renderer.register_action
class HidThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.HID
    icon = "visibility_off"
    description = pgettext_lazy("thread update action description", "Hid thread")


@thread_updates_renderer.register_action
class UnhidThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.UNHID
    icon = "visibility"
    description = pgettext_lazy("thread update action description", "Unhid thread")


@thread_updates_renderer.register_action
class ChangedTitleThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.CHANGED_TITLE
    icon = "edit"
    description = pgettext_lazy(
        "thread update action description", "Changed thread title from %(context)s"
    )


@thread_updates_renderer.register_action
class StartedPollThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.STARTED_POLL
    icon = "poll"
    description = pgettext_lazy(
        "thread update action description", "Started poll: %(context)s"
    )


@thread_updates_renderer.register_action
class ClosedPollThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.CLOSED_POLL
    icon = "poll"
    description = pgettext_lazy("thread update action description", "Closed poll")


@thread_updates_renderer.register_action
class OpenedPollThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.OPENED_POLL
    icon = "poll"
    description = pgettext_lazy("thread update action description", "Opened poll")


@thread_updates_renderer.register_action
class DeletedPollThreadUpdateAction(TextContextThreadUpdateAction):
    action = ThreadUpdateActionName.DELETED_POLL
    icon = "poll"
    description = pgettext_lazy(
        "thread update action description", "Deleted poll: %(context)s"
    )


@thread_updates_renderer.register_action
class TookOwnershipThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.TOOK_OWNERSHIP
    icon = "people"
    description = pgettext_lazy(
        "thread update action description", "Took thread ownership"
    )


@thread_updates_renderer.register_action
class ChangedOwnerThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.CHANGED_OWNER
    icon = "people"
    description = pgettext_lazy(
        "thread update action description", "Changed thread owner to %(context)s"
    )


@thread_updates_renderer.register_action
class JoinedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.JOINED
    icon = "person_add"
    description = pgettext_lazy("thread update action description", "Joined thread")


@thread_updates_renderer.register_action
class LeftThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.LEFT
    icon = "close"
    description = pgettext_lazy("thread update action description", "Left thread")


@thread_updates_renderer.register_action
class AddedMemberThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.ADDED_MEMBER
    icon = "person_add"
    description = pgettext_lazy("thread update action description", "Added %(context)s")


@thread_updates_renderer.register_action
class RemovedMemberThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.REMOVED_MEMBER
    icon = "block"
    description = pgettext_lazy(
        "thread update action description", "Removed %(context)s"
    )
