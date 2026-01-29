# `validate_thread_title_hook`

This hook allows plugins to replace or extend the standard logic used to validate thread titles.


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
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidateThreadTitleHookAction`

The next function registered in this hook, either a custom function or Misago's default.

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
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for validating a thread title. Raises `ValidationError` if the thread title is invalid.


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

Forbid selected words in thread titles:

```python
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext
from misago.posting.hooks import validate_thread_title_hook

BAD_WORDS = ("casino", "win", "spam")

@validate_thread_title_hook.append_filter
def validate_thread_title_bad_words(
    action,
    value: str,
    min_length: int,
    max_length: int,
    request: HttpRequest | None = None,
) -> None:
    if value:
        value_lowercase = value.lower()
        for bad_word in BAD_WORDS:
            if bad_word in value_lowercase:
                raise ValidationError(
                    message=pgettext(
                        "thread validator",
                        "This title is not allowed.",
                    ),
                    code="invalid",
                )

    action(value, min_length, max_length, request)
```