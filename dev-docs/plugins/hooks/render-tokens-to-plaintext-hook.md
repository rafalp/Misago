# `render_tokens_to_plaintext_hook`

This hook wraps the standard function Misago uses to convert a token stream into plain text.

Token stream is a list of the `Token` instances from `markdown_it.tokens` module.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import render_tokens_to_plaintext_hook
```


## Filter

```python
def custom_render_tokens_to_plaintext_filter(
    action: RenderTokensToPlaintextHookAction,
    tokens: list[Token],
    rules: list[Callable[['StatePlaintext'],
    bool]],
) -> str:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RenderTokensToPlaintextHookAction`

A standard Misago function used to convert a token stream into plain text.

See the [action](#action) section for details.


#### `tokens: list[Token]`

A list of `Token` instances to render as text.


#### `rules: list[Callable[[StatePlaintext], bool]]`

A list of `callable`s with rendering rules.


### Return value

A `str` with rendered text.


## Action

```python
def render_tokens_to_plaintext_action(
    tokens: list[Token], rules: list[Callable[['StatePlaintext'], bool]]
) -> str:
    ...
```

A standard Misago function used to convert a token stream into plain text.


### Arguments

#### `tokens: list[Token]`

A list of `Token` instances to render as text.


#### `rules: list[Callable[[StatePlaintext], bool]]`

A list of `callable`s with rendering rules.


### Return value

A `bool` with rendered text.


## Example

The code below implements a custom filter function that includes custom rule for token stream rendering:

```python
from typing import Callable

from markdown_it.tokens import Token
from misago.parser.hooks import render_tokens_to_plaintext_hook
from misago.parser.plaintext import StatePlaintext


def custom_renderer_rule(state: StatePlaintext) -> bool:
    token = state.tokens[state.pos]
    if token.type != "plugin":
        return False

    state.push(tokens[idx].content)
    state.pos += 1

    return True


@render_tokens_to_plaintext_hook.append_filter
def tokenize_with_custom_tokens_processor(
    action,
    tokens: list[Token],
    rules: list[Callable[["StatePlaintext"], bool]],
) -> str:
    rules.append(("custom_rule", custom_renderer_rule))
    return action(parser, markup, processors)
```