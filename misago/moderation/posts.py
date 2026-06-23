from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext, pgettext_lazy

from ..categories.models import Category
from ..categories.tasks import synchronize_categories
from ..permissions.proxy import UserPermissionsProxy
from ..threads.delete import delete_post
from ..threads.hide import hide_post, unhide_post
from ..threads.lock import lock_post, unlock_post
from ..threads.models import Thread
from ..threads.synchronize import synchronize_thread
from .actions import (
    ConfirmMixin,
    FormMixin,
    ModerationResult,
    PostsModerationAction,
)
from .forms import HideForm, SplitPostsForm
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
        SplitPostsModerationAction,
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
        SplitPostsModerationAction,
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
                        "The thread's original post can't be hidden.",
                    )
                )

        for post in self.posts:
            print(post.is_hidden)
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


class SplitPostsModerationAction(FormMixin, PostsModerationAction):
    id = "split"
    full_name = "Split posts into a new thread"
    button_label = "Split"
    form_class = SplitPostsForm
    template_name = "misago/moderation/split_posts.html"

    def validate(self):
        for post in self.posts:
            if post.id == self.thread.first_post:
                raise ValidationError(
                    pgettext(
                        "post moderation validation",
                        "The first post in a thread can't be split.",
                    )
                )

    def form_valid(self, form) -> ModerationResult:
        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts were split into a new thread."),
        )

        if form.cleaned_data["category"] == self.category.id:
            new_category = self.category
            sync_categories_ids = [new_category.id]
        else:
            new_category = Category.objects.get(id=form.cleaned_data["category"])
            sync_categories_ids = [self.category.id, new_category.id]

        from misago.core.utils import slugify

        first_post = self.posts[0]
        if first_post.poster:
            poster_username = first_post.post.username
            poster_slug = first_post.post.slug
        else:
            poster_username = first_post.poster_name
            poster_slug = slugify(first_post.poster_name)

        new_thread = Thread.objects.create(
            category=new_category,
            title=form.cleaned_data["title"],
            slug=slugify(form.cleaned_data["title"]),
            started_at=first_post.posted_at,
            last_posted_at=first_post.posted_at,
            first_post=first_post,
            last_post=first_post,
            starter_name=poster_username,
            starter_slug=poster_slug,
            last_poster_name=poster_username,
            last_poster_slug=poster_slug,
        )

        for post in self.posts:
            post.category = new_category
            post.thread = new_thread
            post.save()

        synchronize_thread(new_thread, request=self.request)
        synchronize_categories.delay(sync_categories_ids)

        return ModerationResult(
            deleted_items=[post.id for post in self.posts],
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
                        "post moderation validation",
                        "The first post in a thread can't be deleted.",
                    )
                )

    def confirmed(self) -> ModerationResult:
        for post in self.posts:
            delete_post(post)

        synchronize_thread(self.thread)
        synchronize_categories.delay([self.thread.category_id])

        messages.success(
            self.request,
            pgettext("posts moderation success", "Posts deleted"),
        )

        return ModerationResult(
            deleted_items=[post.id for post in self.posts],
        )
