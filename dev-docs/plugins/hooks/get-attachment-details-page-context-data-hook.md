# `get_attachment_details_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the attachment details page.


## Location

This hook can be imported from `misago.attachments.hooks`:

```python
from misago.attachments.hooks import get_attachment_details_page_context_data_hook
```


## Filter

```python
def custom_get_attachment_details_page_context_data_filter(
    action: GetAttachmentDetailsPageContextDataHookAction,
    request: HttpRequest,
    attachment: Attachment,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetAttachmentDetailsPageContextDataHookAction`

A standard Misago function used to get the template context data for the attachment details page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `attachment: Attachment`

The `Attachment` instance.


### Return value

A Python `dict` with context data to use to `render` the attachment details page.


## Action

```python
def get_attachment_details_page_context_data_action(request: HttpRequest, attachment: Attachment) -> dict:
    ...
```

A standard Misago function used to get the template context data for the attachment details page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `attachment: Attachment`

The `Attachment` instance.


### Return value

A Python `dict` with context data to use to `render` the attachment details page.


## Example

The code below implements a custom filter function that adds custom context data to the attachment details page:

```python
from django.http import HttpRequest
from misago.attachments.hooks import get_attachment_details_page_context_data_hook


@get_attachment_details_page_context_data_hook.append_filter
def include_custom_context(action, request: HttpRequest, attachment: Attachment) -> dict:
    context = action(request, attachment)

    context["plugin_data"] = "..."

    return context
```