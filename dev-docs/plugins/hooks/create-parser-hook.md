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
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    user: User | None=None,
    request: HttpRequest | None=None,
    content_type: str | None=None,
) -> Parser:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreateParserHookAction`

A standard Misago function used to create a markup parser instance or the next filter function from another plugin.

See the [action](#action) section for details.


#### `block_patterns: list[Pattern]`

A list of `Pattern` instances of block patterns to be used by the parser.


#### `inline_patterns: list[Pattern]`

A list of `Pattern` instances of inline patterns to be used by the parser.


#### `user: User | None = None`

A `User` instance with the parsed text's author or `None` if not provided.


#### `request: HttpRequest | None = None`

The request object or `None` if it was not provided.


#### `content_type: str | None = None`

A `str` with the name of the content type to be parsed (e.g., `post` or `signature`) or `None` if not provided.


### Return value

An instance of the `Parser` class from the `mistune` library.


## Action

```python
def create_parser_action(
    *,
    block_patterns: list[Pattern],
    inline_patterns: list[Pattern],
    user: User | None=None,
    request: HttpRequest | None=None,
    content_type: str | None=None,
) -> Parser:
    ...
```

A standard Misago function used to create a markup parser instance or the next filter function from another plugin.


### Arguments

#### `block_patterns: list[Pattern]`

A list of `Pattern` instances of block patterns to be used by the parser.


#### `inline_patterns: list[Pattern]`

A list of `Pattern` instances of inline patterns to be used by the parser.


#### `user: User | None = None`

A `User` instance with the parsed text's author or `None` if not provided.


#### `request: HttpRequest | None = None`

The request object or `None` if it was not provided.


#### `content_type: str | None = None`

A `str` with the name of the content type to be parsed (e.g., `post` or `signature`) or `None` if not provided.


### Return value

An instance of the `Parser` class from the `mistune` library.


## Example

The code below implements a custom filter function that adds new block pattern to the parser:

```python
from misago.parser.parser import Parser

from .patterns import PluginPattern


@create_markdown_hook.append_filter
def register_custom_pattern(
    action: CreateParserHookAction, *, block_patterns, **kwargs
) -> Parser:
    block_patterns.append(PluginPattern)

    # Call the next function in chain
    return action(block_patterns=block_patterns, **kwargs)
```