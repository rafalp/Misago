# `setup_parser_context_hook`

This hook wraps the standard function that Misago uses to setup a `ParserContext` instance.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import setup_parser_context_hook
```


## Filter

```python
def custom_setup_parser_context_filter(
    action: SetupParserContextHookAction, context: 'ParserContext'
) -> 'ParserContext':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SetupParserContextHookAction`

A standard Misago function used to setup the Parser Context data class instance or the next filter function from another plugin.

See the [action](#action) section for details.


#### `context: ParserContext`

A `ParserContext` data class instance to setup.


### Return value

A `ParserContext` instance to use during parsing.


## Action

```python
def setup_parser_context_action(context: 'ParserContext') -> 'ParserContext':
    ...
```

A standard Misago function used to setup the Parser Context data class instance or the next filter function from another plugin.


### Arguments

#### `context: ParserContext`

A `ParserContext` data class instance to setup.


### Return value

A `ParserContext` instance to use during parsing.


## Example

The code below implements a custom filter function that adds extra data to `plugin_data` dictionary on `ParserContext`:

```python
from misago.parser.context import ParserContext
from misago.parser.hooks import setup_parser_context_hook


@setup_parser_context_hook.append_filter
def register_plugin_data_in_parser_context(
    action: SetupParserContextHookAction, context: ParserContext
) -> ParserContext:
    if context.request:
        context.plugin_data["my_plugin"] = request.my_plugin.get_parser_context()

    # Call the next function in chain
    return action(context)
```