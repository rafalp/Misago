from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Attachment


class GetAttachmentDetailsPageContextDataHookAction(Protocol):
    """
    A standard Misago function used to get the template context data
    for the attachment details page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `attachment: Attachment`

    The `Attachment` instance.

    # Return value

    A Python `dict` with context data to use to `render` the attachment details page.
    """

    def __call__(self, request: HttpRequest, attachment: Attachment) -> dict: ...


class GetAttachmentDetailsPageContextDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetAttachmentDetailsPageContextDataHookAction`

    A standard Misago function used to get the template context data
    for the attachment details page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `attachment: Attachment`

    The `Attachment` instance.

    # Return value

    A Python `dict` with context data to use to `render` the attachment details page.
    """

    def __call__(
        self,
        action: GetAttachmentDetailsPageContextDataHookAction,
        request: HttpRequest,
        attachment: Attachment,
    ) -> dict: ...


class GetAttachmentDetailsPageContextDataHook(
    FilterHook[
        GetAttachmentDetailsPageContextDataHookAction,
        GetAttachmentDetailsPageContextDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to get
    the template context data for the attachment details page.

    # Example

    The code below implements a custom filter function that adds custom context
    data to the attachment details page:

    ```python
    from django.http import HttpRequest
    from misago.attachments.hooks import get_attachment_details_page_context_data_hook


    @get_attachment_details_page_context_data_hook.append_filter
    def include_custom_context(action, request: HttpRequest, attachment: Attachment) -> dict:
        context = action(request, attachment)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetAttachmentDetailsPageContextDataHookAction,
        request: HttpRequest,
        attachment: Attachment,
    ) -> dict:
        return super().__call__(action, request, attachment)


get_attachment_details_page_context_data_hook = GetAttachmentDetailsPageContextDataHook(
    cache=False
)
