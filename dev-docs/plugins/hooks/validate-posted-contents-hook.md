# `validate_posted_contents_hook`

This hook enables plugins to run additional validation against posted contents.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import validate_posted_contents_hook
```


## Action

```python
def custom_validate_posted_contents_filter(formset: 'PostingFormset', state: 'PostingState'):
    ...
```

A function that Misago uses to run additional validation against user-posted contents.

It should either do nothing, raise `ValidationError`, or add one or more `ValidationError` instances to `formset` calling it's `add_error(ValidationError)` method,


### Arguments

#### `formset: PostingFormset`

An instance of the `PostingFormset` subclass specific to the posted contents.


#### `state: PostingState`

An instance of the `PostingState` subclass specific to the posted contents.


## Example

The code below implements a custom validator that ch

```python
from django.core.exceptions import ValidationError
from misago.posting.forms.title import PREFIX as THREAD_TITLE_FORM
from misago.posting.hooks import validate_posted_contents_hook


@validate_posted_contents_hook.append_action
def validate_posted_contents_are_not_spam(formset, state):
    # Exclude moderators from the check
    if state.request.user_permissions.is_category_moderator(state.category.id):
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

    if "spam" in state.post.original.lower():
        return True

    return False
```