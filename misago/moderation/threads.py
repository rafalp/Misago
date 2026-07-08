from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import prefetch_related_objects
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.tasks import synchronize_categories
from ..notifications.tasks import delete_duplicate_watched_threads
from ..permissions.proxy import UserPermissionsProxy
from ..threads.approve import (
    approve_thread,
    remove_thread_reply_approval,
    require_thread_reply_approval,
)
from ..threads.create import create_thread
from ..threads.delete import delete_thread
from ..threads.enums import ThreadPinned
from ..threads.hide import hide_thread, unhide_thread
from ..threads.lock import lock_thread, unlock_thread
from ..threads.merge import get_thread_merge_conflicts, merge_threads
from ..threads.move import move_thread
from ..threads.pin import pin_thread, unpin_thread
from ..threads.synchronize import synchronize_thread
from ..threadupdates.create import (
    create_approved_thread_update,
    create_hidden_thread_update,
    create_locked_thread_update,
    create_merged_thread_update,
    create_moved_thread_update,
    create_pinned_category_thread_update,
    create_pinned_everywhere_thread_update,
    create_removed_reply_approval_thread_update,
    create_required_reply_approval_thread_update,
    create_unhidden_thread_update,
    create_unlocked_thread_update,
    create_unpinned_thread_update,
)
from ..threadupdates.threadflag import set_thread_has_updates
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    ThreadsModerationAction,
)
from .forms import HideForm, MergeThreadsForm, MoveThreadsForm
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
        actions.append(PinEverywhereThreadsModerationAction)

    return actions + [
        PinCategoryThreadsModerationAction,
        UnpinThreadsModerationAction,
        LockThreadsModerationAction,
        UnlockThreadsModerationAction,
        HideThreadsModerationAction,
        UnhideThreadsModerationAction,
        ApproveThreadsModerationAction,
        RequireThreadsReplyApprovalModerationAction,
        RemoveThreadsReplyApprovalModerationAction,
        MoveThreadsModerationAction,
        MergeThreadsModerationAction,
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

    actions = []

    if user_permissions.is_global_moderator:
        actions.append(PinEverywhereThreadsModerationAction)

    return actions + [
        PinCategoryThreadsModerationAction,
        UnpinThreadsModerationAction,
        LockThreadsModerationAction,
        UnlockThreadsModerationAction,
        HideThreadsModerationAction,
        UnhideThreadsModerationAction,
        ApproveThreadsModerationAction,
        RequireThreadsReplyApprovalModerationAction,
        RemoveThreadsReplyApprovalModerationAction,
        MoveThreadsModerationAction,
        MergeThreadsModerationAction,
        DeleteThreadsModerationAction,
    ]


class PinEverywhereThreadsModerationAction(ThreadsModerationAction):
    id = "pin_everywhere"
    button_label = pgettext_lazy("threads moderation button label", "Pin everywhere")

    def validate(self):
        for thread in self.threads:
            if thread.pinned != ThreadPinned.EVERYWHERE:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already pinned.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [
            thread
            for thread in self.threads
            if thread.pinned != ThreadPinned.EVERYWHERE
        ]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            pin_thread(thread, everywhere=True, request=request)

            create_pinned_everywhere_thread_update(
                thread, request.user, request=request
            )

        messages.success(
            request,
            pgettext("threads moderation success", "Threads pinned everywhere"),
        )

        return ModerationResult.from_updated_threads(threads)


class PinCategoryThreadsModerationAction(ThreadsModerationAction):
    id = "pin_category"
    button_label = pgettext_lazy("threads moderation button label", "Pin in category")

    def validate(self):
        for thread in self.threads:
            if thread.pinned != ThreadPinned.CATEGORY:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already pinned.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [
            thread for thread in self.threads if thread.pinned != ThreadPinned.CATEGORY
        ]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            pin_thread(thread, everywhere=False, request=request)

            create_pinned_category_thread_update(thread, request.user, request=request)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads pinned in category"),
        )

        return ModerationResult.from_updated_threads(threads)


