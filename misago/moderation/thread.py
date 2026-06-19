from django.contrib import messages
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.tasks import synchronize_categories
from ..notifications.tasks import (
    delete_duplicate_watched_threads,
    notify_on_new_private_thread,
)
from ..permissions.proxy import UserPermissionsProxy
from ..privatethreads.members import prefetch_private_thread_member_ids
from ..threads.approve import (
    approve_thread,
    remove_thread_reply_approval,
    require_thread_reply_approval,
)
from ..threads.delete import delete_thread
from ..threads.enums import ThreadPinned
from ..threads.hide import hide_thread, unhide_thread
from ..threads.lock import lock_thread, unlock_thread
from ..threads.merge import merge_threads
from ..threads.models import Thread
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
    ModerationActionResult,
    ThreadModerationAction,
)
from .forms import HideForm, MergeThreadForm, MoveThreadForm
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

    if (
        user_permissions.is_global_moderator
        and thread.pinned != ThreadPinned.EVERYWHERE
    ):
        actions.append(PinEverywhereThreadModerationAction)

    if thread.pinned != ThreadPinned.CATEGORY:
        actions.append(PinCategoryThreadModerationAction)

    if thread.pinned:
        actions.append(UnpinThreadModerationAction)

    if thread.is_locked:
        actions.append(UnlockThreadModerationAction)
    else:
        actions.append(LockThreadModerationAction)

    if thread.is_hidden:
        actions.append(UnhideThreadModerationAction)
    else:
        actions.append(HideThreadModerationAction)

    if thread.is_unapproved:
        actions.append(ApproveThreadModerationAction)

    if thread.require_reply_approval:
        actions.append(RemoveThreadReplyApprovalModerationAction)
    else:
        actions.append(RequireThreadReplyApprovalModerationAction)

    return actions + [
        MoveThreadModerationAction,
        MergeThreadModerationAction,
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

    if thread.is_hidden:
        actions.append(UnhideThreadModerationAction)
    else:
        actions.append(HideThreadModerationAction)

    if thread.is_unapproved:
        actions.append(ApprovePrivateThreadModerationAction)

    if thread.require_reply_approval:
        actions.append(RemoveThreadReplyApprovalModerationAction)
    else:
        actions.append(RequireThreadReplyApprovalModerationAction)

    return actions + [
        DeleteThreadModerationAction,
    ]


class PinEverywhereThreadModerationAction(ThreadModerationAction):
    id = "pin_everywhere"
    button_label = pgettext_lazy("thread moderation button label", "Pin everywhere")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        pin_thread(thread, everywhere=True, request=request)

        thread_update = create_pinned_everywhere_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            request,
            pgettext("thread moderation success", "Thread pinned everywhere"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class PinCategoryThreadModerationAction(ThreadModerationAction):
    id = "pin_category"
    button_label = pgettext_lazy("thread moderation button label", "Pin in category")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        pin_thread(thread, everywhere=False, request=request)

        thread_update = create_pinned_category_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            request,
            pgettext("thread moderation success", "Thread pinned in category"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class UnpinThreadModerationAction(ThreadModerationAction):
    id = "unpin"
    button_label = pgettext_lazy("thread moderation button label", "Unpin")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        unpin_thread(thread, request=request)

        thread_update = create_unpinned_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            request,
            pgettext("thread moderation success", "Thread unpinned"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class LockThreadModerationAction(ThreadModerationAction):
    id = "lock"
    button_label = pgettext_lazy("thread moderation button label", "Lock")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        lock_thread(thread, request=request)

        thread_update = create_locked_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            request,
            pgettext("thread moderation success", "Thread locked"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class UnlockThreadModerationAction(ThreadModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("thread moderation button label", "Unlock")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        unlock_thread(thread, request=request)

        thread_update = create_unlocked_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            request,
            pgettext("thread moderation success", "Thread unlocked"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class HideThreadModerationAction(FormMixin, ThreadModerationAction):
    id = "hide"
    full_name = pgettext_lazy("thread moderation action name", "Hide thread")
    button_label = pgettext_lazy("thread moderation button label", "Hide")
    form_class = HideForm
    template_name = "misago/moderation/hide.html"

    def form_valid(self, form) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        hide_thread(
            thread, request.user, form.cleaned_data["hidden_reason"], request=request
        )

        thread_update = create_hidden_thread_update(
            thread, request.user, request=request
        )

        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread hidden"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class UnhideThreadModerationAction(ThreadModerationAction):
    id = "unhide"
    button_label = pgettext_lazy("thread moderation button label", "Unhide")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        unhide_thread(thread, request=request)

        thread_update = create_unhidden_thread_update(
            thread, request.user, request=request
        )

        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread unhidden"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class ApproveThreadModerationAction(ThreadModerationAction):
    id = "approve"
    button_label = pgettext_lazy("thread moderation button label", "Approve")

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        approve_thread(thread, request=request)

        thread_update = create_approved_thread_update(
            thread, request.user, request=request
        )

        self.send_notifications()

        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread approved"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)

    def send_notifications(self):
        pass


class ApprovePrivateThreadModerationAction(ApproveThreadModerationAction):
    def send_notifications(self):
        thread = self.thread

        prefetch_private_thread_member_ids([thread])
        member_ids = thread.private_thread_member_ids
        if thread.starter_id in member_ids:
            member_ids.remove(thread.starter_id)

        notify_on_new_private_thread.delay(thread.starter_id, thread.id, member_ids)


class RequireThreadReplyApprovalModerationAction(ThreadModerationAction):
    id = "require_reply_approval"
    button_label = pgettext_lazy(
        "thread moderation button label", "Require reply approval"
    )

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        require_thread_reply_approval(thread, request=request)

        thread_update = create_required_reply_approval_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            self.request,
            pgettext("thread moderation success", "Reply approval required"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class RemoveThreadReplyApprovalModerationAction(ThreadModerationAction):
    id = "remove_reply_approval"
    button_label = pgettext_lazy(
        "thread moderation button label", "Remove reply approval"
    )

    def execute(self) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        set_thread_has_updates(thread, commit=False)
        remove_thread_reply_approval(thread, request=request)

        thread_update = create_removed_reply_approval_thread_update(
            thread, request.user, request=request
        )

        messages.success(
            self.request,
            pgettext("thread moderation success", "Reply approval removed"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class MoveThreadModerationAction(FormMixin, ThreadModerationAction):
    id = "move"
    full_name = pgettext_lazy("thread moderation action name", "Move thread")
    button_label = pgettext_lazy("thread moderation button label", "Move")
    form_class = MoveThreadForm
    template_name = "misago/moderation/move.html"

    def get_form(self, form_submitted: bool):
        kwargs = {
            "request": self.request,
            "prefix": self.form_prefix,
            "disallowed_categories": [self.thread.category_id],
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationActionResult:
        request = self.request
        thread = self.thread

        old_category = self.category
        new_category = form.cleaned_data["category"]

        set_thread_has_updates(thread, commit=False)
        move_thread(thread, new_category, request=request)
        thread_update = create_moved_thread_update(
            thread, old_category, request.user, request=request
        )

        synchronize_categories.delay([old_category.id, new_category.id])

        messages.success(
            self.request,
            pgettext("thread moderation success", "Thread moved"),
        )

        return ModerationActionResult.from_updated_thread(thread, thread_update)


class MergeThreadModerationAction(FormMixin, ThreadModerationAction):
    id = "merge"
    full_name = pgettext_lazy("thread moderation action name", "Merge thread")
    button_label = pgettext_lazy("thread moderation button label", "Merge")
    form_class = MergeThreadForm
    template_name = "misago/moderation/merge_thread.html"

    def get_form(self, form_submitted: bool):
        kwargs = {
            "request": self.request,
            "prefix": self.form_prefix,
            "thread": self.thread,
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationActionResult:
        request = self.request
        thread = self.thread
        other_thread = form.cleaned_data["other_thread"]

        categories = [thread.category_id]
        if thread.category_id != other_thread.category_id:
            categories.append(other_thread.category_id)

        if form.cleaned_data["direction"] == "other":
            final_thread = other_thread
            merge_threads(other_thread, [thread], {}, request)

            create_merged_thread_update(
                other_thread, thread, self.request.user, request=request
            )
        else:
            final_thread = thread
            merge_threads(thread, [other_thread], {}, request)

            create_merged_thread_update(
                thread, other_thread, self.request.user, request=request
            )

        synchronize_thread(final_thread, request=request)

        synchronize_categories.delay(list(categories))
        delete_duplicate_watched_threads.delay(final_thread.id)

        messages.success(
            self.request,
            pgettext("thread moderation success", "Threads merged"),
        )

        return ModerationActionResult(
            redirect=self.get_redirect_url(final_thread),
        )

    def get_redirect_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_post_redirect_url(thread.last_post)


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
