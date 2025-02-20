# `update_ast_metadata_users_hook`

This hook wraps the standard function that Misago uses to update the metadata with users from the database.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import update_ast_metadata_users_hook
```


## Filter

```python
def custom_update_ast_metadata_users_filter(
    action: UpdateAstMetadataUsersHookAction,
    context: 'ParserContext',
    metadata: dict,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UpdateAstMetadataUsersHookAction`

A standard Misago function used to update the metadata with users from the database, or the next filter function from another plugin.

See the [action](#action) section for details.


#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `metadata: dict`

A `dict` with metadata to update.


## Action

```python
def update_ast_metadata_users_action(*, context: 'ParserContext', metadata: dict) -> None:
    ...
```

A standard Misago function used to update the metadata with users from the database, or the next filter function from another plugin.


### Arguments

#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `metadata: dict`

A `dict` with metadata to update.


## Example

The code below implements a custom filter function that removes users with extra flag in their `plugin_data`:

```python
from misago.parser.context import ParserContext
from misago.parser.hooks import update_ast_metadata_users_hook


@update_ast_metadata_users_hook.append_filter
def update_ast_metadata_users_remove(
    action: UpdateAstMetadataUsersHookAction,
    context: ParserContext,
    metadata: dict,
) -> None:
    for key, user in list(metadata["users"].items()):
        if user.plugin_data.get("disable_mentions"):
            del metadata["users"][key]

    action(context, metadata)