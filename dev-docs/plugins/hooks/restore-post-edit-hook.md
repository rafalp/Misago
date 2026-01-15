# `restore_post_edit_hook`

This hook wraps a standard Misago function used to restore post content from a related PostEdit object.


## Location

This hook can be imported from `misago.edits.hooks`:

```python
from misago.edits.hooks import restore_post_edit_hook
```


## Filter

```python
def custom_restore_post_edit_filter(
    action: RestorePostEditHookAction,
    post_edit: 'PostEdit',
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> tuple['Post', 'PostEdit']:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RestorePostEditHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post_edit: PostEdit`

A `PostEdit` instance to restore the post from.


#### `user: Union["User", str] = None`

The user who restored the post, a `User` instance or a `str` with the user’s name.


#### `commit: bool = True`

A `bool` indicating whether the updated `Post` and the new `PostEdit` instances should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A `tuple` with the updated `Post` instance and the new `PostEdit` instance.


## Action

```python
def restore_post_edit_action(
    post_edit: 'PostEdit',
    user: Union['User', str],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> tuple['Post', 'PostEdit']:
    ...
```

Misago function used to restore post content from a related `PostEdit` object.


### Arguments

#### `post_edit: PostEdit`

A `PostEdit` instance to restore the post from.


#### `user: Union["User", str] = None`

The user who restored the post, a `User` instance or a `str` with the user’s name.


#### `commit: bool = True`

A `bool` indicating whether the updated `Post` and the new `PostEdit` instances should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A `tuple` with the updated `Post` instance and the new `PostEdit` instance.


## Example

The code below implements a custom filter function that sets restored post's edit reason:

```python
from django.http import HttpRequest
from misago.edits.hooks import restore_post_edit_hook
from misago.edits.models import PostEdit
from misago.posting.tasks import upgrade_post_content
from misago.posting.upgradepost import post_needs_content_upgrade
from misago.threads.models import Post
from misago.users.models import User


@restore_post_edit_hook.append_filter
def restore_post_edit_record_user_ip(
    action,
    post_edit: PostEdit,
    user: User | str,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> tuple[Post, PostEdit]:
    post, new_post_edit = action(post_edit, user, False, request)

    post.last_edit_reason = f"Restored from #{new_post_edit.id}"

    if commit:
        post.save()

        post.set_search_vector()
        post.save(update_fields=["search_vector"])

        new_post_edit.save()

        if post_needs_content_upgrade(post):
            upgrade_post_content.delay(post.id, post.sha256_checksum)

    return post, new_post_edit
```