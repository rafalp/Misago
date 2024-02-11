from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...users.models import Group


class CopyGroupPermissionsHookAction(Protocol):
    """
    A standard Misago function used to copy permissions from one user group to another
    or the next filter function from another plugin.

    # Arguments

    ## `src: Group`

    A group to copy permissions from.

    ## `dst: Group`

    A group to copy permissions to.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        src: Group,
        dst: Group,
        request: HttpRequest | None = None,
    ) -> None: ...


class CopyGroupPermissionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CopyGroupPermissionsHookAction`

    A standard Misago function used to copy permissions from one user group to another
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `src: Group`

    A group to copy permissions from.

    ## `dst: Group`

    A group to copy permissions to.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        action: CopyGroupPermissionsHookAction,
        src: Group,
        dst: Group,
        request: HttpRequest | None = None,
    ) -> None: ...


class CopyGroupPermissionsHook(
    FilterHook[CopyGroupPermissionsHookAction, CopyGroupPermissionsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to copy group permissions.

    # Example

    The code below implements a custom filter function that copies a permission from
    one group's `plugin_data` to the other:

    ```python
    from django.http import HttpRequest
    from misago.permissions.hooks import copy_group_permissions_hook
    from misago.users.models import Group


    @copy_group_permissions_hook.append_filter
    def copy_group_plugin_perms(
        action, src: Group, dst: Group, request: HttpRequest | None = None,
    ) -> None:
        dst.plugin_data["can_do_plugin_thing"] = src.plugin_data["can_do_plugin_thing"]

        # Call the next function in chain
        return action(group, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CopyGroupPermissionsHookAction,
        src: Group,
        dst: Group,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, src, dst, request)


copy_group_permissions_hook = CopyGroupPermissionsHook()
