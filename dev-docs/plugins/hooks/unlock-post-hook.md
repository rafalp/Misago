# `unlock_post_hook`

This hook allows plugins to replace or extend the logic used to unlock a post.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import unlock_post_hook
```


## Filter

```python
def custom_unlock_post_filter(
    action: UnlockPostHookAction,
    post: Post,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnlockPostHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

A `Post` to unlock.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the post was unlocked, `False` otherwise.


## Action

```python
def unlock_post_action(
    post: Post, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for unlocking a post.


### Arguments

#### `post: Post`

A `Post` to unlock.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the post was unlocked, `False` otherwise.


## Example

Register user who unlocked the post.

```python
from django.http import HttpRequest
from misago.posts.hooks import unlock_post_hook
from misago.posts.models import Post


@unlock_post_hook.append_filter
def register_user_that_unlocked_post(
    action,
    post: Post,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(post, commit=False, request=request):
        return False

    if request:
        post.plugin_data["unlocked_by"] = request.user.id

    if commit:
        post.save()

    return True