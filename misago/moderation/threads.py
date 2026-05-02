from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..threads.lock import lock_thread, unlock_thread
from ..threads.models import Thread
from ..threadupdates.create import (
    create_locked_thread_update,
    create_unlocked_thread_update,
)
from ..threadupdates.threadflag import set_thread_has_updates
from .actions import ModerationActionResult, ThreadsModerationAction, FormMixin, ConfirmMixin
from .forms import MoveThreads


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


class ConfirmThreadsModerationAction(ConfirmMixin, ThreadsModerationAction):
    id = "confirm"
    full_name = "Confirm threads"
    button_label = "Confirm"
    confirmation_message = "Are you sure you want to test this action? This can't be undone!"

    def validate(self):
        if len(self.threads) > 3:
            raise ValidationError("This action can't be done for more than 3 threads!")
    
    def confirmed(self) -> ModerationActionResult:
        messages.success(self.request, "Test completed")

        return ModerationActionResult(
            updated_items=[thread.id for thread in self.threads],
        )
