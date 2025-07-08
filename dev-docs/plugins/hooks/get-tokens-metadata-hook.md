# `get_tokens_metadata_hook`

This hook wraps the standard function Misago uses to extract metadata from a token stream.

Token stream is a list of the `Token` instances from `markdown_it.tokens` module.


## Location

This hook can be imported from `misago.parser.hooks`:

```python
from misago.parser.hooks import get_tokens_metadata_hook
```


## Filter

```python
def custom_get_tokens_metadata_filter(
    action: GetTokensMetadataHookAction, tokens: list[Token]
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetTokensMetadataHookAction`

Misago function used to extract metadata from a token stream.

See the [action](#action) section for details.


#### `tokens: list[Token]`

A list of tokens ("token stream") from which to extract metadata.


### Return value

A `dict` with metadata extracted from the token stream.


## Action

```python
def get_tokens_metadata_action(tokens: list[Token]) -> dict:
    ...
```

Misago function used to extract metadata from a token stream.


### Arguments

#### `tokens: list[Token]`

A list of tokens ("token stream") from which to extract metadata.


### Return value

A `dict` with metadata extracted from the token stream.


## Example

The code below implements a custom filter function that sets `plugin` metadata if its found in tokens:

```python
from markdown_it.tokens import Token
from misago.parser.hooks import get_tokens_metadata_hook

@get_tokens_metadata_hook.append_filter
def get_tokens_metadata_plugin(action, tokens: list[Token]) -> dict:
    metadata = action(tokens)

    if plugin_metadata := get_plugin_metadata(tokens):
        metadata["plugin"] = plugin_metadata

    return metadata
```