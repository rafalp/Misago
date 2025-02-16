# `serialize_attachment_hook`

This hook wraps the standard function that Misago uses to create a JSON-serializable `dict` for an attachment.


## Location

This hook can be imported from `misago.attachments.hooks`:

```python
from misago.attachments.hooks import serialize_attachment_hook
```


## Filter

```python
def custom_serialize_attachment_filter(
    action: SerializeAttachmentHookAction, attachment: Attachment
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SerializeAttachmentHookAction`

A standard function that Misago uses to create a JSON-serializable `dict` for an attachment.

See the [action](#action) section for details.


#### `attachment: Attachment`

The `Attachment` instance to serialize.


### Return value

A JSON-serializable `dict`.


## Action

```python
def serialize_attachment_action(attachment: Attachment) -> dict:
    ...
```

A standard function that Misago uses to create a JSON-serializable `dict` for an attachment.


### Arguments

#### `attachment: Attachment`

The `Attachment` instance to serialize.


### Return value

A JSON-serializable `dict`.


## Example

The code below implements a custom filter function that includes image's EXIF data in serialized payload

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