from typing import TYPE_CHECKING, Iterable, Protocol

from django.conf import settings as dj_settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import Http404

from ..attachments.models import Attachment
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..conf.dynamicsettings import DynamicSettings
from ..permissions.attachments import check_download_attachment_permission
from ..permissions.generic import (
    check_access_category_permission,
    check_access_post_permission,
    check_access_thread_permission,
)
from ..permissions.proxy import UserPermissionsProxy
from ..permissions.checkutils import check_permissions
from ..privatethreads.members import prefetch_private_thread_member_ids
from ..threadupdates.models import ThreadUpdate
from ..users.models import Group
from .hooks import create_prefetch_posts_feed_related_objects_hook
from .models import Post, Thread

if TYPE_CHECKING:
    from ..users.models import User


__all__ = [
    "PrefetchPostsFeedRelatedObjects",
    "PrefetchPostsFeedRelationsOperation",
    "prefetch_posts_feed_related_objects",
]


def prefetch_posts_feed_related_objects(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    thread_updates: Iterable[ThreadUpdate] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable["User"] | None = None,
) -> dict:
    prefetch = create_prefetch_posts_feed_related_objects_hook(
        _create_prefetch_posts_feed_related_objects_action,
        settings,
        permissions,
        posts,
        categories=categories,
        threads=threads,
        thread_updates=thread_updates,
        attachments=attachments,
        users=users,
    )
    return prefetch()


def _create_prefetch_posts_feed_related_objects_action(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    thread_updates: Iterable[ThreadUpdate] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable["User"] | None = None,
) -> "PrefetchPostsFeedRelatedObjects":
    prefetch = PrefetchPostsFeedRelatedObjects(
        settings,
        permissions,
        categories=categories,
        threads=threads,
        posts=posts,
        thread_updates=thread_updates,
        attachments=attachments,
        users=users,
    )

    prefetch.add(find_attachment_ids)
    prefetch.add(fetch_attachments)
    prefetch.add(find_post_ids)
    prefetch.add(fetch_posts)
    prefetch.add(find_thread_ids)
    prefetch.add(fetch_threads)
    prefetch.add(find_category_ids)
    prefetch.add(fetch_categories)
    prefetch.add(fetch_private_threads_members)
    prefetch.add(find_users_ids)
    prefetch.add(fetch_users)
    prefetch.add(fetch_users_groups)
    prefetch.add(check_categories_permissions)
    prefetch.add(check_threads_permissions)
    prefetch.add(check_posts_permissions)
    prefetch.add(check_attachments_permissions)

    return prefetch


class PrefetchPostsFeedRelationsOperation(Protocol):
    def __call__(
        self,
        data: dict,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
    ) -> None:
        pass


