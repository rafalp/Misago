# `create_prefetch_posts_feed_related_objects_hook`

This hook wraps the standard function Misago uses to create a `PrefetchPostsFeedRelatedObjects` object, which is used to prefetch related objects for items displayed in a posts feed.

The object itself does not implement prefetch logic but instead maintains a list of prefetch operations to be executed in order to fetch the objects from the database.

Additional prefetch operations can be added using the `add`, `add_after` and `add_before` methods.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import create_prefetch_posts_feed_related_objects_hook
```


## Filter

```python
def custom_create_prefetch_posts_feed_related_objects_filter(
    action: CreatePrefetchPostsFeedRelatedObjectsHookAction,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None=None,
    threads: Iterable[Thread] | None=None,
    thread_updates: Iterable[ThreadUpdate] | None=None,
    attachments: Iterable[Attachment] | None=None,
    users: Iterable['User'] | None=None,
) -> 'PrefetchPostsFeedRelatedObjects':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreatePrefetchPostsFeedRelatedObjectsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `settings: DynamicSettings`

The `DynamicSettings` object.


#### `permissions: UserPermissionsProxy`

The `UserPermissionsProxy` object for current user.


#### `posts: Iterable[Post]`

Iterable of `Post` instances to prefetch related objects for.


#### `categories: Iterable[Category] | None = None`

Iterable of categories that were already loaded. Defaults to `None` if not provided.


#### `threads: Iterable[Thread] | None = None`

Iterable of threads that were already loaded. Defaults to `None` if not provided.


#### `thread_updates: Iterable[ThreadUpdate] | None = None,`

Iterable of `ThreadUpdate` instances to prefetch related objects for. Defaults to `None` if not provided.


#### `attachments: Iterable[Attachment] | None = None`

Iterable of attachments that were already loaded. Defaults to `None` if not provided.


#### `users: Iterable["User"] | None = None`

Iterable of users that were already loaded. Defaults to `None` if not provided.


### Return value

A `PrefetchPostsFeedRelatedObjects` object to use to fetch related objects.


## Action

```python
def create_prefetch_posts_feed_related_objects_action(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None=None,
    threads: Iterable[Thread] | None=None,
    thread_updates: Iterable[ThreadUpdate] | None=None,
    attachments: Iterable[Attachment] | None=None,
    users: Iterable['User'] | None=None,
) -> 'PrefetchPostsFeedRelatedObjects':
    ...
```

Misago function used to create a `PrefetchPostsFeedRelatedObjects` object, which is used to prefetch related objects for items displayed on a posts feed.


### Arguments

#### `settings: DynamicSettings`

The `DynamicSettings` object.


#### `permissions: UserPermissionsProxy`

The `UserPermissionsProxy` object for current user.


#### `posts: Iterable[Post]`

Iterable of `Post` instances to prefetch related objects for.


#### `categories: Iterable[Category] | None = None`

Iterable of categories that were already loaded. Defaults to `None` if not provided.


#### `threads: Iterable[Thread] | None = None`

Iterable of threads that were already loaded. Defaults to `None` if not provided.


#### `thread_updates: Iterable[ThreadUpdate] | None = None,`

Iterable of `ThreadUpdate` instances to prefetch related objects for. Defaults to `None` if not provided.


#### `attachments: Iterable[Attachment] | None = None`

Iterable of attachments that were already loaded. Defaults to `None` if not provided.


#### `users: Iterable["User"] | None = None`

Iterable of users that were already loaded. Defaults to `None` if not provided.


### Return value

A `PrefetchPostsFeedRelatedObjects` object to use to fetch related objects.


## Example

The code below implements a custom filter function that includes a new prefetch operation:

```python
from typing import Iterable

from misago.attachments.models import Attachment
from misago.categories.models import Category
from misago.conf.dynamicsettings import DynamicSettings
from misago.permissions.proxy import UserPermissionsProxy
from misago.plugins.hooks import FilterHook
from misago.threads.models import Post, Thread
from misago.threads.prefetch import PrefetchPostsFeedRelatedObjects
from misago.threadupdates.models import ThreadUpdate
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


@create_prefetch_posts_feed_related_objects_hook.append_filter
def include_custom_filter(
    action: CreatePrefetchPostsFeedRelatedObjectsHookAction,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None = None,
    threads: Iterable[Thread] | None = None,
    thread_updates: Iterable[ThreadUpdate] | None = None,
    attachments: Iterable[Attachment] | None = None,
    users: Iterable["User"] | None = None,
) -> PrefetchPostsFeedRelatedObjects:
    prefetch = action(
        settings,
        permissions,
        posts,
        categories=categories,
        threads=threads,
        thread_updates=thread_updates,
        attachments=attachments,
        users=users,
    )

    prefetch.add_operation(fetch_posts_plugin_data)

    return prefetch
```