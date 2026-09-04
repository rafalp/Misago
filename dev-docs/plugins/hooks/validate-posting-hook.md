# `validate_posting_hook`

This hook enables plugins to perform additional validation of the posting formset and state.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import validate_posting_hook
```


## Action

```python
def custom_validate_posting_filter(
    formset: Union['Formset', 'TabbedFormset'], state: 'State'
):
    ...
```

A function that Misago uses to perform additional validation of a posting.

It should either do nothing, raise a `ValidationError`, or add one or more `ValidationError` instances to formset by calling its `add_error()` method.


### Arguments

#### `formset: Formset`

An instance of the `Formset` subclass specific to the posting.


#### `state: State`

An instance of the `State` subclass specific to the posting.


## Example

The code below implements custom anti-spam validation that checks both the thread title and post content.

```python
from django.core.exceptions import ValidationError
from misago.posting.forms.title import PREFIX as THREAD_TITLE_FORM
from misago.posting.hooks import validate_posting_hook


@validate_posting_hook.append_action
def validate_posting_are_not_spam(formset, state):
    # Exclude moderators from the check
    if state.request.user_permissions.is_category_moderator(state.category):
        return

    if is_spam(formset, state):
        raise ValidationError("Your message contains spam!")


def is_spam(formset, state) -> bool:
    # Check if posting form included thread title
    if (
        THREAD_TITLE_FORM in formset
        and "spam" in state.thread.title.lower()
    ):
        return True

    if "spam" in state.post.content.lower():
        return True

    return False
```