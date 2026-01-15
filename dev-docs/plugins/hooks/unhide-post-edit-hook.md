# `unhide_post_edit_hook`

This hook wraps a standard Misago function used to unhide a `PostEdit` object.


## Location

This hook can be imported from `misago.edits.hooks`:

```python
from misago.edits.hooks import unhide_post_edit_hook
```


## Filter

```python
def custom_unhide_post_edit_filter(
    action: UnhidePostEditHookAction,
    post_edit: 'PostEdit',
    commit: bool=True,
    request: HttpRequest | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnhidePostEditHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post_edit: PostEdit`

A `PostEdit` instance to unhide.


#### `commit: bool = True`

A `bool` indicating whether the updated `PostEdit` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Action

```python
def unhide_post_edit_action(
    post_edit: 'PostEdit',
    commit: bool=True,
    request: HttpRequest | None=None,
):
    ...
```

Misago function used to unhide a `PostEdit` object.


### Arguments

#### `post_edit: PostEdit`

A `PostEdit` instance to unhide.


#### `commit: bool = True`

A `bool` indicating whether the updated `PostEdit` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Example

The code below implements a custom filter function that records the details of the user who unhid the edit:

```python
from django.http import HttpRequest
from misago.edits.hooks import unhide_post_edit_hook
from misago.edits.models import PostEdit


@unhide_post_edit_hook.append_filter
def unhide_post_edit_record_user(
    action,
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    action(post_edit, False, request)

    if request:
        post_edit.plugin_data.update({
            "unhidden_by_user_id": request.user.id,
            "unhidden_by_user_name": request.user.username,
            "inhidden_by_ip": request.user_ip,
        })

    if commit:
        post_edit.save()
```