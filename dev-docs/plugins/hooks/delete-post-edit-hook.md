# `delete_post_edit_hook`

This hook wraps a standard Misago function used to delete a `PostEdit` object.


## Location

This hook can be imported from `misago.edits.hooks`:

```python
from misago.edits.hooks import delete_post_edit_hook
```


## Filter

```python
def custom_delete_post_edit_filter(
    action: DeletePostEditHookAction,
    post_edit: 'PostEdit',
    commit: bool=True,
    request: HttpRequest | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeletePostEditHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `post_edit: PostEdit`

A `PostEdit` instance to delete.


#### `commit: bool = True`

A `bool` indicating whether the `PostEdit` instance should be deleted from the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Action

```python
def delete_post_edit_action(
    post_edit: 'PostEdit',
    commit: bool=True,
    request: HttpRequest | None=None,
):
    ...
```

Misago function used to delete a `PostEdit` object.


### Arguments

#### `post_edit: PostEdit`

A `PostEdit` instance to delete.


#### `commit: bool = True`

A `bool` indicating whether the `PostEdit` instance should be deleted from the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Example

The code below implements a custom filter function that records a number of deleted post edits:

```python
from django.http import HttpRequest
from misago.edits.hooks import delete_post_edit_hook
from misago.edits.models import PostEdit


@delete_post_edit_hook.append_filter
def count_post_edit_deletions(
    action,
    post_edit: PostEdit,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    post = post_edit.post
    action(post_edit, commit, request)

    post.plugin_data.setdefault("deleted_edits", 0) += 1
    post.save(update_fields=["plugin_data"])
```