class UnpinThreadsModerationAction(ThreadsModerationAction):
    id = "unpin"
    button_label = pgettext_lazy("threads moderation button label", "Unpin")

    def validate(self):
        for thread in self.threads:
            if thread.pinned:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already unpinned.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if thread.pinned]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            unpin_thread(thread, request=request)

            create_unpinned_thread_update(thread, request.user, request=request)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads unpinned"),
        )

        return ModerationResult.from_updated_threads(threads)


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

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if not thread.is_locked]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            lock_thread(thread, request=request)

            create_locked_thread_update(thread, request.user, request=request)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads locked"),
        )

        return ModerationResult.from_updated_threads(threads)


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

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if thread.is_locked]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            unlock_thread(thread, request=request)
            create_unlocked_thread_update(thread, request.user, request=request)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads unlocked"),
        )

        return ModerationResult.from_updated_threads(threads)


class HideThreadsModerationAction(FormMixin, ThreadsModerationAction):
    id = "hide"
    full_name = pgettext_lazy("threads moderation action name", "Hide threads")
    button_label = pgettext_lazy("threads moderation button label", "Hide")

    form_class = HideForm
    template_name = "misago/moderation/hide.html"

    def validate(self):
        for thread in self.threads:
            if not thread.is_hidden:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already hidden.")
        )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if not thread.is_hidden]
        hidden_reason = form.cleaned_data["hidden_reason"]
        categories = list(set(thread.category_id for thread in threads))

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            hide_thread(thread, request.user, hidden_reason, request=request)
            create_hidden_thread_update(thread, request.user, request=request)

        synchronize_categories.delay(categories)

        messages.success(
            self.request,
            pgettext("thread moderation success", "Threads hidden"),
        )

        return ModerationResult.from_updated_threads(threads)


class UnhideThreadsModerationAction(ThreadsModerationAction):
    id = "unhide"
    button_label = pgettext_lazy("threads moderation button label", "Unhide")

    def validate(self):
        for thread in self.threads:
            if thread.is_hidden:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already unhidden.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if thread.is_hidden]
        categories = list(set(thread.category_id for thread in threads))

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            unhide_thread(thread, request=request)
            create_unhidden_thread_update(thread, request.user, request=request)

        synchronize_categories.delay(categories)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads unhidden"),
        )

        return ModerationResult.from_updated_threads(threads)


