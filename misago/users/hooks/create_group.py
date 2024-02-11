from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Group


class CreateGroupHookAction(Protocol):
    """
    A standard Misago function used for creating a new user group or the next filter
    function from another plugin.

    # Arguments

    Accepts the same arguments as `Group.objects.create()`.

    It is guaranteed to be called with at least the `name: str` argument.

    # Additional arguments

    In addition to the standard `kwargs` accepted by `Group.objects.create()`, optional
    arguments may be present:

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.

    ## `form: Optional[Form]`

    Bound `Form` instance that was used to create this group.

    ## `plugin_data: dict`

    A plugin data `dict` that will be saved on the `Group.plugin_data` attribute.

    # Return value

    A newly created `Group` instance.
    """

    def __call__(self, **kwargs) -> Group: ...


class CreateGroupHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CreateGroupHookAction`

    A standard Misago function used for creating a new user group or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    # Additional arguments

    In addition to the standard `kwargs` accepted by `Group.objects.create()`, optional
    arguments may be present:

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.

    ## `form: Optional[Form]`

    Bound `Form` instance that was used to create this group.

    ## `plugin_data: dict`

    A plugin data `dict` that will be saved on the `Group.plugin_data` attribute.

    # Return value

    A newly created `Group` instance.
    """

    def __call__(self, action: CreateGroupHookAction, **kwargs) -> Group: ...


class CreateGroupHook(FilterHook[CreateGroupHookAction, CreateGroupHookFilter]):
    """
    This hook wraps the standard function that Misago uses to create a new user group.

    Misago group creation logic is a thin wrapper for `Group.objects.create()` that
    updates the `kwargs` to include a valid `slug` generated from the `name` and next
    valid `ordering` position.

    If `kwargs` contains either `request` of `form` special keys, those are also removed
    before the `create(**kwargs)` is called.

    # Example

    The code below implements a custom filter function that stores an ID of user who
    created the group, if its available:

    ```python
    from django.http import HttpRequest
    from misago.postgres.delete import delete_all
    from misago.users.models import Group

    @create_group_hook.append_filter
    def set_group_creator_id(action, **kwargs) -> Group:
        # request and plugin_data keys are guaranteed to be set in `kwargs`
        if kwargs["request"] and kwargs["request"].user.id:
            kwargs["plugin_data"]["creator_id"] = kwargs["request"].user.id

        # Call the next function in chain
        return action(group, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(self, action: CreateGroupHookAction, **kwargs) -> Group:
        return super().__call__(action, **kwargs)


create_group_hook = CreateGroupHook()
