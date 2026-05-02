from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import pgettext, pgettext_lazy

from ..threads.lock import lock_thread, unlock_thread
from ..threadupdates.create import (
    create_locked_thread_update,
    create_unlocked_thread_update,
)
from ..threadupdates.threadflag import set_thread_has_updates
from .actions import (
    ModerationActionResult,
    ThreadsModerationAction,
    FormMixin,
    ConfirmMixin,
)
from .forms import MoveThreadForm


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
