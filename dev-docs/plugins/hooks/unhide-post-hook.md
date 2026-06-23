# `unhide_post_hook`

This hook allows plugins to replace or extend the logic used to unhide a post.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import unhide_post_hook
```


## Filter

```python
def custom_unhide_post_filter(
    action: UnhidePostHookAction,
    post: Post,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnhidePostHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

A `Post` to unhide.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the post was unhidden, `False` otherwise.


## Action

```python
def unhide_post_action(
    post: Post, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for unhiding a post.


### Arguments

#### `post: Post`

A `Post` to unhide.


#### `commit: bool = True`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the post was unhidden, `False` otherwise.


## Example

Register user who unhidden the post:

```python
from django.http import HttpRequest
from misago.posts.hooks import unhide_post_hook
from misago.posts.models import Post


@unhide_post_hook.append_filter
def register_user_that_unhidden_post(
    action,
    post: Post,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(post, commit=False, request=request):
        return False

    if request:
        post.plugin_data["unhidden_by"] = request.user.id

    if commit:
        post.save()

    return True