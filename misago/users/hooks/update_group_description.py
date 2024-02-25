from typing import Protocol

from ...plugins.hooks import FilterHook
from ..models import Group


class UpdateGroupDescriptionHookAction(Protocol):
    """
    A standard Misago function used to update an existing user group's description or
    the next filter function from another plugin.

    # Arguments

    ## `group: Group`

    A group instance to update.

    ## `**kwargs`

    A `dict` with group description's attributes to update.

    # Additional arguments

    Optional arguments in `kwargs` that are not used to update the group but are still
    provided for use by plugins:

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.

    ## `form: Optional[Form]`

    Bound `Form` instance that was used to update this group's description.

    # Return value

    An updated `Group` instance.
    """

    def __call__(self, group: Group, **kwargs) -> Group: ...


class UpdateGroupDescriptionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UpdateGroupDescriptionHookAction`

    A standard Misago function used to update an existing user group's description or
    the next filter function from another plugin.

    See the [action](#action) section for details.

    ## `group: Group`

    A group instance to update.

    ## `**kwargs`

    A `dict` with group description's attributes to update.

    # Additional arguments

    Optional arguments in `kwargs` that are not used to update the group but are still
    provided for use by plugins:

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.

    ## `form: Optional[Form]`

    Bound `Form` instance that was used to update this group's description.

    # Return value

    An updated `Group` instance.
    """

    def __call__(
        self, action: UpdateGroupDescriptionHookAction, group: Group, **kwargs
    ) -> Group: ...


class UpdateGroupDescriptionHook(
    FilterHook[UpdateGroupDescriptionHookAction, UpdateGroupDescriptionHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to update
    user group's description.

    # Example

    The code below implements a custom filter function that stores an ID of user who
    last modified the group description, if its available:

    ```python
    from django.http import HttpRequest
    from misago.users.models import Group

    @update_group_description_hook.append_filter
    def set_group_description_updated_by_id(action, **kwargs) -> Group:
        # request key is guaranteed to be set in `kwargs`
        if kwargs["request"] and kwargs["request"].user.id:
            group.description.plugin_data["updated_by"] = kwargs["request"].user.id

        # Call the next function in chain
        return action(group, **kwargs)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self, action: UpdateGroupDescriptionHookAction, group: Group, **kwargs
    ) -> Group:
        return super().__call__(action, group, **kwargs)


update_group_description_hook = UpdateGroupDescriptionHook()
