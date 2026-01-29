# `remove_post_like_hook`

This hook allows plugins to replace or extend the logic used to remove a post like from a user.

Internally, Misago uses the `synchronize_post_likes` function to update the post after deleting the `Like` instance.


## Location

This hook can be imported from `misago.likes.hooks`:

```python
from misago.likes.hooks import remove_post_like_hook
```


## Filter

```python
def custom_remove_post_like_filter(
    action: RemovePostLikeHookAction,
    post: Post,
    user: 'User',
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RemovePostLikeHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

The post to remove a like from.


#### `user: User`

The user who's post like will be removed.


#### `commit: bool`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


#### Return value

Returns `True` if like was deleted and `False` otherwise.


## Action

```python
def remove_post_like_action(
    post: Post,
    user: 'User',
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

Misago function for removing a post `Like` from a user and updating the post's `likes` and `last_likes` attributes.


### Arguments

#### `post: Post`

The post to remove a like from.


#### `user: User`

The user who's post like will be removed.


#### `commit: bool`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


#### Return value

Returns `True` if like was deleted and `False` otherwise.


## Example

Record the historical number of the post's likes:

```python
from django.http import HttpRequest
from misago.likes.hooks import remove_post_like_hook
from misago.threads.models import Post
from misago.users.models import User


@remove_post_like_hook.append_filter
def record_post_historic_likes(
    action,
    post: Post,
    user: User,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    likes = post.likes

    result = action(post, user, False, request)

    if post.plugin_data.get("total_likes"):
        post.plugin_data["total_likes"] = max(likes, post.plugin_data["total_likes"])
    else:
        post.plugin_data["total_likes"] = likes

    if commit:
        post.save(update_fields=["likes", "last_likes", "plugin_data"])

    return result
```