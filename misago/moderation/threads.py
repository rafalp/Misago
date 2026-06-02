from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..permissions.proxy import UserPermissionsProxy
from ..threads.enums import ThreadPinned
from ..threads.lock import lock_thread, unlock_thread
from ..threads.pin import pin_thread_globally, pin_thread_in_category, unpin_thread
from ..threadupdates.create import (
    create_locked_thread_update,
    create_pinned_globally_thread_update,
    create_pinned_in_category_thread_update,
    create_unlocked_thread_update,
    create_unpinned_thread_update,
)
from ..threadupdates.threadflag import set_thread_has_updates
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationActionResult,
    ThreadsModerationAction,
)
from .forms import MoveThreadForm
from .hooks import (
    get_category_threads_moderation_actions_hook,
    get_threads_moderation_actions_hook,
)


def get_threads_moderation_actions(
    user_permissions: UserPermissionsProxy,
    request: HttpRequest | None = None,
) -> list[type[ThreadsModerationAction]]:
    return get_threads_moderation_actions_hook(
        _get_threads_moderation_actions_action, user_permissions, request
    )


def _get_threads_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    request: HttpRequest | None = None,
) -> list[type[ThreadsModerationAction]]:
    if not user_permissions.moderated_categories:
        return []

    actions = []

    if user_permissions.is_global_moderator:
        actions.append()

    return [
        LockThreadsModerationAction,
        UnlockThreadsModerationAction,
        MoveThreadsModerationAction,
        DeleteThreadsModerationAction,
    ]


def get_category_threads_moderation_actions(
    user_permissions: UserPermissionsProxy,
    category: Category,
    request: HttpRequest | None = None,
) -> list[type[ThreadsModerationAction]]:
    return get_category_threads_moderation_actions_hook(
        _get_category_threads_moderation_actions_action,
        user_permissions,
        category,
        request,
    )


def _get_category_threads_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    category: Category,
    request: HttpRequest | None = None,
) -> list[type[ThreadsModerationAction]]:
    if not user_permissions.is_category_moderator(category.id):
        return []

    return [
        LockThreadsModerationAction,
        UnlockThreadsModerationAction,
        MoveThreadsModerationAction,
        DeleteThreadsModerationAction,
    ]


class PinGloballyThreadModerationAction(ThreadsModerationAction):
    id = "pin_globally"
    button_label = pgettext_lazy("threads moderation button label", "Pin globally")

    def validate(self):
        for thread in self.threads:
            if thread.pinned != ThreadPinned.EVERYWHERE:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already locked.")
        )

    def execute(self) -> ModerationActionResult:
        valid_threads = [thread for thread in self.threads if not thread.is_locked]

        for thread in valid_threads:
            set_thread_has_updates(thread, commit=False)
            lock_thread(thread, request=self.request)

            create_locked_thread_update(thread, self.request.user, request=self.request)

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads locked"),
        )

        return ModerationActionResult(
            updated_items=[thread.id for thread in valid_threads],
        )


class LockThreadsModerationAction(ThreadsModerationAction):
    id = "lock"
    button_label = pgettext_lazy("threads moderation button label", "Lock")

    def validate(self):
        for thread in self.threads:
            if not thread.is_locked:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already locked.")
        )

    def execute(self) -> ModerationActionResult:
        valid_threads = [thread for thread in self.threads if not thread.is_locked]

        for thread in valid_threads:
            set_thread_has_updates(thread, commit=False)
            lock_thread(thread, request=self.request)

            create_locked_thread_update(thread, self.request.user, request=self.request)

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads locked"),
        )

        return ModerationActionResult(
            updated_items=[thread.id for thread in valid_threads],
        )


class UnlockThreadsModerationAction(ThreadsModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("threads moderation button label", "Unlock")

    def validate(self):
        for thread in self.threads:
            if thread.is_locked:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already unlocked.")
        )

    def execute(self) -> ModerationActionResult:
        valid_threads = [thread for thread in self.threads if thread.is_locked]

        for thread in valid_threads:
            set_thread_has_updates(thread, commit=False)
            unlock_thread(thread, request=self.request)

            create_unlocked_thread_update(
                thread, self.request.user, request=self.request
            )

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads unlocked"),
        )

        return ModerationActionResult(
            updated_items=[thread.id for thread in valid_threads],
        )


class MoveThreadsModerationAction(FormMixin, ThreadsModerationAction):
    id = "move"
    full_name = "Move threads"
    button_label = "Move"
    form_class = MoveThreadForm
    template_name = "misago/moderation/move_threads.html"

    def form_valid(self, form) -> ModerationActionResult:
        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads moved"),
        )

        return ModerationActionResult(
            updated_items=[thread.id for thread in self.threads],
        )


class DeleteThreadsModerationAction(ConfirmMixin, ThreadsModerationAction):
    id = "delete"
    full_name = "Delete threads"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "threads moderation",
        "Are you sure you want to delete the selected threads? This action cannot be undone.",
    )

    def confirmed(self) -> ModerationActionResult:
        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads deleted"),
        )

        return ModerationActionResult(
            deleted_items=[thread.id for thread in self.threads],
        )
