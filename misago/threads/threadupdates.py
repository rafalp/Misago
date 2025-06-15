from html import escape
from typing import TYPE_CHECKING, Union

from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from .enums import ThreadUpdateActionName
from .hooks import (
    create_thread_update_hook,
    delete_thread_update_hook,
    hide_thread_update_hook,
    unhide_thread_update_hook,
)
from .models import Thread, ThreadUpdate
from .threadurl import get_thread_url

if TYPE_CHECKING:
    from ..users.models import User

__all__ = [
    "create_thread_update",
    "delete_thread_update",
    "hide_thread_update",
    "unhide_thread_update",
]


def create_thread_update(
    thread: Thread,
    action: str,
    actor: Union["User", str, None] = None,
    *,
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
) -> ThreadUpdate:
    return create_thread_update_hook(
        _create_thread_update_action,
        thread,
        action,
        actor,
        request=request,
        context=context,
        context_object=context_object,
        is_hidden=is_hidden,
        plugin_data={},
    )


def _create_thread_update_action(
    thread: Thread,
    action: str,
    actor: Union["User", None, str] = None,
    *,
    request: HttpRequest | None = None,
    context: str | None = None,
    context_object: Model | None = None,
    is_hidden: bool = False,
    plugin_data: dict,
) -> ThreadUpdate:
    actor_id = None
    actor_name = None
    context_type = None
    context_id = None

    if isinstance(actor, str):
        actor_name = actor
    elif actor:
        actor_id = actor.id
        actor_name = actor.username

    if context_object:
        context_type = ".".join(
            (
                context_object._meta.app_label,
                context_object._meta.model_name,
            )
        )
        context_id = context_object.id

    return ThreadUpdate.objects.create(
        category_id=thread.category_id,
        thread_id=thread.id,
        actor_id=actor_id,
        actor_name=actor_name,
        action=action,
        context=context,
        context_type=context_type,
        context_id=context_id,
        created_at=timezone.now(),
        is_hidden=is_hidden,
        plugin_data=plugin_data,
    )


def hide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return hide_thread_update_hook(
        _hide_thread_update_action, thread_update, {"is_hidden", "hidden_at"}, request
    )


def _hide_thread_update_action(
    thread_update: ThreadUpdate,
    update_fields: set[str],
    request: HttpRequest | None = None,
) -> bool:
    if thread_update.is_hidden:
        return False

    thread_update.is_hidden = True
    thread_update.hidden_at = timezone.now()

    if request and request.user.is_authenticated:
        thread_update.hidden_by = request.user
        thread_update.hidden_by_name = request.user.username
        update_fields.update(("hidden_by", "hidden_by_name"))

    thread_update.save(update_fields=update_fields)
    return True


def unhide_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
) -> bool:
    return unhide_thread_update_hook(
        _unhide_thread_update_action, thread_update, {"is_hidden", "hidden_at"}, request
    )


def _unhide_thread_update_action(
    thread_update: ThreadUpdate,
    update_fields: set[str],
    request: HttpRequest | None = None,
) -> bool:
    if not thread_update.is_hidden:
        return False

    thread_update.is_hidden = False
    thread_update.hidden_by = None
    thread_update.hidden_by_name = None
    thread_update.hidden_at = None

    update_fields.update(("hidden_by", "hidden_by_name"))

    thread_update.save(update_fields=update_fields)
    return True


def delete_thread_update(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    delete_thread_update_hook(_delete_thread_update_action, thread_update, request)


def _delete_thread_update_action(
    thread_update: ThreadUpdate, request: HttpRequest | None = None
):
    thread_update.delete()
    return True


class ThreadUpdatesRenderer:
    actions: dict[str, "ThreadUpdateAction"]

    def __init__(self):
        self.actions = {}

    def register_action(self, action: type["ThreadUpdateAction"]):
        action_obj = action()
        self.actions[action_obj.action] = action_obj
        return action

    def render_thread_update(
        self, thread_update: ThreadUpdate, data: dict
    ) -> dict | None:
        action = self.actions.get(thread_update.action)
        if not action:
            return

        return {
            "icon": action.icon,
            "description": action.get_description(thread_update, data),
        }


thread_updates_renderer = ThreadUpdatesRenderer()


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
        "thread update action description", "Merged %(context)s thread with this thread"
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
class TookOwnershipThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.TOOK_OWNERSHIP
    icon = "people"
    description = pgettext_lazy(
        "thread update action description", "Took thread ownership"
    )


@thread_updates_renderer.register_action
class JoinedThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.JOINED
    icon = "person_add"
    description = pgettext_lazy("thread update action description", "Joined thread")


@thread_updates_renderer.register_action
class InvitedThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.INVITED
    icon = "person_add"
    description = pgettext_lazy(
        "thread update action description", "Invited %(context)s"
    )


@thread_updates_renderer.register_action
class LeftThreadUpdateAction(ThreadUpdateAction):
    action = ThreadUpdateActionName.LEFT
    icon = "close"
    description = pgettext_lazy("thread update action description", "Left thread")


@thread_updates_renderer.register_action
class RemovedParticipantThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.REMOVED_PARTICIPANT
    icon = "block"
    description = pgettext_lazy(
        "thread update action description", "Removed %(context)s"
    )


@thread_updates_renderer.register_action
class ChangedOwnerThreadUpdateAction(UserContextThreadUpdateAction):
    action = ThreadUpdateActionName.CHANGED_OWNER
    icon = "people"
    description = pgettext_lazy(
        "thread update action description", "Changed thread owner to %(context)s"
    )
