from typing import Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook


class CopyCategoryPermissionsHookAction(Protocol):
    """
    A standard Misago function used to copy permissions from one category to another
    or the next filter function from another plugin.

    # Arguments

    ## `src: Category`

    A category to copy permissions from.

    ## `dst: Category`

    A category to copy permissions to.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        src: Category,
        dst: Category,
        request: HttpRequest | None = None,
    ) -> None: ...


class CopyCategoryPermissionsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CopyCategoryPermissionsHookAction`

    A standard Misago function used to copy permissions from one category to another
    or the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `src: Category`

    A category to copy permissions from.

    ## `dst: Category`

    A category to copy permissions to.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        action: CopyCategoryPermissionsHookAction,
        src: Category,
        dst: Category,
        request: HttpRequest | None = None,
    ) -> None: ...


class CopyCategoryPermissionsHook(
    FilterHook[CopyCategoryPermissionsHookAction, CopyCategoryPermissionsHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to copy category permissions.

    # Example

    The code below implements a custom filter function that copies additional models with
    the plugin's category permissions:

    ```python
    from django.http import HttpRequest
    from misago.permissions.hooks import copy_category_permissions_hook
    from misago.users.models import Category

    from .models PluginCategoryPermissions


    @copy_category_permissions_hook.append_filter
    def copy_group_plugin_perms(
        action, src: Category, dst: Category, request: HttpRequest | None = None,
    ) -> None:
        # Delete old permissions
        PluginCategoryPermissions.objects.filter(category=dst).delete()

        # Copy permissions
        for permission in PluginCategoryPermissions.objects.filter(category=src):
            PluginCategoryPermissions.objects.create(
                category=dst,
                group_id=permission.group_id,
                can_do_something=permission.can_do_something,
            )

        # Call the next function in chain
        return action(group, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CopyCategoryPermissionsHookAction,
        src: Category,
        dst: Category,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, src, dst, request)


copy_category_permissions_hook = CopyCategoryPermissionsHook()
