# `complete_markup_html_hook`

This hook wraps the standard function that Misago uses to complete an HTML representation of parsed markup.

Completion process includes:

- Replacing of placeholder spoiler blocks summaries with messages in active language. - Replacing quotation blocks headers with final HTML.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import complete_markup_html_hook
```


## Filter

```python
def custom_complete_markup_html_filter(
    action: CompleteMarkupHtmlHookAction, html: str, **kwargs
) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CompleteMarkupHtmlHookAction`

A standard Misago function used to complete an HTML representation of parsed markup or the next filter function from another plugin.

See the [action](#action) section for details.


#### `html: str`

An HTML representation of parsed markup to complete.


#### `**kwargs`

Additional data that can be used to complete the HTML.


### Return value

A `str` with completed HTML representation of parsed markup.


## Action

```python
def complete_markup_html_action(html: str, **kwargs) -> str:
    ...
```

A standard Misago function used to complete an HTML representation of parsed markup or the next filter function from another plugin.


### Arguments

#### `html: str`

An HTML representation of parsed markup to complete.


#### `**kwargs`

Additional data that can be used to complete the HTML.


### Return value

A `str` with completed HTML representation of parsed markup.


## Example

The code below implements a custom filter function that replaces default spoiler block summary with a custom message:

```python
from misago.parser.context import ParserContext
from misago.parser.html import SPOILER_SUMMARY


@complete_markup_html_hook.append_filter
def complete_markup_html_with_custom_spoiler-summary(
    action: CompleteMarkupHtmlHookAction,
    html: str,
    **kwargs,
) -> str:
    if SPOILER_SUMMARY in html:
        html = html.replace(
            SPOILER_SUMMARY, "SPOILER! Click at your own discretion!"
        )

    # Call the next function in chain
    return action(context, html, **kwargs)
```