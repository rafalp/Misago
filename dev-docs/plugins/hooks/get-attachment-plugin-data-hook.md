# `get_attachment_plugin_data_hook`

This hook wraps the standard function that Misago uses to create a `dict` to be saved in new attachment's `plugin_data` JSON field.


## Location

This hook can be imported from `misago.attachments.hooks`:

```python
from misago.attachments.hooks import get_attachment_plugin_data_hook
```


## Filter

```python
def custom_get_attachment_plugin_data_filter(
    action: GetAttachmentPluginDataHookAction,
    request: HttpRequest,
    upload: UploadedFile,
    image: Image | None=None,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetAttachmentPluginDataHookAction`

A standard function that Misago uses to create a `dict` to be saved in new attachment's `plugin_data` JSON field.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `upload: UploadedFile`

The `UploadedFile` instance.


#### `image: Image | None`

The `PIL.Image.Image` instance if uploaded file was an image, or `None`.


### Return value

A JSON-serializable `dict`.


## Action

```python
def get_attachment_plugin_data_action(
    request: HttpRequest, upload: UploadedFile, image: Image | None=None
) -> dict:
    ...
```

A standard function that Misago uses to create a `dict` to be saved in new attachment's `plugin_data` JSON field.


### Arguments

#### `request: HttpRequest`

The request object.


#### `upload: UploadedFile`

The `UploadedFile` instance.


#### `image: Image | None`

The `PIL.Image.Image` instance if uploaded file was an image, or `None`.


### Return value

A JSON-serializable `dict`.


## Example

The code below implements a custom filter function that stores an image's EXIF data in the `Attachment.plugin_data` if the uploaded file is an image:

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