# `convert_rich_text_block_to_html_hook`

```python
convert_rich_text_block_to_html_hook.call_action(
    action: ConvertRichTextBlockToHTMLAction, context: GraphQLContext, block: dict
)
```

A synchronous filter for the function used to convert `dict` with rich text block to HTML.

Returns `str` or `None`.


## Required arguments

### `action`

```python
def convert_rich_text_block_to_html(
    context: GraphQLContext, block: dict
) -> Optional[str]:
    ...
```

Next filter or built-in function used to convert `dict` with rich text block to HTML `str`.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context.


### `block`

```python
dict
```

`dict` containing the rich text representation of the block.