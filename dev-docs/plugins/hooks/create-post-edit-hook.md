# `create_post_edit_hook`

This hook wraps a standard Misago function used to create a `PostEdit` object.


## Location

This hook can be imported from `misago.edits.hooks`:

```python
from misago.edits.hooks import create_post_edit_hook
```


## Filter

```python
def custom_create_post_edit_filter(
    action: CreatePostEditHookAction,
    *,
    post: 'Post',
    user: Union['User', str],
    edit_reason: str | None,
    old_title: str | None,
    new_title: str | None,
    old_content: str | None,
    new_content: str | None,
    attachments: list['Attachment'],
    deleted_attachments: list['Attachment'],
    edited_at: datetime | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'PostEdit':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreatePostEditHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post: Post`

A `Post` instance being edited.


#### `user: Union["User", str] = None`

The user who performed the edit, a `User` instance or a `str` with the user's name.


#### `edit_reason: str | None`

A `str` with a short description of the changes, or `None`.


#### `old_content: str`

A `str` with a snapshot of `Post.original` before the edit.


#### `old_title: str | None = None`

A `str` with the previous thread title, or `None`.


#### `new_title: str | None = None`

A `str` with the new thread title, or `None`.


#### `attachments: list[Attachment]`

A `list` of new or current `Attachment` instances.


#### `deleted_attachments: list[Attachment]`

A `list` of deleted `Attachment` instances.


#### `edited_at: datetime | None = None`

A `datetime` with the timestamp of when the edit occurred.

Defaults to the current timestamp if `None`.


#### `commit: bool`

A `bool` indicating whether the new `PostEdit` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A new `PostEdit` instance.


## Action

```python
def create_post_edit_action(
    *,
    post: 'Post',
    user: Union['User', str],
    edit_reason: str | None,
    old_title: str | None,
    new_title: str | None,
    old_content: str | None,
    new_content: str | None,
    attachments: list['Attachment'],
    deleted_attachments: list['Attachment'],
    edited_at: datetime | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'PostEdit':
    ...
```

Misago function used to create a `PostEdit` object.


### Arguments

#### `post: Post`

A `Post` instance being edited.


#### `user: Union["User", str] = None`

The user who performed the edit, a `User` instance or a `str` with the user's name.


#### `edit_reason: str | None`

A `str` with a short description of the changes, or `None`.


#### `old_title: str | None = None`

A `str` with the previous thread title, or `None`.


#### `new_title: str | None = None`

A `str` with the new thread title, or `None`.


#### `old_content: str | None`

A `str` with a snapshot of `Post.original` before the edit, or `None`.


#### `new_content: str | None`

A `str` with a snapshot of new `Post.original`, or `None`.


#### `attachments: list[Attachment]`

A `list` of new or current `Attachment` instances.


#### `deleted_attachments: list[Attachment]`

A `list` of deleted `Attachment` instances.


#### `edited_at: datetime | None = None`

A `datetime` with the timestamp of when the edit occurred.

Defaults to the current timestamp if `None`.


#### `commit: bool`

A `bool` indicating whether the new `PostEdit` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A new `PostEdit` instance.


## Example

The code below implements a custom filter function that records the user's IP address on the post edit object when it's created:

```python
from django.http import HttpRequest
from misago.attachments.models import Attachment
from misago.edits.hooks import create_post_edit_hook
from misago.edits.models import PostEdit
from misago.threads.models import Post
from misago.users.models import User


@create_post_edit_hook.append_filter
def set_user_ip_on_post_edit(
    action,
    *,
    commit: bool = True,
    request: HttpRequest | None = None,
    **kwargs,
) -> PostEdit:
    post_edit = action(
        commit=False,
        request=request,
        **kwargs,
    )

    if request:
        post_edit.plugin_data["user_ip"] = request.user_ip

    if commit:
        post_edit.save()

    return post_edit
```