# `highlight_syntax_hook`

This hook wraps the standard function that Misago uses to return HTML with highlighted code.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import highlight_syntax_hook
```


## Filter

```python
def custom_highlight_syntax_filter(
    action: HighlightSyntaxHookAction, syntax: str, code: str
) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: HighlightSyntaxHookAction`

Misago function used to return HTML with highlighted code.

See the [action](#action) section for details.


#### `syntax: str`

A syntax to use for code highlighting.


#### `code: str`

A code snippet to highlight.


### Return value

An HTML string with highlighted code.


## Action

```python
def highlight_syntax_action(syntax: str, code: str) -> str:
    ...
```

Misago function used to return HTML with highlighted code.


### Arguments

#### `syntax: str`

A syntax to use for code highlighting.


#### `code: str`

A code snippet to highlight.


### Return value

An HTML string with highlighted code.


## Example

The code below implements a custom filter function that replaces the default syntax highlighting logic with a custom implementation.

```python
from misago.parser.hooks import highlight_syntax_hook
from plugin import custom_highlighter


@highlight_syntax_hook.append_filter
def replace_rich_text_spoiler_hoom(
    action,
    syntax: str,
    code: str,
) -> str:
    return custom_highlighter(syntax, code)
```