class ApproveThreadsModerationAction(ThreadsModerationAction):
    id = "approve"
    button_label = pgettext_lazy("threads moderation button label", "Approve")

    def validate(self):
        for thread in self.threads:
            if thread.is_unapproved:
                return

        raise ValidationError(
            pgettext("threads moderation validation", "Threads are already approved.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if thread.is_unapproved]
        categories = list(set(thread.category_id for thread in threads))

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            approve_thread(thread, request=request)
            create_approved_thread_update(thread, request.user, request=request)

        synchronize_categories.delay(categories)

        messages.success(
            request,
            pgettext("threads moderation success", "Threads approved"),
        )

        return ModerationResult.from_updated_threads(threads)


class RequireThreadsReplyApprovalModerationAction(ThreadsModerationAction):
    id = "require_reply_approval"
    button_label = pgettext_lazy(
        "threads moderation button label", "Require reply approval"
    )

    def validate(self):
        for thread in self.threads:
            if not thread.require_reply_approval:
                return

        raise ValidationError(
            pgettext(
                "threads moderation validation",
                "Threads already require reply approval.",
            )
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [
            thread for thread in self.threads if not thread.require_reply_approval
        ]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            require_thread_reply_approval(thread, request=request)

            create_required_reply_approval_thread_update(
                thread, request.user, request=request
            )

        messages.success(
            request,
            pgettext("threads moderation success", "Reply approval required"),
        )

        return ModerationResult.from_updated_threads(threads)


class RemoveThreadsReplyApprovalModerationAction(ThreadsModerationAction):
    id = "remove_reply_approval"
    button_label = pgettext_lazy(
        "threads moderation button label", "Remove reply approval"
    )

    def validate(self):
        for thread in self.threads:
            if thread.require_reply_approval:
                return

        raise ValidationError(
            pgettext(
                "threads moderation validation",
                "Threads already don't require reply approval.",
            )
        )

    def execute(self) -> ModerationResult:
        request = self.request
        threads = [thread for thread in self.threads if thread.require_reply_approval]

        for thread in threads:
            set_thread_has_updates(thread, commit=False)
            remove_thread_reply_approval(thread, request=request)

            create_removed_reply_approval_thread_update(
                thread, request.user, request=request
            )

        messages.success(
            request,
            pgettext("threads moderation success", "Reply approval removed"),
        )

        return ModerationResult.from_updated_threads(threads)


class MoveThreadsModerationAction(FormMixin, ThreadsModerationAction):
    id = "move"
    full_name = pgettext_lazy("threads moderation action name", "Move threads")
    button_label = pgettext_lazy("threads moderation button label", "Move")

    form_class = MoveThreadsForm
    template_name = "misago/moderation/move_threads.html"

    def get_form(self, form_submitted: bool):
        kwargs = {
            "request": self.request,
            "prefix": self.form_prefix,
        }

        threads_categories = set(thread.category_id for thread in self.threads)
        if len(threads_categories) == 1:
            kwargs["disallowed_categories"] = threads_categories

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        new_category = form.cleaned_data["category"]
        threads = [
            thread for thread in self.threads if thread.category_id != new_category.id
        ]

        categories = set()
        categories.add(new_category.id)

        prefetch_related_objects(threads, "category")

        for thread in threads:
            old_category = thread.category
            categories.add(old_category.id)

            set_thread_has_updates(thread, commit=False)
            move_thread(thread, new_category, request=request)
            create_moved_thread_update(
                thread, old_category, request.user, request=request
            )

        synchronize_categories.delay(list(categories))

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads moved"),
        )

        return ModerationResult.from_updated_threads(threads)


class MergeThreadsModerationAction(FormMixin, ThreadsModerationAction):
    id = "merge"
    full_name = pgettext_lazy("threads moderation action name", "Merge threads")
    button_label = pgettext_lazy("threads moderation button label", "Merge")

    form_class = MergeThreadsForm
    template_name = "misago/moderation/merge_threads.html"

    def validate(self):
        if len(self.threads) < 2:
            raise ValidationError(
                pgettext(
                    "threads moderation validation",
                    "Select at least two threads to merge.",
                )
            )

    def get_form(self, form_submitted: bool):
        kwargs = {
            "request": self.request,
            "prefix": self.form_prefix,
            "conflicts": get_thread_merge_conflicts(self.threads, self.request),
            "initial": {
                "category": self.threads[0].category_id,
            },
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        new_category = form.cleaned_data["category"]
        threads = self.threads

        categories = set()
        categories.add(new_category.id)

        prefetch_related_objects(threads, "category")

        for thread in threads:
            categories.add(thread.category_id)

        conflicts = form.get_conflicts_resolutions()
        new_thread = create_thread(
            new_category,
            form.cleaned_data["title"],
            pinned=form.cleaned_data["pin"],
            is_locked=form.cleaned_data["is_locked"],
            is_hidden=form.cleaned_data["is_hidden"],
            request=request,
        )

        merge_threads(new_thread, threads, conflicts, request=request)

        for thread in threads:
            create_merged_thread_update(
                new_thread, thread, self.request.user, request=request
            )

        synchronize_thread(new_thread, request=request)

        synchronize_categories.delay(list(categories))
        delete_duplicate_watched_threads.delay(new_thread.id)

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads merged"),
        )

        return ModerationResult.from_deleted_threads(threads)


class DeleteThreadsModerationAction(ConfirmMixin, ThreadsModerationAction):
    id = "delete"
    full_name = "Delete threads"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "threads moderation",
        "Are you sure you want to delete the selected threads? This can't be undone.",
    )

    def confirmed(self) -> ModerationResult:
        request = self.request

        categories = set()

        for thread in self.threads:
            categories.add(thread.category_id)
            delete_thread(thread, request=request)

        synchronize_categories.delay(list(categories))

        messages.success(
            self.request,
            pgettext("threads moderation success", "Threads deleted"),
        )

        return ModerationResult(
            deleted_items=[thread.id for thread in self.threads],
        )
