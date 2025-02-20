# `get_ast_metadata_users_queryset_hook`

This hook wraps the standard function that Misago uses to retrieve the metadata with data from the Abstract Syntax Tree representation of parsed markup.

It can be employed to initialize new keys in the `metadata` dictionary before the next action call and to retrieve missing data from the database or another source after the action.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import get_ast_metadata_users_queryset_hook
```


## Filter

```python
def custom_get_ast_metadata_users_queryset_filter(
    action: GetAstMetadataUsersQuerysetHookAction,
    context: 'ParserContext',
    usernames: list[str],
) -> Iterable[User]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetAstMetadataUsersQuerysetHookAction`

A standard Misago function used to create a `User` queryset or the next filter function from another plugin.

See the [action](#action) section for details.


#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `usernames: list[str]`

A list of normalized usernames of `User` instance to retrieve from the database.

Names are normalized using the `slugify` function from `misago.core.utils`.


### Return value

A queryset with `User` instances to use in updating the metadata.


## Action

```python
def get_ast_metadata_users_queryset_action(*, context: 'ParserContext', usernames: list[str]) -> Iterable[User]:
    ...
```

A standard Misago function used to create a `User` queryset or the next filter function from another plugin.


### Arguments

#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `usernames: list[str]`

A list of normalized usernames of `User` instance to retrieve from the database.

Names are normalized using the `slugify` function from `misago.core.utils`.


### Return value

A queryset with `User` instances to use in updating the metadata.


## Example

The code below implements a custom filter function that updates the queryset to exclude users belonging to a specified group.

```python
from misago.parser.context import ParserContext
from misago.parser.hooks import get_ast_metadata_users_queryset_hook


@get_ast_metadata_users_queryset_hook.append_filter
def get_ast_metadata_users_queryset_exclude_promotors(
    action: GetAstMetadataUsersQuerysetHookAction,
    context: ParserContext,
    usernames: list[str],
):
    return action(context, usernames).exclude(group_id=10)
```