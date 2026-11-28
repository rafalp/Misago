from typing import TYPE_CHECKING, Protocol, Union

from django.core.exceptions import ValidationError

from ...plugins.hooks import ActionHook

if TYPE_CHECKING:
    from ..formsets import Formset, TabbedFormset
    from ..state import State


class ValidatePostingHookAction(Protocol):
    """
    A function that Misago uses to perform additional validation of a posting.

    It should either do nothing, raise a `ValidationError`, or add one or more
    `ValidationError` instances to formset by calling its `add_error()` method.

    # Arguments

    ## `formset: Formset`

    An instance of the `Formset` subclass specific to the posting.

    ## `state: State`

    An instance of the `State` subclass specific to the posting.
    """

    def __call__(self, formset: Union["Formset", "TabbedFormset"], state: "State"): ...


class ValidatePostingHook(ActionHook[ValidatePostingHookAction]):
    """
    This hook enables plugins to perform additional validation
    of the posting formset and state.

    # Example

    The code below implements custom anti-spam validation
    that checks both the thread title and post content.

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
    """

    __slots__ = ActionHook.__slots__

    def __call__(self, formset: Union["Formset", "TabbedFormset"], state: "State"):
        if self._cache is None:
            self._cache = self._actions_first + self._actions_last
        if not self._cache:
            return []

        for validator in self._cache:
            try:
                validator(formset, state)
            except ValidationError as e:
                formset.add_error(e)


validate_posting_hook = ValidatePostingHook()
