# `merge_posts_hook`

This hook allows plugins to replace or extend the logic used to merge posts.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import merge_posts_hook
```


## Filter

```python
def custom_merge_posts_filter(
    action: MergePostsHookAction,
    target: Post,
    posts: Iterable[Post],
    conflicts: dict[str, Model],
    merged_by: Union['User', str],
    edit_reason: str | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Post:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: MergePostsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `target: Post`

The `Post` to merge `posts` into.


#### `posts: Iterable[Post]`

An iterable of `Post` instances to merge into `target`.

These posts are deleted during the merge.


#### `conflicts: dict[str, Model]`

A `dict` with the conflict resolutions to use during the merge.


#### `merged_by: Union["User", str] = None`

The user who performed the merge, a `User` instance or a `str` with the user's name.


#### `edit_reason: str | None = None`

A `str` with a reason for merging posts, or `None`.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

The `Post` instance.


## Action

```python
def merge_posts_action(
    target: Post,
    posts: Iterable[Post],
    conflicts: dict[str, Model],
    merged_by: Union['User', str],
    edit_reason: str | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Post:
    ...
```

Misago function for merging posts.


### Arguments

#### `target: Post`

The `Post` to merge `posts` into.


#### `posts: Iterable[Post]`

An iterable of `Post` instances to merge into `target`.

These posts are deleted during the merge.


#### `conflicts: dict[str, Model]`

A `dict` with the conflict resolutions to use during the merge.


#### `merged_by: Union["User", str] = None`

The user who performed the merge, a `User` instance or a `str` with the user's name.


#### `edit_reason: str | None = None`

A `str` with a reason for merging posts, or `None`.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

The `Post` instance.


## Example

Update `PluginModel` objects during the merge

```python
from typing import Iterable

from django.db.models import Model
from django.http import HttpRequest
from misago.posts.hooks import merge_posts_hook
from misago.posts.models import Post
from misago.users.models import User
from myplugin.models import PluginModel


@merge_posts_hook.append_filter
def get_plugin_merge_conflicts(
    action,
    target: Post,
    posts: Iterable[Post],
    conflicts: dict[str, Model],
    merged_by: Union["User", str],
    edit_reason: str | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Post:
    PluginModel.objects.filter(post__in=posts).update(
        category=target.category, post=target
    )

    return action(
        target,
        posts,
        conflicts,
        merged_by,
        edit_reason,
        commit,
        request,
    )