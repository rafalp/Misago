# `synchronize_post_likes_hook`

This hook allows plugins to replace or extend the logic used to synchronize post likes.

Post likes synchronization updates the `likes` count and the `last_likes` JSON field.


## Location

This hook can be imported from `misago.likes.hooks`:

```python
from misago.likes.hooks import synchronize_post_likes_hook
```


## Filter

```python
def custom_synchronize_post_likes_filter(
    action: SynchronizePostLikesHookAction,
    post: Post,
    queryset: QuerySet | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SynchronizePostLikesHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

The post to synchronize.


#### `queryset: QuerySet | None`

The queryset used to fetch a post's likes. Defaults to `Like.objects` if `None`.


#### `commit: bool`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Action

```python
def synchronize_post_likes_action(
    post: Post,
    queryset: QuerySet | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for synchronizing post likes.


### Arguments

#### `post: Post`

The post to synchronize.


#### `queryset: QuerySet | None`

The queryset used to fetch a post's likes. Defaults to `Like.objects` if `None`.


#### `commit: bool`

Whether the updated post instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Record the last user who synchronized the post likes:

```python
from django.db.models import Queryset
from django.http import HttpRequest
from misago.likes.hooks import synchronize_post_likes_hook
from misago.threads.models import Post


@synchronize_post_likes_hook.append_filter
def record_user_who_synced_post_likes(
    action,
    post: Post,
    queryset: QuerySet | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    action(post, queryset, False, request)

    if request:
        post.plugin_data["likes_synced_by"] = {
            "id": request.user.id,
            "username": request.user.username if request.user.id else None,
        }

    if commit:
        post.save(update_fields=["likes", "last_likes", "plugin_data"])
```