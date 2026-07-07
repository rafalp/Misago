from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import Form
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..attachments.models import Attachment
from ..categories.tasks import synchronize_categories
from ..notifications.tasks import notify_on_new_thread_reply
from ..permissions.proxy import UserPermissionsProxy
from ..postedits.create import create_post_edit
from ..threads.approve import approve_post
from ..threads.create import create_thread
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.merge import get_post_merge_conflicts, merge_posts
from ..threads.models import Thread
from ..threads.move import move_post
from ..threads.synchronize import synchronize_thread
from ..threadupdates.create import (
    create_deleted_posts_thread_update,
    create_moved_posts_from_thread_update,
    create_moved_posts_to_thread_update,
    create_split_posts_from_thread_update,
    create_split_posts_into_thread_update,
)
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    PostsModerationAction,
)
from .forms import HideForm, MergePostsForm, MovePostsForm, SplitPostsForm
from .hooks import (
    get_private_thread_posts_moderation_actions_hook,
    get_thread_posts_moderation_actions_hook,
)


def get_thread_posts_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    return get_thread_posts_moderation_actions_hook(
        _get_thread_posts_moderation_actions_action,
        user_permissions,
        thread,
        request,
    )


def _get_thread_posts_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    if not user_permissions.is_category_moderator(thread.category_id):
        return []

    return [
        LockPostsModerationAction,
        UnlockPostsModerationAction,
        HidePostsModerationAction,
        UnhidePostsModerationAction,
        ApprovePostsModerationAction,
        SplitPostsModerationAction,
        MovePostsModerationAction,
        MergePostsModerationAction,
        DeletePostsModerationAction,
    ]


def get_private_thread_posts_moderation_actions(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    return get_private_thread_posts_moderation_actions_hook(
        _get_private_thread_posts_moderation_actions_action,
        user_permissions,
        thread,
        request,
    )


def _get_private_thread_posts_moderation_actions_action(
    user_permissions: UserPermissionsProxy,
    thread: Thread,
    request: HttpRequest | None = None,
) -> list[type[PostsModerationAction]]:
    if not user_permissions.is_private_threads_moderator:
        return []

    return [
        LockPostsModerationAction,
        UnlockPostsModerationAction,
        HidePostsModerationAction,
        UnhidePostsModerationAction,
        ApprovePostsModerationAction,
        MergePostsModerationAction,
        DeletePostsModerationAction,
    ]


class LockPostsModerationAction(PostsModerationAction):
    id = "lock"
    button_label = pgettext_lazy("posts moderation button label", "Lock")

    def validate(self):
        for post in self.posts:
            if not post.is_locked:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already locked.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if not post.is_locked]

        for post in valid_posts:
            lock_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts locked"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class UnlockPostsModerationAction(PostsModerationAction):
    id = "unlock"
    button_label = pgettext_lazy("posts moderation button label", "Unlock")

    def validate(self):
        for post in self.posts:
            if post.is_locked:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already unlocked.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if post.is_locked]

        for post in valid_posts:
            unlock_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts unlocked"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class HidePostsModerationAction(FormMixin, PostsModerationAction):
    id = "hide"
    full_name = pgettext_lazy("posts moderation action name", "Hide posts")
    button_label = pgettext_lazy("posts moderation button label", "Hide")

    form_class = HideForm
    template_name = "misago/moderation/hide.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "posts moderation validation",
                        "Thread's original post can't be hidden.",
                    )
                )

        for post in self.posts:
            if not post.is_hidden:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already hidden.")
        )

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if not post.is_hidden]
        hidden_reason = form.cleaned_data["hidden_reason"]

        for post in valid_posts:
            hide_post(post, request.user, hidden_reason, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts hidden"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class UnhidePostsModerationAction(PostsModerationAction):
    id = "unhide"
    button_label = pgettext_lazy("posts moderation button label", "Unhide")

    def validate(self):
        for post in self.posts:
            if post.is_hidden:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already unhidden.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        valid_posts = [post for post in self.posts if post.is_hidden]

        for post in valid_posts:
            unhide_post(post, request=request)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts unhidden"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class ApprovePostsModerationAction(PostsModerationAction):
    id = "approve"
    button_label = pgettext_lazy("posts moderation button label", "Approve")

    def validate(self):
        for post in self.posts:
            if post.is_unapproved:
                return

        raise ValidationError(
            pgettext("posts moderation validation", "Posts are already approved.")
        )

    def execute(self) -> ModerationResult:
        request = self.request
        thread = self.thread
        valid_posts = [post for post in self.posts if post.is_unapproved]

        for post in valid_posts:
            approve_post(post, request=request)

        synchronize_thread(thread, request=request)

        for post in valid_posts:
            notify_on_new_thread_reply.delay(post.id)

        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts approved"),
        )

        return ModerationResult(
            updated_items=[post.id for post in valid_posts],
        )


