# `tokenize_hook`

This hook wraps the standard function Misago uses to create a token stream from markup.

Token stream is a list of the `Token` instances from `markdown_it.tokens` module.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import tokenize_hook
```


## Filter

```python
def custom_tokenize_filter(
    action: TokenizeHookAction,
    parser: MarkdownIt,
    markup: str,
    processors: list[Callable[[list[Token]],
    list[Token] | None]],
) -> list[Token]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: TokenizeHookAction`

Misago function used to create a token stream from markup.

See the [action](#action) section for details.


#### `parser: MarkdownIt`

A `MarkdownIt` instance used to parse the `markup` string.


#### `markup: str`

A `str` to tokenize.


#### `processors: Iterable[Callable[[list[Token]], list[Token] | None]]`

A list of callables that each accept a single argument (a list of tokens) and return either a updated list of tokens or `None` if no changes were made.


### Return value

A list of `Token` instances.


## Action

```python
def tokenize_action(
    parser: MarkdownIt,
    markup: str,
    processors: list[Callable[[list[Token]],
    list[Token] | None]],
) -> list[Token]:
    ...
```

Misago function used to create a token stream from markup.


### Arguments

#### `parser: MarkdownIt`

A `MarkdownIt` instance used to parse the `markup` string.


#### `markup: str`

A `str` to tokenize.


#### `processors: Iterable[Callable[[list[Token]], list[Token] | None]]`

A list of callables that each accept a single argument (a list of tokens) and return either a updated list of tokens or `None` if no changes were made.


### Return value

A list of `Token` instances.


## Example

The code below implements a custom filter function that includes custom processor for token stream:

```python
from typing import Callable

from markdown_it import MarkdownIt
from markdown_it.tokens import Token
from misago.parser.hooks import tokenize_hook


def custom_tokens_processor(tokens: list[Token]) -> list[Token] | None:
    return tokens  # Return changed `tokens` list or None


@tokenize_hook.append_filter
def tokenize_with_custom_tokens_processor(
    action,
    parser: MarkdownIt,
    markup: str,
    processors: list[Callable[[list[Token]], list[Token] | None]],
) -> list[Token]:
    processors.append(custom_tokens_processor)
    return action(parser, markup, processors)
```