class PrefetchPostsFeedRelatedObjects:
    operations: list[PrefetchPostsFeedRelationsOperation]

    settings: DynamicSettings
    permissions: UserPermissionsProxy

    categories: list[Category]
    threads: list[Thread]
    posts: list[Post]
    thread_updates: list[ThreadUpdate]
    attachments: list[Attachment]
    users: list["User"]
    extra_kwargs: dict

    def __init__(
        self,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        *,
        posts: Iterable[Post],
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        thread_updates: Iterable[ThreadUpdate] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
        **kwargs,
    ):
        self.operations = []

        self.settings = settings
        self.permissions = permissions

        self.categories = categories or []
        self.threads = threads or []
        self.posts = list(posts)
        self.thread_updates = thread_updates or []
        self.attachments = attachments or []
        self.users = users or []

        if permissions.user.is_authenticated and permissions.user not in self.users:
            self.users.append(permissions.user)

        self.extra_kwargs = kwargs

    def __call__(self) -> dict:
        data = {
            "category_ids": set(),
            "thread_ids": set(),
            "post_ids": set(),
            "attachment_ids": set(),
            "user_ids": set(),
            "categories": {c.id: c for c in self.categories if c.id},
            "visible_categories": {c.id for c in self.categories if c.id},
            "threads": {t.id: t for t in self.threads if t.id},
            "visible_threads": {t.id for t in self.threads if t.id},
            "posts": {p.id: p for p in self.posts if p.id},
            "visible_posts": {p.id for p in self.posts if p.id},
            "thread_updates": {u.id: u for u in self.thread_updates},
            "visible_thread_updates": {u for u in self.thread_updates},
            "attachments": {a.id: a for a in self.attachments},
            "attachment_errors": {},
            "users": {u.id: u for u in self.users},
            "extra_kwargs": self.extra_kwargs,
            "metadata": {},
        }

        if self.posts and not self.posts[0].id:
            data["metadata"] = self.posts[0].metadata

        for op in self.operations:
            op(data, self.settings, self.permissions)

        return data

    def __contains__(self, op: PrefetchPostsFeedRelationsOperation) -> bool:
        return op in self.operations

    def add(self, op: PrefetchPostsFeedRelationsOperation):
        self.operations.append(op)

    def add_before(
        self,
        before: PrefetchPostsFeedRelationsOperation,
        op: PrefetchPostsFeedRelationsOperation,
    ):
        success = False
        new_operations: list[PrefetchPostsFeedRelationsOperation] = []

        for existing_step in self.operations:
            if existing_step == before:
                new_operations.append(op)
                success = True
            new_operations.append(existing_step)

        self.operations = new_operations

        if not success:
            raise ValueError(
                f"Operation '{before}' doesn't exist in this loader instance"
            )

    def add_after(
        self,
        after: PrefetchPostsFeedRelationsOperation,
        op: PrefetchPostsFeedRelationsOperation,
    ):
        success = False
        new_operations: list[PrefetchPostsFeedRelationsOperation] = []

        for existing_step in self.operations:
            new_operations.append(existing_step)
            if existing_step == after:
                new_operations.append(op)
                success = True

        self.operations = new_operations

        if not success:
            raise ValueError(
                f"Operation '{after}' doesn't exist in this loader instance"
            )


def find_category_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        if post.category_id:
            data["category_ids"].add(post.category_id)

    for thread in data["threads"].values():
        if thread.category_id:
            data["category_ids"].add(thread.category_id)

    for thread_update in data["thread_updates"].values():
        if context_id := thread_update.get_context_id("misago_categories.category"):
            data["category_ids"].add(context_id)

    for attachment in data["attachments"].values():
        if attachment.category_id:
            data["category_ids"].add(attachment.category_id)


