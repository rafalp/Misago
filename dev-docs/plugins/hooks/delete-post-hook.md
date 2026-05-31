# `delete_post_hook`

This hook allows plugins to replace or extend the logic used to delete a post.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import delete_post_hook
```


## Filter

```python
def custom_delete_post_filter(
    action: DeletePostHookAction,
    post: Post,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeletePostHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

A `Post` to delete.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the post was hidden, `False` otherwise.


## Action

```python
def delete_post_action(post: Post, request: HttpRequest | None=None) -> None:
    ...
```

Misago function for deleting a post.


### Arguments

#### `post: Post`

A `Post` to delete.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Delete plugin objects related to this post.

```python
from django.http import HttpRequest
from misago.postgres.delete import delete_all
from misago.threads.hooks import delete_post_hook
from misago.threads.models import Post
from my_plugin.models import PostBoost


@delete_post_hook.append_filter
def delete_post_boosts(
    action,
    post: Post,
    request: HttpRequest | None = None,
) -> None:
    # Skip Django's delete collector logic
    delete_all(PostBoost, post_id=post.id)
    action(post, request)