class SplitPostsModerationAction(FormMixin, PostsModerationAction):
    id = "split"
    full_name = "Split posts into a new thread"
    button_label = "Split"

    form_class = SplitPostsForm
    template_name = "misago/moderation/split_posts.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be split.",
                    )
                )

    def get_form(self, form_submitted: bool) -> Form:
        kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "initial": {
                "category": self.thread.category_id,
            },
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        posts = self.posts
        posts_count = len(posts)

        new_thread = create_thread(
            form.cleaned_data["category"],
            form.cleaned_data["title"],
            pinned=form.cleaned_data["pin"],
            is_locked=form.cleaned_data["is_locked"],
            is_hidden=form.cleaned_data["is_hidden"],
            request=request,
        )

        for post in posts:
            move_post(post, new_thread)

        thread_update = create_split_posts_from_thread_update(
            new_thread, thread, posts_count, request.user, request=request
        )
        create_split_posts_into_thread_update(
            thread, new_thread, posts_count, request.user, request=request
        )

        synchronize_thread(thread, request=request)
        synchronize_thread(new_thread, request=request)

        sync_categories_ids = list({thread.category_id, new_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts were split into a new thread."),
        )

        if form.cleaned_data["redirect_to"] == "new":
            return ModerationResult(redirect_to=self.get_thread_url(new_thread))

        return ModerationResult(
            deleted_items=[post.id for post in posts],
            thread_updates=[thread_update],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class MovePostsModerationAction(FormMixin, PostsModerationAction):
    id = "move"
    full_name = "Move posts to another thread"
    button_label = "Move"

    form_class = MovePostsForm
    template_name = "misago/moderation/move_posts.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be moved.",
                    )
                )

    def get_form(self, form_submitted: bool) -> Form:
        kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "current_thread": self.thread,
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        target_thread = form.cleaned_data["target_thread"]
        posts = self.posts
        posts_count = len(posts)

        for post in posts:
            move_post(post, target_thread)

        thread_update = create_moved_posts_from_thread_update(
            target_thread, thread, posts_count, request.user, request=request
        )
        create_moved_posts_to_thread_update(
            thread, target_thread, posts_count, request.user, request=request
        )

        synchronize_thread(thread, request=request)
        synchronize_thread(target_thread, request=request)

        sync_categories_ids = list({thread.category_id, target_thread.category_id})
        synchronize_categories.delay(sync_categories_ids)

        messages.success(
            self.request,
            pgettext(
                "posts moderation success", "Posts were moved to the target thread."
            ),
        )

        if form.cleaned_data["redirect_to"] == "target":
            return ModerationResult(redirect_to=self.get_thread_url(target_thread))

        return ModerationResult(
            deleted_items=[post.id for post in posts],
            thread_updates=[thread_update],
        )

    def get_thread_url(self, thread: Thread) -> str:
        from ..threads.views.backend import thread_backend

        return thread_backend.get_thread_url(thread)


class MergePostsModerationAction(FormMixin, PostsModerationAction):
    id = "merge"
    full_name = "Merge posts"
    button_label = "Merge"

    form_class = MergePostsForm
    template_name = "misago/moderation/merge_posts.html"

    def validate(self):
        posts = self.posts

        if len(posts) < 2:
            raise ValidationError(
                pgettext(
                    "posts moderation validation",
                    "Select at least two posts to merge.",
                )
            )

        posts = sorted(self.posts, key=lambda i: i.id)
        target, posts = posts[0], posts[1:]

        for post in posts:
            if (target.poster_id and target.poster_id != post.poster_id) or (
                not target.poster_id and post.poster_name != target.poster_name
            ):
                raise ValidationError(
                    pgettext(
                        "posts moderation validation",
                        "Merged posts must belong to the same user.",
                    )
                )

    def get_form(self, form_submitted: bool) -> Form:
        kwargs = {
            "prefix": self.form_prefix,
            "request": self.request,
            "conflicts": get_post_merge_conflicts(self.posts, self.request),
        }

        if form_submitted:
            return self.form_class(self.request.POST, **kwargs)

        return self.form_class(**kwargs)

    def form_valid(self, form) -> ModerationResult:
        request = self.request
        thread = self.thread
        edit_reason = form.cleaned_data["edit_reason"]
        posts = sorted(self.posts, key=lambda i: i.id)
        target, posts = posts[0], posts[1:]

        old_content = target.original
        attachments = []

        attachments_queryset = Attachment.objects.filter(post__in=self.posts).order_by(
            "-id"
        )
        for attachment in attachments_queryset:
            # A bit of black magic: by unsetting attachment post relations
            # we make 'create_post_edit' record attachment as new addition to a post
            if attachment.post_id != target.id:
                attachment.category = None
                attachment.thread = None
                attachment.post = None

            attachments.append(attachment)

        merge_posts(
            target,
            posts,
            form.get_conflicts_resolutions(),
            request.user,
            edit_reason,
            request=request,
        )

        create_post_edit(
            post=target,
            user=request.user,
            edit_reason=edit_reason,
            old_content=old_content,
            new_content=target.original,
            attachments=attachments,
            edited_at=target.updated_at,
            request=request,
        )

        synchronize_thread(thread, request=request)
        synchronize_categories.delay([thread.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts merged"),
        )

        return ModerationResult(
            updated_items=[target.id],
            deleted_items=[post.id for post in posts],
        )


class DeletePostsModerationAction(ConfirmMixin, PostsModerationAction):
    id = "delete"
    full_name = "Delete posts"
    button_label = "Delete"
    confirmation_message = pgettext_lazy(
        "posts moderation",
        "Are you sure you want to delete the selected posts? This action cannot be undone.",
    )

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post_id:
                raise ValidationError(
                    pgettext(
                        "posts moderation validation",
                        "The first post in a thread can't be deleted.",
                    )
                )

    def confirmed(self) -> ModerationResult:
        request = self.request
        thread = self.thread
        posts = self.posts

        for post in posts:
            delete_post(post)

        thread_update = create_deleted_posts_thread_update(
            thread, len(posts), request.user, request=request
        )

        synchronize_thread(thread)
        synchronize_categories.delay([thread.category_id])

        messages.success(
            request,
            pgettext("posts moderation success", "Posts deleted"),
        )

        return ModerationResult(
            deleted_items=[post.id for post in posts],
            thread_updates=[thread_update],
        )
