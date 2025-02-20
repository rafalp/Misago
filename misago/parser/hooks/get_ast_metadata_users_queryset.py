from typing import TYPE_CHECKING, Iterable, Protocol

from django.contrib.auth import get_user_model

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..context import ParserContext

User = get_user_model()


class GetAstMetadataUsersQuerysetHookAction(Protocol):
    """
    A standard Misago function used to create a `User` queryset or the next filter
    function from another plugin.

    # Arguments

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `usernames: list[str]`

    A list of normalized usernames of `User` instance to retrieve from the database.

    Names are normalized using the `slugify` function from `misago.core.utils`.

    # Return value

    A queryset with `User` instances to use in updating the metadata.
    """

    def __call__(
        self,
        *,
        context: "ParserContext",
        usernames: list[str],
    ) -> Iterable[User]: ...


class GetAstMetadataUsersQuerysetHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetAstMetadataUsersQuerysetHookAction`

    A standard Misago function used to create a `User` queryset or the next filter
    function from another plugin.

    See the [action](#action) section for details.

    ## `context: ParserContext`

    An instance of the `ParserContext` data class that contains dependencies
    used during parsing.

    ## `usernames: list[str]`

    A list of normalized usernames of `User` instance to retrieve from the database.

    Names are normalized using the `slugify` function from `misago.core.utils`.

    # Return value

    A queryset with `User` instances to use in updating the metadata.
    """

    def __call__(
        self,
        action: GetAstMetadataUsersQuerysetHookAction,
        context: "ParserContext",
        usernames: list[str],
    ) -> Iterable[User]: ...


class GetAstMetadataUsersQuerysetHook(
    FilterHook[
        GetAstMetadataUsersQuerysetHookAction, GetAstMetadataUsersQuerysetHookFilter
    ]
):
    """
    This hook wraps the standard function that Misago uses to retrieve the metadata
    with data from the Abstract Syntax Tree representation of parsed markup.

    It can be employed to initialize new keys in the `metadata` dictionary before
    the next action call and to retrieve missing data from the database or another
    source after the action.

    # Example

    The code below implements a custom filter function that updates the queryset
    to exclude users belonging to a specified group.

    ```python
    from misago.parser.context import ParserContext
    from misago.parser.hooks import get_ast_metadata_users_queryset_hook


    @get_ast_metadata_users_queryset_hook.append_filter
    def get_ast_metadata_users_queryset_exclude_promotors(
        action,
        context: ParserContext,
        usernames: list[str],
    ):
        return action(context, usernames).exclude(group_id=10)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetAstMetadataUsersQuerysetHookAction,
        context: "ParserContext",
        usernames: list[str],
    ):
        return super().__call__(action, context, usernames)


get_ast_metadata_users_queryset_hook = GetAstMetadataUsersQuerysetHook()
