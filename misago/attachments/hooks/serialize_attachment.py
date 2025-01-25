from typing import Protocol

from ...plugins.hooks import FilterHook
from ..models import Attachment


class SerializeAttachmentHookAction(Protocol):
    """
    A standard function that Misago uses to create a JSON-serializable `dict`
    for an attachment.

    # Arguments

    ## `attachment: Attachment`

    The `Attachment` instance to serialize.

    # Return value

    A JSON-serializable `dict`.
    """

    def __call__(self, attachment: Attachment) -> dict: ...


class SerializeAttachmentHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SerializeAttachmentHookAction`

    A standard function that Misago uses to create a JSON-serializable `dict`
    for an attachment.

    See the [action](#action) section for details.

    ## `attachment: Attachment`

    The `Attachment` instance to serialize.

    # Return value

    A JSON-serializable `dict`.
    """

    def __call__(
        self,
        action: SerializeAttachmentHookAction,
        attachment: Attachment,
    ) -> dict: ...


class SerializeAttachmentHook(
    FilterHook[
        SerializeAttachmentHookAction,
        SerializeAttachmentHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a
    JSON-serializable `dict` for an attachment.

    # Example

    The code below implements a custom filter function that includes image's
    EXIF data in serialized payload

    ```python
    from misago.attachments.hooks import serialize_attachment_hook
    from misago.attachments.models import Attachment


    @serialize_attachment_hook.append_filter
    def serialize_attachment_exif_data(
        action, attachment: Attachment
    ) -> dict:
        data = action(attachment)
        data["exif"] = attachment.plugin_data.get("exif)
        return data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SerializeAttachmentHookAction,
        attachment: Attachment,
    ) -> dict:
        return super().__call__(action, attachment)


serialize_attachment_hook = SerializeAttachmentHook()
