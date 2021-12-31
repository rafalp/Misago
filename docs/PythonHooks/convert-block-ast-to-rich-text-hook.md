# `convert_block_ast_to_rich_text_hook`

```python
from misago.richtext.hooks import convert_block_ast_to_rich_text_hook

convert_block_ast_to_rich_text_hook.call_action(
    action: ConvertBlockAstToRichTextAction,
    context: GraphQLContext,
    ast: dict,
    metadata: dict,
)
```

A synchronous filter for the function used to convert `dict` with block's abstract syntax tree to `RichTextBlock`.

Returns JSON-serializable `dict` if block's AST is valid or `None`.


## Required arguments

### `action`

```python
def convert_block_ast_to_rich_text(
    context: GraphQLContext, act: dict
) -> Optional[RichTextBlock]:
    ...
```

Next filter or built-in function used to convert `dict` with block's abstract syntax tree to `RichTextBlock`.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context.


### `ast`

```python
dict
```

`dict` containing abstract syntax tree for markup block as returned by `mistune.AstRenderer`.


### `metadata`

```python
Dict[str, Any]
```

A mutable dict with all metadata for parsed markup.