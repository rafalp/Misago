# `get_thread_merge_form_fields_hook`

This hook allows plugins to replace or extend the logic used to create form fields for resolving conflicts in thread merges.

Fields must be instances of `TypedChoiceField` or `ChoiceField` and are always rendered using the `select` widget.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_merge_form_fields_hook
```


## Filter

```python
def custom_get_thread_merge_form_fields_filter(
    action: GetThreadMergeConflictsHookAction,
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None=None,
) -> dict[str, Field]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadMergeConflictsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `conflicts: dict[str, list[Model]]`

A `dict` with the existing conflicts.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` of fields to merge with the form's existing `fields`.


## Action

```python
def get_thread_merge_form_fields_action(
    conflicts: dict[str, list[Model]], request: HttpRequest | None=None
) -> dict[str, Field]:
    ...
```

Misago function for creating form fields for resolving conflicts in thread merges.


### Arguments

#### `conflicts: dict[str, list[Model]]`

A `dict` with the existing conflicts.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` of fields to merge with the form's existing `fields`.


## Example

Include a field for resolving plugin's merge conflicts:

```python
from typing import Iterable

from django.db.models import Model
from django.forms import
from django.http import HttpRequest
from django.utils.translation import pgettext
from misago.threads.hooks import get_thread_merge_form_fields_hook
from myplugin.models import PluginModel


@get_thread_merge_form_fields_hook.append_filter
def get_plugin_thread_merge_form_fields(
    action,
    conflicts: dict[str, list[Model]],
    request: HttpRequest | None = None,
) -> dict[str, Field]:
    fields = action(conflicts, request)

    if "plugin" in conflicts:
        fields["plugin"] = forms.TypedChoiceField(
            label=pgettext("thread merge poll conflict", "Plugin"),
            help_text=pgettext(
                "thread merge poll conflict",
                "Select plugin object to keep in the merged thread. Other objects will be deleted.",
            ),
            coerce=int,
            choices=[
                (obj.id, f"{obj.name} ({obj.thread.title})")
                for obj in conflicts["plugin"]
            ],
        )

    return fields