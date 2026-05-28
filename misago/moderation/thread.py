from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..permissions.proxy import UserPermissionsProxy
from ..categories.tasks import synchronize_categories
from ..threads.delete import delete_thread
from ..threads.lock import lock_thread, unlock_thread
from ..threads.models import Thread
from ..threadupdates.create import (
    create_locked_thread_update,
    create_unlocked_thread_update,
)
from ..threadupdates.threadflag import set_thread_has_updates
from .actions import (
    ModerationActionResult,
    ThreadModerationAction,
    FormMixin,
    ConfirmMixin,
)
from .forms import MoveThreadForm
from .hooks import (
    get_private_thread_moderation_actions_hook,
    get_thread_moderation_actions_hook,
)


def get_thread_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[ThreadModerationAction]]:
    return get_thread_moderation_actions_hook(
        _get_thread_moderation_actions_action, user_permissions, thread, request
    )


def _get_thread_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[ThreadModerationAction]]:
    if not user_permissions.is_category_moderator(thread.category_id):
        return []

    actions = []

    if thread.is_locked:
        actions.append(UnlockThreadModerationAction)
    else:
        actions.append(LockThreadModerationAction)

    return actions + [
        MoveThreadModerationAction,
        DeleteThreadModerationAction,
    ]


def get_private_thread_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[ThreadModerationAction]]:
    return get_private_thread_moderation_actions_hook(
        _get_private_thread_moderation_actions_action, user_permissions, thread, request
    )


def _get_private_thread_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[ThreadModerationAction]]:
    if not user_permissions.is_private_threads_moderator:
        return []

    actions = []

    if thread.is_locked:
        actions.append(UnlockThreadModerationAction)
    else:
        actions.append(LockThreadModerationAction)

    return actions + [
        DeleteThreadModerationAction,
    ]


class LockThreadModerationAction(ThreadModerationAction):
    id = "lock"
    button_label = pgettext_lazy("thread moderation button label", "Lock")

    def validate(self):
        if self.thread.is_locked:
            raise ValidationError(
                pgettext("thread moderation validation", "Thread is already locked.")
            )

    def execute(self) -> ModerationActionResult:
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        lock_thread(thread, request=self.request)

        thread_update = create_locked_thread_update(
            thread, self.request.user, request=self.request
        )

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread locked"),
        )

        return ModerationActionResult(
            updated_items=[thread.id],
            thread_updates=[thread_update],
        )


class UnlockThreadModerationAction(ThreadModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("thread moderation button label", "Unlock")

    def validate(self):
        if not self.thread.is_locked:
            raise ValidationError(
                pgettext("thread moderation validation", "Thread is already unlocked.")
            )

    def execute(self) -> ModerationActionResult:
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        unlock_thread(thread, request=self.request)

        thread_update = create_unlocked_thread_update(
            thread, self.request.user, request=self.request
        )

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread unlocked"),
        )

        return ModerationActionResult(
            updated_items=[thread.id], thread_updates=[thread_update]
        )


class MoveThreadModerationAction(FormMixin, ThreadModerationAction):
    id = "move"
    full_name = "Move thread"
    button_label = "Move"
    form_class = MoveThreadForm
    template_name = "misago/moderation/move_thread.html"

    def form_valid(self, form) -> ModerationActionResult:
        thread = self.thread

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread moved"),
        )

        return ModerationActionResult(
            updated_items=[thread.id],
        )


class DeleteThreadModerationAction(ConfirmMixin, ThreadModerationAction):
    id = "delete"
    full_name = "Delete thread"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "thread moderation",
        "Are you sure you want to delete this thread? This action cannot be undone.",
    )

    def confirmed(self) -> ModerationActionResult:
        thread_id = self.thread.id
        category_id = self.thread.category_id

        delete_thread(self.thread, self.request)
        synchronize_categories.delay([category_id])

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread deleted"),
        )

        return ModerationActionResult(
            deleted_items=[thread_id],
        )
