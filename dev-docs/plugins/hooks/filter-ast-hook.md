# `filter_ast_hook`

This hook wraps the standard function that Misago uses to filter an abstract syntax tree representing the contents of parsed markup.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import filter_ast_hook
```


## Filter

```python
def custom_ast_filter(
    action: FilterAstHookAction, ast: list, content_type: str | None=None
) -> list:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterAstHookAction`

A standard Misago function used to process and clean an abstract syntax tree returned by the parser or next filter function from another plugin.

See the [action](#action) section for details.


### Arguments

#### `ast: list`

A list of Python `dict`s with AST returned by the parser.


#### `content_type: str | None = None`

A `str` with the name of the content type (e.g., `post` or `signature`) or `None` if not provided.


### Return value

A list of Python `dict`s with an AST for parsed markup.


## Action

```python
def filter_ast_action(ast: list, content_type: str | None=None) -> list:
    ...
```

A standard Misago function used to process and clean an abstract syntax tree returned by the parser or next filter function from another plugin.


### Arguments

#### `ast: list`

A list of Python `dict`s with AST returned by the parser.


#### `content_type: str | None = None`

A `str` with the name of the content type (e.g., `post` or `signature`) or `None` if not provided.


### Return value

A list of Python `dict`s with an AST for parsed markup.


## Example

The code below implements a custom filter function that adds the table Mistune plugin to the parser:

```python
from typing import Callable, Protocol

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from mistune import BlockParser, InlineParser, Markdown
from mistune.plugins.table import table

User = get_user_model()

@create_markdown_hook.append_filter
def register_custom_markdown_plugin(
    action: FilterAstHookAction, *, plugins, **kwargs
) -> None:
    plugins.append(table)

    # Call the next function in chain
    return action(plugins=plugins, **kwargs)
```