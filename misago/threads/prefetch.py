from typing import TYPE_CHECKING, Iterable, Protocol

from django.contrib.auth import get_user_model

from ..attachments.models import Attachment
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..conf.dynamicsettings import DynamicSettings
from ..permissions.attachments import check_download_attachment_permission
from ..permissions.posts import check_see_post_permission
from ..permissions.proxy import UserPermissionsProxy
from ..permissions.checkutils import check_permissions
from ..users.models import Group
from .hooks import create_prefetch_posts_related_objects_hook
from .models import Post, Thread
from .privatethreads import prefetch_private_thread_member_ids

if TYPE_CHECKING:
    from ..users.models import User
else:
    User = get_user_model()

__all__ = [
    "PrefetchPostsRelatedObjects",
    "PrefetchPostsRelationsOperation",
    "prefetch_posts_related_objects",
]


def prefetch_posts_related_objects(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable["User"] | None = None,
) -> dict:
    prefetch = create_prefetch_posts_related_objects_hook(
        _create_prefetch_posts_related_objects_action,
        settings,
        permissions,
        posts,
        categories=categories,
        threads=threads,
        attachments=attachments,
        users=users,
    )
    return prefetch()


def _create_prefetch_posts_related_objects_action(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable["User"] | None = None,
) -> "PrefetchPostsRelatedObjects":
    prefetch = PrefetchPostsRelatedObjects(
        settings,
        permissions,
        posts=posts,
        categories=categories,
        threads=threads,
        attachments=attachments,
        users=users,
    )

    prefetch.add_operation(find_attachment_ids)
    prefetch.add_operation(fetch_attachments)
    prefetch.add_operation(find_post_ids)
    prefetch.add_operation(fetch_posts)
    prefetch.add_operation(find_thread_ids)
    prefetch.add_operation(fetch_threads)
    prefetch.add_operation(find_category_ids)
    prefetch.add_operation(fetch_categories)
    prefetch.add_operation(fetch_private_threads_members)
    prefetch.add_operation(find_users_ids)
    prefetch.add_operation(fetch_users)
    prefetch.add_operation(fetch_users_groups)
    prefetch.add_operation(check_attachments_permissions)

    return prefetch


class PrefetchPostsRelationsOperation(Protocol):
    def __call__(
        self,
        data: dict,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
    ) -> None:
        pass


class PrefetchPostsRelatedObjects:
    ops: list[PrefetchPostsRelationsOperation]

    settings: DynamicSettings
    permissions: User

    categories: list[Category]
    threads: list[Thread]
    posts: list[Post]
    attachments: list[Attachment]
    users: list[User]
    extra_kwargs: dict

    def __init__(
        self,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        *,
        posts: Iterable[Post],
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
        **kwargs,
    ):
        self.ops = []

        self.settings = settings
        self.permissions = permissions

        self.categories = categories or []
        self.threads = threads or []
        self.posts = list(posts)
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
            "threads": {t.id: t for t in self.threads if t.id},
            "posts": {p.id: p for p in self.posts if p.id},
            "attachments": {a.id: a for a in self.attachments},
            "attachment_errors": {},
            "users": {u.id: u for u in self.users},
            "extra_kwargs": self.extra_kwargs,
        }

        for op in self.ops:
            op(data, self.settings, self.permissions)

        return data

    def add_operation(
        self,
        op: PrefetchPostsRelationsOperation,
        *,
        after: PrefetchPostsRelationsOperation | None = None,
        before: PrefetchPostsRelationsOperation | None = None,
    ):
        if after and before:
            raise ValueError("'after' and 'before' option's can't be used together")

        if after:
            inserted = False
            new_ops: list[PrefetchPostsRelationsOperation] = []

            for existing_step in self.ops:
                new_ops.append(existing_step)
                if existing_step == after:
                    new_ops.append(op)
                    inserted = True
            self.ops = new_ops

            if not inserted:
                raise ValueError(
                    f"Operation '{after}' doesn't exist in this loader instance"
                )

        elif before:
            prepended = False
            new_ops: list[PrefetchPostsRelationsOperation] = []

            for existing_step in self.ops:
                if existing_step == before:
                    new_ops.append(op)
                    prepended = True
                new_ops.append(existing_step)
            self.ops = new_ops

            if not prepended:
                raise ValueError(
                    f"Operation '{after}' doesn't exist in this loader instance"
                )

        else:
            self.ops.append(op)


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
    for attachment in data["attachments"].values():
        if attachment.post_id:
            data["post_ids"].add(attachment.post_id)


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


def fetch_attachments(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    visible_posts: list[int] = []
    for post in data["posts"].values():
        with check_permissions() as can_see:
            check_see_post_permission(
                permissions,
                post.category,
                post.thread,
                post,
            )

        if can_see:
            visible_posts.append(post.id)

    queryset = Attachment.objects.filter(post_id__in=visible_posts)

    if ids_to_fetch := data["attachment_ids"].difference(data["attachments"]):
        if settings.additional_embedded_attachments_limit:
            queryset = queryset.union(
                Attachment.objects.filter(id__in=ids_to_fetch, post__isnull=False)
                .exclude(post_id__in=visible_posts)
                .order_by("-id")[: settings.additional_embedded_attachments_limit]
            )

    data["attachments"].update({a.id: a for a in queryset})


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
        if attachment.category_id:
            attachment.category = data["categories"][attachment.category_id]
        if attachment.thread_id:
            attachment.thread = data["threads"][attachment.thread_id]
        if attachment.post_id:
            attachment.post = data["posts"][attachment.post_id]

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


def fetch_users(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["user_ids"].difference(data["users"]):
        queryset = User.objects.filter(id__in=ids_to_fetch, is_active=True)
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
