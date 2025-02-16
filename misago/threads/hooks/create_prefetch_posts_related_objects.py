from typing import TYPE_CHECKING, Iterable, Protocol

from ...attachments.models import Attachment
from ...categories.models import Category
from ...conf.dynamicsettings import DynamicSettings
from ...permissions.proxy import UserPermissionsProxy
from ...plugins.hooks import FilterHook
from ..models import Post, Thread

if TYPE_CHECKING:
    from ...users.models import User
    from ..prefetch import PrefetchPostsRelatedObjects


class CreatePrefetchPostsRelatedObjectsHookAction(Protocol):
    """
    A standard Misago function used to create a `PrefetchPostsRelatedObjects`
    object, which is used to prefetch related objects for posts displayed on
    a thread replies page.

    # Arguments

    ## `settings: DynamicSettings`

    The `DynamicSettings` object.

    ## `permissions: UserPermissionsProxy`

    The `UserPermissionsProxy` object for current user.

    ## `posts: Iterable[Post]`

    Iterable of `Post` instances to prefetch related objects for.

    ## `categories: Iterable[Category] | None = None`

    Iterable of categories that were already loaded. Defaults to `None` if not
    provided.

    ## `threads: Iterable[Thread] | None = None`

    Iterable of threads that were already loaded. Defaults to `None` if not provided.

    ## `attachments: Iterable[Attachment] | None = None`

    Iterable of attachments that were already loaded. Defaults to `None` if not
    provided.

    ## `users: Iterable["User"] | None = None`

    Iterable of users that were already loaded. Defaults to `None` if not provided.

    # Return value

    A `PrefetchPostsRelatedObjects` object to use to fetch related objects.
    """

    def __call__(
        self,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        posts: Iterable[Post],
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
    ) -> "PrefetchPostsRelatedObjects": ...


class CreatePrefetchPostsRelatedObjectsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreatePrefetchPostsRelatedObjectsHookAction`

    A standard Misago function used to create a `PrefetchPostsRelatedObjects`
    object, which is used to prefetch related objects for posts displayed on
    a thread replies page.

    See the [action](#action) section for details.

    ## `settings: DynamicSettings`

    The `DynamicSettings` object.

    ## `permissions: UserPermissionsProxy`

    The `UserPermissionsProxy` object for current user.

    ## `posts: Iterable[Post]`

    Iterable of `Post` instances to prefetch related objects for.

    ## `categories: Iterable[Category] | None = None`

    Iterable of categories that were already loaded. Defaults to `None` if not
    provided.

    ## `threads: Iterable[Thread] | None = None`

    Iterable of threads that were already loaded. Defaults to `None` if not provided.

    ## `attachments: Iterable[Attachment] | None = None`

    Iterable of attachments that were already loaded. Defaults to `None` if not
    provided.

    ## `users: Iterable["User"] | None = None`

    Iterable of users that were already loaded. Defaults to `None` if not provided.

    # Return value

    A `PrefetchPostsRelatedObjects` object to use to fetch related objects.
    """

    def __call__(
        self,
        action: CreatePrefetchPostsRelatedObjectsHookAction,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        posts: Iterable[Post],
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
    ) -> "PrefetchPostsRelatedObjects": ...


class CreatePrefetchPostsRelatedObjectsHook(
    FilterHook[
        CreatePrefetchPostsRelatedObjectsHookAction,
        CreatePrefetchPostsRelatedObjectsHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to create a
    `PrefetchPostsRelatedObjects` object, which prefetches related objects for
    posts displayed on a thread replies page.

    `PrefetchPostsRelatedObjects` is initialized with settings, user permissions,
    a list of posts for which related objects need to be prefetched, and lists
    of other already available objects.

    The object itself does not implement prefetch logic but instead maintains
    a list of prefetch operations to be executed to fetch the objects required
    for displaying posts on a thread's page.

    Additional prefetch operations can be added using the add_operation method.

    # Example

    The code below implements a custom filter function that includes a new
    prefetch operation:

    ```python
    from typing import Iterable

    from misago.attachments.models import Attachment
    from misago.categories.models import Category
    from misago.conf.dynamicsettings import DynamicSettings
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.plugins.hooks import FilterHook
    from misago.threads.models import Post, Thread
    from misago.threads.prefetch import PrefetchPostsRelatedObjects
    from misago.users.models import User

    from .plugin.models import PluginModel


    def fetch_posts_plugin_data(
        data: dict,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
    ):
        data["plugin_models"] = {}
        ids_to_fetch: set[int] = set()

        for post in data["posts"].values():
            ids_to_fetch.add(post.plugin_data["plugin_object_id"])

        if ids_to_fetch:
            queryset = PluginModel.objects.filter(id__in=ids_to_fetch)
            data["plugin_models"] = {u.id: u for u in queryset}


    @create_prefetch_posts_related_objects_hook.append_filter
    def include_custom_filter(
        action: CreatePrefetchPostsRelatedObjectsHookAction,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        posts: Iterable[Post],
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
    ) -> PrefetchPostsRelatedObjects:
        prefetch = action(
            settings,
            permissions,
            posts,
            categories=categories,
            threads=threads,
            attachments=attachments,
            users=users,
        )

        prefetch.add_operation(fetch_posts_plugin_data)

        return prefetch
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CreatePrefetchPostsRelatedObjectsHookAction,
        settings: DynamicSettings,
        permissions: UserPermissionsProxy,
        posts: Iterable[Post],
        *,
        categories: Iterable[Category] | None = None,
        threads: Iterable[Thread] | None = None,
        attachments: Iterable[Attachment] | None = None,
        users: Iterable["User"] | None = None,
    ) -> "PrefetchPostsRelatedObjects":
        return super().__call__(
            action,
            settings,
            permissions,
            posts,
            categories=categories,
            threads=threads,
            attachments=attachments,
            users=users,
        )


create_prefetch_posts_related_objects_hook = CreatePrefetchPostsRelatedObjectsHook(
    cache=False
)