def fetch_categories(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["category_ids"].difference(data["categories"]):
        queryset = Category.objects.filter(id__in=ids_to_fetch)
        data["categories"].update({c.id: c for c in queryset})


def find_thread_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        if post.thread_id:
            data["thread_ids"].add(post.thread_id)

    for thread_update in data["thread_updates"].values():
        if context_id := thread_update.get_context_id("misago_threads.thread"):
            data["thread_ids"].add(context_id)

    for attachment in data["attachments"].values():
        if attachment.thread_id:
            data["thread_ids"].add(attachment.thread_id)


def fetch_threads(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["thread_ids"].difference(data["threads"]):
        queryset = Thread.objects.filter(id__in=ids_to_fetch)
        data["threads"].update({t.id: t for t in queryset})


def fetch_private_threads_members(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    private_threads: list[Thread] = []
    for thread in data["threads"].values():
        category = data["categories"][thread.category_id]
        if category.tree_id == CategoryTree.PRIVATE_THREADS:
            private_threads.append(thread)

    if private_threads:
        prefetch_private_thread_member_ids(private_threads)


def find_post_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for thread_update in data["thread_updates"].values():
        if context_id := thread_update.get_context_id("misago_threads.post"):
            data["post_ids"].add(context_id)

    for attachment in data["attachments"].values():
        if attachment.post_id:
            data["post_ids"].add(attachment.post_id)

    quoted_posts: set[int] = set()
    for post in data["posts"].values():
        if related_posts := post.metadata.get("posts"):
            quoted_posts.update(related_posts)

    if extra_posts := data["metadata"].get("posts"):
        quoted_posts.update(extra_posts)

    if quoted_posts := sorted(quoted_posts)[: dj_settings.MISAGO_QUOTED_POSTS_LIMIT]:
        data["post_ids"].update(quoted_posts)


def fetch_posts(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["post_ids"].difference(data["posts"]):
        queryset = Post.objects.filter(id__in=ids_to_fetch)
        data["posts"].update({p.id: p for p in queryset})


def find_attachment_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        data["attachment_ids"].update(post.metadata.get("attachments", []))

    for thread_update in data["thread_updates"].values():
        if context_id := thread_update.get_context_id("misago_attachments.attachment"):
            data["attachment_ids"].add(context_id)

    if extra_attachments := data["metadata"].get("attachments"):
        data["attachment_ids"].update(extra_attachments)


def fetch_attachments(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    queryset = Attachment.objects.filter(post_id__in=data["posts"])

    embedded_attachments = data["attachment_ids"].difference(data["attachments"])
    if settings.additional_embedded_attachments_limit and embedded_attachments:
        queryset = queryset.union(
            Attachment.objects.filter(id__in=embedded_attachments, post__isnull=False)
            .exclude(post_id__in=data["posts"])
            .order_by("-id")[: settings.additional_embedded_attachments_limit]
        )

    data["attachments"].update({a.id: a for a in queryset})


def check_categories_permissions(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for category in tuple(data["categories"].values()):
        if category.id in data["visible_categories"]:
            continue  # Skip previously checked categories

        try:
            check_access_category_permission(permissions, category)
        except (Http404, PermissionDenied):
            data["categories"].pop(category.id)

    data.pop("visible_categories")


def check_threads_permissions(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for thread in tuple(data["threads"].values()):
        if thread.id in data["visible_threads"]:
            continue  # Skip previously checked threads

        try:
            if thread.category_id not in data["categories"]:
                raise Http404()

            check_access_thread_permission(
                permissions,
                data["categories"][thread.category_id],
                thread,
            )
        except (Http404, PermissionDenied):
            data["threads"].pop(thread.id)

    data.pop("visible_threads")


def check_posts_permissions(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in tuple(data["posts"].values()):
        if post.id in data["visible_posts"]:
            continue  # Skip previously checked posts

        try:
            if post.category_id not in data["categories"]:
                raise Http404()
            if post.thread_id not in data["threads"]:
                raise Http404()

            check_access_post_permission(
                permissions,
                data["categories"][post.category_id],
                data["threads"][post.thread_id],
                post,
            )
        except (Http404, PermissionDenied):
            data["posts"].pop(post.id)

    data.pop("visible_posts")


def check_attachments_permissions(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    attachments_list = sorted(
        data["attachments"].values(), reverse=True, key=lambda a: a.id
    )

    accessible_attachments: dict[int, Attachment] = {}
    for attachment in attachments_list:
        try:
            if attachment.category_id:
                attachment.category = data["categories"][attachment.category_id]
            if attachment.thread_id:
                attachment.thread = data["threads"][attachment.thread_id]
            if attachment.post_id:
                attachment.post = data["posts"][attachment.post_id]
        except KeyError:
            continue

        with check_permissions() as can_download:
            check_download_attachment_permission(
                permissions,
                attachment.category,
                attachment.thread,
                attachment.post,
                attachment,
            )

        if can_download:
            accessible_attachments[attachment.id] = attachment
        else:
            data["attachment_errors"][attachment.id] = can_download

    data["attachments"] = accessible_attachments


def find_users_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        data["user_ids"].add(post.poster_id)

    for thread_update in data["thread_updates"].values():
        if thread_update.actor_id:
            data["user_ids"].add(thread_update.actor_id)
        if context_id := thread_update.get_context_id("misago_users.user"):
            data["user_ids"].add(context_id)


def fetch_users(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["user_ids"].difference(data["users"]):
        queryset = get_user_model().objects.filter(id__in=ids_to_fetch, is_active=True)
        data["users"].update({u.id: u for u in queryset})


def fetch_users_groups(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    users = data["users"].values()

    ids_to_fetch: set[int] = set(u.group_id for u in users)
    if ids_to_fetch:
        groups = {g.id: g for g in Group.objects.filter(id__in=ids_to_fetch)}
        for user in users:
            user.group = groups[user.group_id]
