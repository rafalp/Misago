from typing import TYPE_CHECKING, Iterable, Protocol

from django.contrib.auth import get_user_model

from ..attachments.models import Attachment
from ..categories.models import Category
from ..conf.dynamicsettings import DynamicSettings
from ..permissions.attachments import check_download_attachment_permission
from ..permissions.proxy import UserPermissionsProxy
from ..permissions.checkutils import check_permissions
from .models import Post, Thread

if TYPE_CHECKING:
    from ..users.models import User
else:
    User = get_user_model()


def prefetch_posts_related_objects(
    posts: Iterable[Post],
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable[User] | None = None,
) -> dict:
    loader = PrefetchPostsRelatedObjects(
        settings,
        permissions,
        posts=posts,
        categories=categories,
        threads=threads,
        attachments=attachments,
        users=users,
    )

    loader.add_operation(find_attachment_ids)
    loader.add_operation(fetch_attachments)
    loader.add_operation(find_category_ids)
    loader.add_operation(find_thread_ids)
    loader.add_operation(find_post_ids)
    loader.add_operation(find_users_ids)
    loader.add_operation(fetch_categories)
    loader.add_operation(fetch_threads)
    loader.add_operation(fetch_posts)
    loader.add_operation(fetch_users)
    loader.add_operation(filter_attachments)

    return loader.fetch_data()


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
        users: Iterable[User] | None = None,
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

    def fetch_data(self) -> dict:
        data = {
            "category_ids": set(),
            "thread_ids": set(),
            "post_ids": set(),
            "attachment_ids": set(),
            "user_ids": set(),
            "categories": {c.id: c for c in self.categories},
            "threads": {t.id: t for t in self.threads},
            "posts": {p.id: p for p in self.posts},
            "attachments": {a.id: a for a in self.attachments},
            "attachment_errors": {},
            "users": {u.id: u for u in self.users},
            "extra_kwargs": self.extra_kwargs,
        }

        for op in self.ops:
            op(data, self.settings, self.permissions)

        return data


def find_category_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_thread_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_post_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def find_attachment_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        data["attachment_ids"].update(post.metadata.get("attachments", []))


def find_users_ids(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    for post in data["posts"].values():
        data["user_ids"].add(post.poster_id)


def fetch_categories(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def fetch_threads(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def fetch_posts(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    pass


def fetch_attachments(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    queryset = Attachment.objects.filter(post__in=data["posts"])

    if ids_to_fetch := data["attachment_ids"].difference(data["attachments"]):
        queryset = queryset.union(
            Attachment.objects.filter(id__in=ids_to_fetch).exclude(
                post__in=data["posts"]
            )[:10]
        )

    data["attachments"].update({a.id: a for a in queryset})


def fetch_users(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    if ids_to_fetch := data["user_ids"].difference(data["users"]):
        queryset = User.objects.filter(id__in=ids_to_fetch, is_active=True)
        data["users"].update({u.id: u for u in queryset})


def filter_attachments(
    data: dict,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
):
    attachments_list = sorted(
        data["attachments"].values(), reverse=True, key=lambda a: a.id
    )

    accessible_attachments: dict[int, Attachment] = {}
    for attachment in attachments_list:
        category = None
        thread = None
        post = None

        if attachment.category_id:
            category = data["categories"][attachment.category_id]
        if attachment.thread_id:
            thread = data["threads"][attachment.thread_id]
        if attachment.post_id:
            post = data["posts"][attachment.post_id]

        with check_permissions() as can_download:
            check_download_attachment_permission(
                permissions, category, thread, post, attachment
            )

        if can_download:
            accessible_attachments[attachment.id] = attachment
        else:
            data["attachment_errors"][attachment.id] = can_download

    data["attachments"] = accessible_attachments
