from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class ContextProcessorHookAction(Protocol):
    """
    A standard function that Misago uses to create an empty context data dict
    for plugins to extend.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `dict` with context data that matches the given type:

    ```python
    from typing import TypedDict

    class TemplateComponent(TypedDict, total=False):
        template_name: str

    class ContextProcessorReturnValue(TypedDict, total=False):
        before_head_close: list[TemplateComponent]
        after_body_open: list[TemplateComponent]
        before_body_close: list[TemplateComponent]
        above_navbar: list[TemplateComponent]
        below_navbar: list[TemplateComponent]
        above_footer: list[TemplateComponent]
        below_footer: list[TemplateComponent]
    ```
    """

    def __call__(
        self,
        request: HttpRequest,
    ) -> dict: ...


class ContextProcessorHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ContextProcessorHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    # Return value

    A `dict` with context data that matches the given type:

    ```python
    from typing import TypedDict

    class TemplateComponent(TypedDict, total=False):
        template_name: str

    class ContextProcessorReturnValue(TypedDict, total=False):
        before_head_close: list[TemplateComponent]
        after_body_open: list[TemplateComponent]
        before_body_close: list[TemplateComponent]
        above_navbar: list[TemplateComponent]
        below_navbar: list[TemplateComponent]
        above_footer: list[TemplateComponent]
        below_footer: list[TemplateComponent]
    ```
    """

    def __call__(
        self,
        action: ContextProcessorHookAction,
        request: HttpRequest,
    ) -> dict: ...


class ContextProcessorHook(
    FilterHook[ContextProcessorHookAction, ContextProcessorHookFilter]
):
    """
    This hook allows plugin authors to inject custom data into the template
    context without having to create a custom context processor.

    # Example: inject extra data into a template context

    ```python
    from django.http import HttpRequest
    from misago.context_processors.hooks import context_processor_hook


    @context_processor_hook.append_filter
    def plugin_context_data(
        action, request: HttpRequest
    ) -> dict:
        context_data = action(request)

        context_data["my_plugin_data"] = request.my_plugin_data

        return context_data
    ```

    # Example: include template component in the base template

    ```python
    from django.http import HttpRequest
    from misago.context_processors.hooks import context_processor_hook


    @context_processor_hook.append_filter
    def plugin_context_data(
        action, request: HttpRequest
    ) -> dict:
        context_data = action(request)

        if not request.session.get("cookie_agreement"):
            context_data["below_footer"].append(
                {
                    "template_name": "cookie_agreement.html",
                    "agreement_message:": request.settings.cookie_agreement,
                }
            )

        return context_data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ContextProcessorHookAction,
        request: HttpRequest,
    ) -> dict:
        return super().__call__(action, request)


context_processor_hook = ContextProcessorHook()
