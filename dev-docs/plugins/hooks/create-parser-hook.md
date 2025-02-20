# `create_parser_hook`

This hook wraps the standard function that Misago uses to create a markup parser instance.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import create_parser_hook
```


## Filter

```python
def custom_create_parser_filter(
    action: CreateParserHookAction,
    context: 'ParserContext',
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    post_processors: list[Callable[[Parser, list[dict]],
    list[dict]]],
) -> Parser:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreateParserHookAction`

A standard Misago function used to create a markup parser instance or the next filter function from another plugin.

See the [action](#action) section for details.


#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `block_patterns: list[Pattern]`

A list of `Pattern` instances of block patterns to be used by the parser.


#### `inline_patterns: list[Pattern]`

A list of `Pattern` instances of inline patterns to be used by the parser.


#### `post_processors: list[Callable[[Parser, list[dict]], list[dict]]]`

A list of post-processor functions called by the parser to finalize the AST.

A post-processor function should have the following signature:

```python
def custom_postprocessor(parser: Parser, ast: list[dict]) -> list[dict]:
    # Do something with the 'ast'...
    return ast
```


### Return value

An instance of the `Parser` class.


## Action

```python
def create_parser_action(
    context: 'ParserContext',
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    post_processors: list[Callable[[Parser, list[dict]],
    list[dict]]],
) -> Parser:
    ...
```

A standard Misago function used to create a markup parser instance or the next filter function from another plugin.


### Arguments

#### `context: ParserContext`

An instance of the `ParserContext` data class that contains dependencies used during parsing.


#### `block_patterns: list[Pattern]`

A list of `Pattern` instances of block patterns to be used by the parser.


#### `inline_patterns: list[Pattern]`

A list of `Pattern` instances of inline patterns to be used by the parser.


#### `post_processors: list[Callable[[Parser, list[dict]], list[dict]]]`

A list of post-processor functions called by the parser to finalize the AST.

A post-processor function should have the following signature:

```python
def custom_postprocessor(parser: Parser, ast: list[dict]) -> list[dict]:
    # Do something with the 'ast'...
    return ast
```


### Return value

An instance of the `Parser` class.


## Example

The code below implements a custom filter function that adds new block pattern to the parser:

```python
from misago.parser.context import ParserContext
from misago.parser.hooks import create_parser_hook
from misago.parser.parser import Parser

from .patterns import PluginPattern


@create_parser_hook.append_filter
def create_parser_with_custom_pattern(
    action: CreateParserHookAction,
    context: ParserContext,
    *,
    block_patterns,
    **kwargs,
) -> Parser:
    block_patterns.append(PluginPattern)

    # Call the next function in chain
    return action(context, block_patterns=block_patterns, **kwargs)
```