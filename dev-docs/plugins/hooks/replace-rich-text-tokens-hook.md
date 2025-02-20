# `replace_rich_text_tokens_hook`

This hook wraps the standard function that Misago uses to replace rich-text tokens in pre-rendered HTML or the next filter from another plugin.

Tokens are pseudo-HTML elements like `<attachment="..">` that are replaced with real HTML markup instead.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import replace_rich_text_tokens_hook
```


## Filter

```python
def custom_replace_rich_text_tokens_filter(
    action: ReplaceRichTextTokensHookAction, html: str, data: dict
) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ReplaceRichTextTokensHookAction`

A standard Misago function used to replace rich-text tokens in pre-rendered HTML or the next filter from another plugin.

See the [action](#action) section for details.


#### `html: str`

An HTML string in which tokens will be replaced.


#### `data: dict`

Data that can be embedded in HTML.


### Return value

A `str` with HTML that has its tokens replaced.


## Action

```python
def replace_rich_text_tokens_action(html: str, data: dict) -> str:
    ...
```

A standard Misago function used to replace rich-text tokens in pre-rendered HTML or the next filter from another plugin.


### Arguments

#### `html: str`

An HTML string in which tokens will be replaced.


#### `data: dict`

Data that can be embedded in HTML.


### Return value

A `str` with HTML that has its tokens replaced.


## Example

The code below implements a custom filter function that replaces default spoiler block summary with a custom message:

```python
from misago.parser.context import ParserContext
from misago.parser.hooks import replace_rich_text_tokens_hook
from misago.parser.html import SPOILER_SUMMARY


@replace_rich_text_tokens_hook.append_filter
def replace_rich_text_spoiler_hoom(
    action: ReplaceRichTextTokensHookAction,
    html: str,
    data: dict,
) -> str:
    if SPOILER_SUMMARY in html:
        html = html.replace(
            SPOILER_SUMMARY, "SPOILER! Click at your own discretion!"
        )

    # Call the next function in chain
    return action(context, html, **kwargs)
```