from typing import Protocol

from django.db.models import Model
from django.forms import Field
from django.http import HttpRequest

from ...plugins.hooks import FilterHook


class GetThreadMergeConflictsHookAction(Protocol):
    """
    Misago function for creating form fields for resolving conflicts in thread merges.

    # Arguments

    ## `conflicts: dict[str, list[Model]]`

    A `dict` with the existing conflicts.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `dict` of fields to merge with the form's existing `fields`.
    """

    def __call__(
        self,
        conflicts: dict[str, list[Model]],
        request: HttpRequest | None = None,
    ) -> dict[str, Field]: ...


class GetThreadMergeConflictsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadMergeConflictsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `conflicts: dict[str, list[Model]]`

    A `dict` with the existing conflicts.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `dict` of fields to merge with the form's existing `fields`.

    """

    def __call__(
        self,
        action: GetThreadMergeConflictsHookAction,
        conflicts: dict[str, list[Model]],
        request: HttpRequest | None = None,
    ) -> dict[str, Field]: ...


class GetThreadMergeConflictsHook(
    FilterHook[
        GetThreadMergeConflictsHookAction,
        GetThreadMergeConflictsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    create form fields for resolving conflicts in thread merges.

    Fields must be instances of `TypedChoiceField` or `ChoiceField` and are always
    rendered using the `select` widget.

    # Example

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
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadMergeConflictsHookAction,
        conflicts: dict[str, list[Model]],
        request: HttpRequest | None = None,
    ) -> dict[str, Field]:
        return super().__call__(action, conflicts, request)


get_thread_merge_form_fields_hook = GetThreadMergeConflictsHook()
