from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetContextDataHookAction(Protocol):
    """
    A standard function that Misago uses to check if
    a new thread should require moderator approval.

    # Arguments

    ## `state: ThreadStartState`

    A `ThreadStartState` instance containing data used to create a new thread.

    # Return value

    `dict` with context data.
    """

    def __call__(
        self,
        request: HttpRequest,
    ) -> dict: ...


class GetContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetContextDataHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `state: ThreadStartState`

    A `ThreadStartState` instance containing data used to create a new thread.

    # Return value

    `True` if the new thread should require moderator approval, or `False` otherwise.
    """

    def __call__(
        self,
        action: GetContextDataHookAction,
        request: HttpRequest,
    ) -> dict: ...


class GetContextDataHook(
    FilterHook[GetContextDataHookAction, GetContextDataHookFilter]
):
    """
    This hook allows plugin authors to inject custom data into the template
    context without creating a custom context processor.

    # Example

    The code below implements a custom filter function that flags a new thread for
    moderator approval if it contains links and the user recently joined.

    ```python
    from django.http import HttpRequest
    from misago.context_processors.hooks import get_context_data_hook


    @get_context_data_hook.append_filter
    def plugin_context_data(
        action, request: HttpRequest
    ) -> dict:
        context_data = action(request)

        # Set new keys on the context data
        context_data["extra_key"] = "Lorem ipsum!"

        # Or include a template with extra context in a predefined slot:
        context_data["before_body_close"].append(
            {
                "template_name": "my_plugin/cookie_agreement.html",
                "api_key": "d8s9a7d98sa79dsa",
            }
        )

        return context_data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetContextDataHookAction,
        request: HttpRequest,
    ) -> dict:
        return super().__call__(action, request)


get_context_data_hook = GetContextDataHook()
