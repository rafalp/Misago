# `validate_thread_title_hook`

This hook wraps a standard function used by Misago to validate thread titles. Raises `ValidationError` if the thread title is invalid.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import validate_thread_title_hook
```


## Filter

```python
def custom_validate_thread_title_filter(
    action: ValidateThreadTitleHookAction,
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidateThreadTitleHookAction`

A standard function used by Misago to validate thread titles. Raises `ValidationError` if the thread title is invalid.

See the [action](#action) section for details.


#### `value: str`

The value to validate.


#### `min_length: int`

The minimum required length of the thread title.


#### `max_length: int`

The maximum allowed length of the thread title.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Action

```python
def validate_thread_title_action(
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A standard function used by Misago to validate thread titles. Raises `ValidationError` if the thread title is invalid.


### Arguments

#### `value: str`

The value to validate.


#### `min_length: int`

The minimum required length of the thread title.


#### `max_length: int`

The maximum allowed length of the thread title.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Example

The code below implements a custom thread title validator that raises the minimal required length of a thread's title for new users.

```python
from django.http import HttpRequest
from misago.posting.hooks import validate_thread_title_hook


@validate_thread_title_hook.append_filter
def validate_thread_title_for_new_users(
    action,
    value: str,
    min_length: int,
    max_length: int,
    *,
    request: HttpRequest | None = None,
) -> None:
    if request and request.user.is_authenticated and request.user.posts < 5:
        min_length = min(min_length + 10)

    action(value, min_length, max_length, request=request)
```