# `create_prefetch_post_feed_data_hook`

This hook wraps the standard function Misago uses to create a `PrefetchPostFeedData` object, which is used to prefetch data for a post feed.

The object itself does not implement prefetch logic, but instead contains a list of prefetch operations to be executed to fetch data from the database.

Additional prefetch operations can be added using the `add`, `add_after`, and `add_before` methods.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import create_prefetch_post_feed_data_hook
```


## Filter

```python
def custom_create_prefetch_post_feed_data_filter(
    action: CreatePrefetchPostFeedDataHookAction,
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None=None,
    threads: Iterable[Thread] | None=None,
    thread_updates: Iterable[ThreadUpdate] | None=None,
    attachments: Iterable[Attachment] | None=None,
    users: Iterable['User'] | None=None,
) -> 'PrefetchPostFeedData':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreatePrefetchPostFeedDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `settings: DynamicSettings`

The `DynamicSettings` object.


#### `permissions: UserPermissionsProxy`

The `UserPermissionsProxy` object for current user.


#### `posts: Iterable[Post]`

Iterable of `Post` instances to prefetch data for.


#### `categories: Iterable[Category] | None = None`

Iterable of `Category` instances that have already been loaded. Defaults to `None` if not provided.


#### `threads: Iterable[Thread] | None = None`

Iterable of `Thread` instances that have already been loaded. Defaults to `None` if not provided.


#### `thread_updates: Iterable[ThreadUpdate] | None = None`

Iterable of `ThreadUpdate` instances to prefetch data for. Defaults to `None` if not provided.


#### `attachments: Iterable[Attachment] | None = None`

Iterable of `Attachment` instances that have already been loaded. Defaults to `None` if not provided.


#### `users: Iterable["User"] | None = None`

Iterable of users that were already loaded. Defaults to `None` if not provided.


### Return value

A `PrefetchPostFeedData` object used to fetch post feed data.


## Action

```python
def create_prefetch_post_feed_data_action(
    settings: DynamicSettings,
    permissions: UserPermissionsProxy,
    posts: Iterable[Post],
    *,
    categories: Iterable[Category] | None=None,
    threads: Iterable[Thread] | None=None,
    thread_updates: Iterable[ThreadUpdate] | None=None,
    attachments: Iterable[Attachment] | None=None,
    users: Iterable['User'] | None=None,
) -> 'PrefetchPostFeedData':
    ...
```

Misago function used to create a `PrefetchPostFeedData` object for prefetching data used to display a post feed.


### Arguments

#### `settings: DynamicSettings`

The `DynamicSettings` object.


#### `permissions: UserPermissionsProxy`

The `UserPermissionsProxy` object for current user.


#### `posts: Iterable[Post]`

Iterable of `Post` instances to prefetch data for.


#### `categories: Iterable[Category] | None = None`

Iterable of `Category` instances that have already been loaded. Defaults to `None` if not provided.


#### `threads: Iterable[Thread] | None = None`

Iterable of `Thread` instances that have already been loaded. Defaults to `None` if not provided.


#### `thread_updates: Iterable[ThreadUpdate] | None = None`

Iterable of `ThreadUpdate` instances to prefetch data for. Defaults to `None` if not provided.


#### `attachments: Iterable[Attachment] | None = None`

Iterable of `Attachment` instances that have already been loaded. Defaults to `None` if not provided.


#### `users: Iterable["User"] | None = None`

Iterable of users that were already loaded. Defaults to `None` if not provided.


### Return value

A `PrefetchPostFeedData` object used to fetch post feed data.


## Example

The code below implements a custom filter function that adds a new operation to the `PrefetchPostFeedData` instance:

```python
from misago.conf.dynamicsettings import DynamicSettings
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.prefetch import PrefetchPostFeedData, fetch_posts

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


@create_prefetch_post_feed_data_hook.append_filter
def include_custom_operation(action, *args, **kwargs) -> PrefetchPostFeedData:
    prefetch = action(*args, **kwargs)

    # Run op before `fetch_posts` because it changes `data["posts"]`
    prefetch.add_before(fetch_posts_plugin_data, fetch_posts)

    return prefetch
```