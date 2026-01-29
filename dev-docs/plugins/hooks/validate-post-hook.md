# `validate_post_hook`

This hook allows plugins to replace or extend the standard logic used to validate post contents.

Post contents are represented as a `ParsingResult` object with the following attributes:

- `markup: str`: The original markup posted by the user. - `tokens: list[Token]`: A token stream returned by the parser. - `html: str`: An HTML representation of the parsed markup. - `text: str`: A plain text representation of the parsed markup.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import validate_post_hook
```


## Filter

```python
def custom_validate_post_filter(
    action: ValidatePostHookAction,
    value: ParsingResult,
    min_length: int,
    max_length: int,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidatePostHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `value: ParsingResult`

The value to validate.


#### `min_length: int`

The minimum required length of posted message.


#### `max_length: int`

The maximum allowed length of posted message. `0` disables this check.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Action

```python
def validate_post_action(
    value: ParsingResult,
    min_length: int,
    max_length: int,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for validating the contents of a post. Raises `ValidationError` if the post contents are invalid.


### Arguments

#### `value: ParsingResult`

The value to validate.


#### `min_length: int`

The minimum required length of posted message.


#### `max_length: int`

The maximum allowed length of posted message. `0` disables this check.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Example

Raises the minimal required length of a post for new users.

```python
from django.http import HttpRequest
from misago.parser.parse import ParsingResult
from misago.posting.hooks import validate_post_hook


@validate_post_hook.append_filter
def validate_post_for_new_users(
    action,
    value: ParsingResult,
    min_length: int,
    max_length: int,
    request: HttpRequest | None = None,
) -> None:
    if request and request.user.is_authenticated and request.user.posts < 5:
        min_length = min(min_length + 50)

    action(value, min_length, max_length, request)
```