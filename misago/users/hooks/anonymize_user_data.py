from typing import Any, Protocol

from django.contrib.auth import get_user_model

from ...plugins.hooks import FilterHook

User = get_user_model()


class AnonymizeUserDataHookAction(Protocol):
    """
    Misago function used to anonymize user data.

    # Arguments:

    ## `user: User`

    User instance that data will be anonymized.

    ## `anonymous_username: str`

    A new user name that will replace current user name.

    ## `context: dict[str, Any] | None`

    Additional context passed to the anonymize action.
    """

    def __call__(
        self,
        user: User,
        anonymous_username: str,
        *,
        context: dict[str, Any] | None = None,
    ): ...


class AnonymizeUserDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered
    in this hook.

    # Arguments:

    ## `action: AnonymizeUserDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user: User`

    User instance that data will be anonymized.

    ## `anonymous_username: str`

    A new username that will replace current username.

    ## `context: dict[str, Any] | None`

    Additional context passed to the anonymize action.
    """

    def __call__(
        self,
        action: AnonymizeUserDataHookAction,
        user: User,
        anonymous_username: str,
        *,
        context: dict[str, Any] | None = None,
    ): ...


class AnonymizeUserDataHook(
    FilterHook[
        AnonymizeUserDataHookAction,
        AnonymizeUserDataHookFilter,
    ]
):
    """
    This hook wraps the Misago function used to anonymize user data.

     # Example

    The code below implements a custom filter function that logs anonymization event.

     ```python
    import logging
    from typing import list, Protocol

    from django.contrib.auth import get_user_model
    from django.http import HttpRequest
    from misago.users.hooks import anonymize_user_data_hook

    User = get_user_model()

    logger = logging.getLogger("anonymize_user_data")


    @anonymize_user_data_hook.append_filter
    def log_anonymize_user_data(
        action,
        user: User,
        anonymous_username: str,
        *,
        context: dict[str, Any] | None = None,
    ):
        action(
            user,
            anonymous_username=anonymous_username,
            context = context
        )

        logger.info(
            "Anonymized user's data with a new username: %s", anonymous_username,
            extra = {"user": user},
        )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: AnonymizeUserDataHookAction,
        user: User,
        anonymous_username: str,
        *,
        context: dict[str, Any] | None = None,
    ):
        return super().__call__(action, user, anonymous_username, context=context)


anonymize_user_data_hook = AnonymizeUserDataHook()
