# `validate_poll_choices_hook`

This hook allows plugins to replace or extend the standard logic used to validate poll choices.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import validate_poll_choices_hook
```


## Filter

```python
def custom_validate_poll_choices_filter(
    action: ValidatePollChoicesHookAction,
    choices: PollChoices,
    max_choices: int,
    choice_min_length: int,
    choice_max_length: int,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ValidatePollChoicesHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `choices: PollChoices`

The `PollChoices` instance to validate


#### `max_choices: int`

The maximum number of allowed choices.


#### `choice_min_length: int`

The minimum allowed length for each poll choice.


#### `choice_max_length: int`

The maximum allowed length for each poll choice.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Action

```python
def validate_poll_choices_action(
    choices: PollChoices,
    max_choices: int,
    choice_min_length: int,
    choice_max_length: int,
    request: HttpRequest | None=None,
) -> None:
    ...
```

Misago function for validating poll choices. Raises `ValidationError` if one or more poll choices are invalid.


### Arguments

#### `choices: PollChoices`

The `PollChoices` instance to validate


#### `max_choices: int`

The maximum number of allowed choices.


#### `choice_min_length: int`

The minimum allowed length for each poll choice.


#### `choice_max_length: int`

The maximum allowed length for each poll choice.


#### `request: HttpRequest | None`

The request object or `None` if not provided.


## Example

Forbid selected words in poll choices:

```python
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import pgettext
from misago.polls.choices import PollChoices
from misago.posting.hooks import validate_poll_choices_hook

BAD_WORDS = ("casino", "win", "spam")

@validate_poll_choices_hook.append_filter
def validate_poll_choices_bad_words(
    action,
    choices: PollChoices,
    max_choices: int,
    choice_min_length: int,
    choice_max_length: int,
    request: HttpRequest | None = None,
) -> None:
    for choice, name in enumerate(choices.get_names(), start=1):
        name_lowercase = name.lower()
        for bad_word in BAD_WORDS:
            if bad_word in name_lowercase:
                raise ValidationError(
                    message=pgettext(
                        "poll choices validator",
                        "Choice #%(choice)s is not allowed.",
                    ),
                    code="invalid",
                    params={"choice": choice},
                )

    action(
        choices,
        max_choices,
        choice_min_length,
        choice_max_length,
        request,
    )
```