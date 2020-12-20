# `convert_rich_text_to_html_hook`

```python
convert_rich_text_to_html_hook.call_action(
    action: ConvertRichTextBlockToHTMLAction, context: GraphQLContext, rich_text: List[dict]
)
```

A synchronous filter for the function used to convert rich text to HTML.

Returns `str`.


## Required arguments

### `action`

```python
def convert_rich_text_to_html(
    context: GraphQLContext, rich_text: List[dict]
) -> str:
    ...
```

Next filter or built-in function used to convert rich text to HTML `str`.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context.


### `rich_text`

```python
List[dict]
```

List of `dict` containing the rich text to be converted.