from typing import TYPE_CHECKING, Protocol

from django.core.exceptions import ValidationError

from ...plugins.hooks import ActionHook

if TYPE_CHECKING:
    from ..formsets import PostingFormset
    from ..state import PostingState


class ValidatePostedContentsHookAction(Protocol):
    """
    A function that Misago uses to run additional validation against user-posted
    contents.

    It should either do nothing, raise `ValidationError`, or add one or more
    `ValidationError` instances to `formset` calling it's `add_error(ValidationError)`
    method,

    # Arguments

    ## `formset: PostingFormset`

    An instance of the `PostingFormset` subclass specific to the posted contents.

    ## `state: PostingState`

    An instance of the `PostingState` subclass specific to the posted contents.
    """

    def __call__(self, formset: "PostingFormset", state: "PostingState"): ...


class ValidatePostedContentsHook(ActionHook[ValidatePostedContentsHookAction]):
    """
    This hook enables plugins to run additional validation against posted contents.

    # Example

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
    """

    __slots__ = ActionHook.__slots__

    def __call__(self, formset: "PostingFormset", state: "PostingState"):
        if self._cache is None:
            self._cache = self._actions_first + self._actions_last
        if not self._cache:
            return []

        for validator in self._cache:
            try:
                validator(formset, state)
            except ValidationError as e:
                formset.add_error(e)


validate_posted_contents_hook = ValidatePostedContentsHook()
