from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Group


class DeleteGroupHookAction(Protocol):
    """
    A standard Misago function used for deleting the user group, or the next
    filter function from another plugin.

    # Arguments

    ## `group: Group`

    A `Group` model instance to delete from the database.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        group: Group,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeleteGroupHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteGroupHookAction`

    A standard Misago function used for deleting the user group, or the next
    filter function from another plugin.

    See the [action](#action) section for details.

    ## `group: Group`

    A `Group` model instance to delete from the database.

    ## `request: Optional[HttpRequest]`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        action: DeleteGroupHookAction,
        group: Group,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeleteGroupHook(FilterHook[DeleteGroupHookAction, DeleteGroupHookFilter]):
    """
    This hook wraps the standard function that Misago uses to delete a user group.

    Misago executes delete queries for groups and their relations directly, skipping
    the Django ORM which uses the Object Collector logic to simulate the delete cascade
    behavior that databases implement and run the pre and post delete signals.

    Because of this, plugins need to explicitly delete objects related to the deleted
    group in custom filters before a group itself is deleted from the database.

    # Example

    The code below implements a custom filter function that deletes a custom model
    implemented in a plugin before group itself is deleted:

    ```python
    from django.http import HttpRequest
    from misago.postgres.delete import delete_all
    from misago.users.models import Group

    from .models import GroupPromotionRule

    @delete_group_hook.append_filter
    def delete_group_promotion_rules(
        action, group: Group, request: HttpRequest | None = None
    ) -> None:
        # Delete promotion rules related with this group bypassing the Django ORM
        delete_all(GroupPromotionRule, group_id=group.id)

        # Call the next function in chain
        return action(group, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteGroupHookAction,
        group: Group,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, group, request)


delete_group_hook = DeleteGroupHook()
