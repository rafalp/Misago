# `remove_thread_reply_approval_hook`

This hook allows plugins to replace or extend the logic used to remove the requirement for approval of new replies in a thread.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import remove_thread_reply_approval_hook
```


## Filter

```python
def custom_remove_thread_reply_approval_filter(
    action: RemoveThreadReplyApprovalHookAction,
    thread: Thread,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RemoveThreadReplyApprovalHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` to remove reply approval from.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was updated, `False` otherwise.


## Action

```python
def remove_thread_reply_approval_action(
    thread: Thread, commit: bool=True, request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function for removing the requirement for approval of all new replies in a thread.


### Arguments

#### `thread: Thread`

A `Thread` to remove reply approval from.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

`True` if the thread was updated, `False` otherwise.


## Example

Register user who approved the thread.

```python
from django.http import HttpRequest
from misago.threads.hooks import remove_thread_reply_approval_hook
from misago.threads.models import Thread


@remove_thread_reply_approval_hook.append_filter
def register_user_that_removed_require_thread_reply_approval(
    action,
    thread: Thread,
    commit: bool = True,
    request: HttpRequest | None = None,
) -> bool:
    if not action(thread, commit=False, request=request):
        return False

    if request:
        thread.plugin_data["removed_require_reply_approval"] = request.user.id

    if commit:
        thread.save()

    return True