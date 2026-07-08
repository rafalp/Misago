# `get_post_merge_conflicts_hook`

This hook allows plugins to replace or extend the logic used to find merge conflicts in an iterable of posts.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_post_merge_conflicts_hook
```


## Filter

```python
def custom_get_post_merge_conflicts_filter(
    action: GetPostMergeConflictsHookAction,
    posts: Iterable[Post],
    request: HttpRequest | None=None,
) -> dict[str, list[Model]]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPostMergeConflictsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `posts: Iterable[Post]`

An iterable of `Post` instances that will be merged into a single post.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` containing lists of models for each conflict.


## Action

```python
def get_post_merge_conflicts_action(
    posts: Iterable[Post], request: HttpRequest | None=None
) -> dict[str, list[Model]]:
    ...
```

Misago function for finding merge conflicts in an iterable of posts.


### Arguments

#### `posts: Iterable[Post]`

An iterable of `Post` instances that will be merged into a single post.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` containing lists of models for each conflict. For example:

```python
conflicts = {
    "some_type": [some_instance_1, some_instance_2],
    "other_type": [other_instance_1],
}
```


## Example

Find merge conflicts for a plugin:

```python
from typing import Iterable

from django.db.models import Model
from django.http import HttpRequest
from misago.posts.hooks import get_post_merge_conflicts_hook
from misago.posts.models import Post
from myplugin.models import PluginModel


@get_post_merge_conflicts_hook.append_filter
def get_plugin_merge_conflicts(
    action,
    posts: Iterable[Post],
    request: HttpRequest | None = None,
) -> dict[str, list[Model]]:
    conflicts = action(posts, request)

    conflicts["plugin"] = list(
        PluginModel.objects.filter(post__in=posts).order_by("post")
    )

    return conflicts