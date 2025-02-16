from typing import Protocol

from PIL.Image import Image
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetAttachmentPluginDataHookAction(Protocol):
    """
    A standard function that Misago uses to create a `dict` to be saved in new
    attachment's `plugin_data` JSON field.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `upload: UploadedFile`

    The `UploadedFile` instance.

    ## `image: Image | None`

    The `PIL.Image.Image` instance if uploaded file was an image, or `None`.

    # Return value

    A JSON-serializable `dict`.
    """

    def __call__(
        self,
        request: HttpRequest,
        upload: UploadedFile,
        image: Image | None = None,
    ) -> dict: ...


class GetAttachmentPluginDataHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetAttachmentPluginDataHookAction`

    A standard function that Misago uses to create a `dict` to be saved in new
    attachment's `plugin_data` JSON field.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `upload: UploadedFile`

    The `UploadedFile` instance.

    ## `image: Image | None`

    The `PIL.Image.Image` instance if uploaded file was an image, or `None`.

    # Return value

    A JSON-serializable `dict`.
    """

    def __call__(
        self,
        action: GetAttachmentPluginDataHookAction,
        request: HttpRequest,
        upload: UploadedFile,
        image: Image | None = None,
    ) -> dict: ...


class GetAttachmentPluginDataHook(
    FilterHook[
        GetAttachmentPluginDataHookAction,
        GetAttachmentPluginDataHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a `dict`
    to be saved in new attachment's `plugin_data` JSON field.

    # Example

    The code below implements a custom filter function that stores an image's
    EXIF data in the `Attachment.plugin_data` if the uploaded file is an image:

    ```python
    from PIL.Image import Image
    from django.core.files.uploadedfile import UploadedFile
    from django.http import HttpRequest
    from misago.attachments.hooks import get_attachment_plugin_data_hook


    @get_attachment_plugin_data_hook.append_filter
    def store_attachment_exif_data(
        action,
        request: HttpRequest,
        upload: UploadedFile,
        image: Image | None = None,
    ) -> dict:
        plugin_data = action(request, upload, image)

        if image:
            exif = image.getexif()
            plugin_data["exif"] = {
                "make": exif.get(271, None),
                "model": exif.get(272, None)
            }

        return plugin_data
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetAttachmentPluginDataHookAction,
        request: HttpRequest,
        upload: UploadedFile,
        image: Image | None = None,
    ) -> dict:
        return super().__call__(action, request, upload, image)


get_attachment_plugin_data_hook = GetAttachmentPluginDataHook()
