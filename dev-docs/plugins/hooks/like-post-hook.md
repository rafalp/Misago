# `like_post_hook`

This hook allows plugins to replace or extend the logic used to like a post.

It creates a new `Like` instance and updates the post's `likes` count and `last_likes` JSON field.


## Location

This hook can be imported from `misago.likes.hooks`:

```python
from misago.likes.hooks import like_post_hook
```


## Filter

```python
def custom_like_post_filter(
    action: LikePostHookAction,
    post: Post,
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Like:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: LikePostHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

The post to like.


#### `user: User | str`

The user who liked the post.


#### `commit: bool`

Whether the new `Like` instance and the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

New `Like` instance.


## Action

```python
def like_post_action(
    post: Post,
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Like:
    ...
```

Misago function for creating a post `Like` instance and updating the liked post's `likes` and `last_likes` attributes.


### Arguments

#### `post: Post`

The post to like.


#### `user: User | str`

The user who liked the post.


#### `commit: bool`

Whether the new `Like` instance and the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

New `Like` instance.


## Example

Record the IP address of the user who liked the post:

```python
from django.http import HttpRequest
from misago.likes.hooks import like_post_hook
from misago.likes.models import Like
from misago.threads.models import Post
from misago.users.models import User


@like_post_hook.append_filter
def record_like_ip_address(
    action,
    post: Post,
    user: User | str,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Like:
    like = action(post, user, False, request)

    if request:
        like.plugin_data["user_up"] = request.user_ip

    if commit:
        like.save()
        post.save()

    return like
```